from __future__ import annotations

import socket as socket_module
from typing import TYPE_CHECKING, cast

import pytest

from peary.peary_client import PearyClient
from peary.peary_protocol import PearyProtocol
from peary.peary_proxy import PearyProxy

if TYPE_CHECKING:
    from typing import Any

    from typing_extensions import Buffer


class MockSocket(socket_module.socket):
    """Mock socket class."""

    address: tuple[str, int] | None = None
    is_connected: bool | None = None
    is_shutdown: bool | None = None
    how_shutdown: int | None = None

    # pylint: disable=super-init-not-called,unused-argument,redefined-builtin
    def __init__(
        self,
        family: int,  # noqa: ARG002
        type: int,  # noqa: A002, ARG002
        proto: int = 0,  # noqa: ARG002
        fileno: int | None = None,  # noqa: ARG002
    ) -> None:
        self.address: tuple[Any, ...] | str | Buffer | None = None

    # pylint: enable=super-init-not-called,unused-argument,redefined-builtin

    def connect(self, address: tuple[Any, ...] | str | Buffer) -> None:
        """Mock connect method."""
        MockSocket.is_connected = True
        MockSocket.is_shutdown = False
        MockSocket.address = cast("tuple[str, int]", address)

    # pylint: disable-next=R6301
    def shutdown(self, how: int) -> None:
        """Mock connect method."""
        MockSocket.is_shutdown = True
        MockSocket.how_shutdown = how

    # pylint: disable-next=R6301
    def close(self) -> None:
        """Mock connect method."""
        MockSocket.is_connected = False

    def settimeout(self, value: float | None = None) -> None:
        """Mock settimeout method"""

    # pylint: disable-next=W0613
    def recv(self, size: int, flags: int = 0) -> bytes:  # noqa: ARG002
        return PearyProtocol.encode(PearyProtocol.VERSION, 1, PearyProtocol.STATUS_OK)

    # pylint: disable-next=W0613
    def send(self, data: Buffer, flags: int = 0) -> int:  # noqa: ARG002
        return len(bytes(data))


def test_peary_client_context_manager_executes_body() -> None:
    with PearyClient("", socket_class=MockSocket):
        test_result = True
    assert test_result is True


def test_peary_client_context_manager_returns_proxy_class() -> None:
    class MockProxy(PearyProxy):
        """Mock proxy class."""

    with PearyClient("", socket_class=MockSocket) as client:
        assert isinstance(client, PearyProxy)
    with PearyClient("", socket_class=MockSocket, proxy_class=MockProxy) as client:
        assert isinstance(client, MockProxy)


def test_peary_client_context_manager_enter_socket_connect_good() -> None:
    MockSocket.is_connected = None
    with PearyClient("", socket_class=MockSocket):
        assert MockSocket.is_connected is True


def test_peary_client_context_manager_enter_socket_connect_error() -> None:
    with pytest.raises(PearyClient.PearySockerError) as e, PearyClient("-", 0):
        pass  # pragma: no cover
    assert "Unable to connect to host - using port 0." in str(e)


def test_peary_client_context_manager_enter_socket_address_default_port() -> None:
    MockSocket.address = None
    with PearyClient("alpha", socket_class=MockSocket):
        assert MockSocket.address == ("alpha", 12345)
    with PearyClient("beta", socket_class=MockSocket):
        assert MockSocket.address == ("beta", 12345)


def test_peary_client_context_manager_enter_socket_address_nondefault_port() -> None:
    MockSocket.address = None
    with PearyClient(host="", port=0, socket_class=MockSocket):
        assert MockSocket.address == ("", 0)
    with PearyClient(host="", port=1, socket_class=MockSocket):
        assert MockSocket.address == ("", 1)


def test_peary_client_context_manager_exit_socket_shutdown() -> None:
    MockSocket.is_shutdown = None
    MockSocket.how_shutdown = None
    with PearyClient(host="", port=0, socket_class=MockSocket):
        pass
    assert MockSocket.is_shutdown is True
    assert MockSocket.how_shutdown == socket_module.SHUT_RDWR


def test_peary_client_context_manager_exit_socket_closes() -> None:
    MockSocket.is_connected = None
    with PearyClient("", socket_class=MockSocket):
        assert MockSocket.is_connected is True
    assert MockSocket.is_connected is False


def test_peary_client_context_manager_enter_socket_exit_gracefully() -> None:
    class MockError(Exception):
        """Mock exception for testing purposes."""

    MockSocket.is_shutdown = None
    MockSocket.how_shutdown = None
    MockSocket.is_connected = None

    try:  # pylint: disable=too-many-try-statements
        with PearyClient("", socket_class=MockSocket):
            raise MockError  # noqa: TRY301
    except MockError:
        assert MockSocket.is_connected is False
        assert MockSocket.is_shutdown is True
        assert MockSocket.how_shutdown == socket_module.SHUT_RDWR
