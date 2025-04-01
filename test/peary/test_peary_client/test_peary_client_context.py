from __future__ import annotations

import socket as socket_module
from typing import TYPE_CHECKING

import pytest

from peary.peary_client import PearyClient
from peary.peary_proxy import PearyProxy

if TYPE_CHECKING:
    from .conftest import MockSocket


def test_peary_client_context_manager_executes_body(
    mock_socket_class: type[MockSocket],
) -> None:
    with PearyClient("", socket_class=mock_socket_class):
        test_result = True
    assert test_result is True


def test_peary_client_context_manager_returns_proxy_class(
    mock_socket_class: type[MockSocket],
) -> None:
    with PearyClient("", socket_class=mock_socket_class) as client:
        assert isinstance(client, PearyProxy)


def test_peary_client_context_manager_enter_socket_connect_success(
    mock_socket_class: type[MockSocket],
) -> None:
    mock_socket_class.is_connected = None
    with PearyClient("", socket_class=mock_socket_class):
        assert mock_socket_class.is_connected is True


def test_peary_client_context_manager_enter_socket_connect_error() -> None:
    with pytest.raises(PearyClient.PearySockerError) as e, PearyClient("-", 0):
        pass  # pragma: no cover
    assert "Unable to connect to host - using port 0." in str(e)


def test_peary_client_context_manager_enter_socket_address_default_port(
    mock_socket_class: type[MockSocket],
) -> None:
    mock_socket_class.address = None
    with PearyClient("alpha", socket_class=mock_socket_class):
        assert mock_socket_class.address == ("alpha", 12345)
    with PearyClient("beta", socket_class=mock_socket_class):
        assert mock_socket_class.address == ("beta", 12345)


def test_peary_client_context_manager_enter_socket_address_nondefault_port(
    mock_socket_class: type[MockSocket],
) -> None:
    mock_socket_class.address = None
    with PearyClient(host="", port=0, socket_class=mock_socket_class):
        assert mock_socket_class.address == ("", 0)
    with PearyClient(host="", port=1, socket_class=mock_socket_class):
        assert mock_socket_class.address == ("", 1)


def test_peary_client_context_manager_exit_socket_shutdown(
    mock_socket_class: type[MockSocket],
) -> None:
    mock_socket_class.is_shutdown = None
    mock_socket_class.how_shutdown = None
    with PearyClient("", socket_class=mock_socket_class):
        pass
    assert mock_socket_class.is_shutdown is True
    assert mock_socket_class.how_shutdown == socket_module.SHUT_RDWR


def test_peary_client_context_manager_exit_socket_closes(
    mock_socket_class: type[MockSocket],
) -> None:
    mock_socket_class.is_connected = None
    with PearyClient("", socket_class=mock_socket_class):
        assert mock_socket_class.is_connected is True
    assert mock_socket_class.is_connected is False


def test_peary_client_context_manager_enter_socket_exit_gracefully(
    mock_socket_class: type[MockSocket],
) -> None:
    class MockError(Exception):
        """Mock exception for testing purposes."""

    mock_socket_class.is_shutdown = None
    mock_socket_class.how_shutdown = None
    mock_socket_class.is_connected = None

    try:  # pylint: disable=too-many-try-statements
        with PearyClient("", socket_class=mock_socket_class):
            raise MockError  # noqa: TRY301
    except MockError:
        assert mock_socket_class.is_connected is False
        assert mock_socket_class.is_shutdown is True
        assert mock_socket_class.how_shutdown == socket_module.SHUT_RDWR
