from __future__ import annotations

import socket as socket_module
import struct
from typing import TYPE_CHECKING, cast

from peary.peary_client import PearyClient
from peary.peary_protocol import PearyProtocol
from peary.peary_proxy import PearyProxy

if TYPE_CHECKING:
    from socket import socket as socket_type

    import pytest

    from peary.peary_protocol_interface import PearyProtocolInterface


class MockProxy(PearyProxy):
    """Mock proxy class."""

    # pylint: disable-next=W0231
    def __init__(
        self,
        socket: socket_type,
        protocol_class: type[PearyProtocolInterface] = PearyProtocol,  # noqa: ARG002
    ) -> None:
        """Mock intializer"""
        self.socket = socket


class MockSocket:
    """Mock socket class."""

    NUM_BITS_PACKET_ID = 2
    NUM_BITS_PACKET_LENGTH = 4
    NUM_BITS_PACKET_STATUS = 2
    PROTOCOL_VERSION = b"1"
    RESPONSE_STATUS_OK = 0
    STRUCT_PACKET_HEADER = struct.Struct("!HH")
    STRUCT_PACKET_LENGTH = struct.Struct("!L")

    is_connected = None
    is_shutdown = None
    how_shutdown = None
    timeout = None

    # pylint: disable-next=super-init-not-called,unused-argument
    def __init__(self, addr_family: int, socket_type: int) -> None:
        self.addr_family = addr_family
        self.socket_type = socket_type
        self.address: tuple[str, int] | None = None

    def connect(self, address: tuple[str, int]) -> None:
        """Mock connect method."""
        MockSocket.is_connected = True
        MockSocket.is_shutdown = False
        self.address = address

    # pylint: disable-next=R6301
    def shutdown(self, how: int) -> None:
        """Mock connect method."""
        MockSocket.is_shutdown = True
        MockSocket.how_shutdown = how

    # pylint: disable-next=R6301
    def close(self) -> None:
        """Mock connect method."""
        MockSocket.is_connected = False


# pylint: disable=no-member
def test_peary_client_init_host() -> None:
    assert PearyClient("alpha").host == "alpha"
    assert PearyClient("beta").host == "beta"


def test_peary_client_init_port() -> None:
    assert PearyClient("").port == 12345
    assert PearyClient("", 12345).port == 12345
    assert PearyClient("", 54321).port == 54321


def test_peary_client_init_proxy_class() -> None:
    assert PearyClient("").proxy_class is PearyProxy
    assert PearyClient("", proxy_class=MockProxy).proxy_class is MockProxy


def test_peary_client_init_socket(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr("socket.socket", MockSocket)
    assert (
        cast("MockSocket", PearyClient("").socket).addr_family == socket_module.AF_INET
    )
    assert (
        cast("MockSocket", PearyClient("").socket).socket_type
        == socket_module.SOCK_STREAM
    )
    assert cast("MockSocket", PearyClient("").socket).address is None
    assert cast("MockSocket", PearyClient("").socket).is_connected is None
    assert cast("MockSocket", PearyClient("").socket).is_shutdown is None


def test_peary_client_context_manager_runs_statements(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setattr("socket.socket", MockSocket)
    with PearyClient("", proxy_class=MockProxy):
        test_result = True
    assert test_result is True


def test_peary_client_context_manager_enter_proxy_class(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setattr("socket.socket", MockSocket)
    with PearyClient("", proxy_class=MockProxy) as client:
        assert isinstance(client, MockProxy)


def test_peary_client_context_manager_enter_socket_connects(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setattr("socket.socket", MockSocket)
    with PearyClient("", proxy_class=MockProxy) as client:
        assert cast("MockSocket", cast("MockProxy", client).socket).is_connected is True
        assert cast("MockSocket", cast("MockProxy", client).socket).is_shutdown is False


def test_peary_client_context_manager_enter_socket_address(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setattr("socket.socket", MockSocket)
    with PearyClient("alpha", port=0, proxy_class=MockProxy) as client:
        assert cast("MockSocket", cast("MockProxy", client).socket).address == (
            "alpha",
            0,
        )
    with PearyClient("beta", port=1, proxy_class=MockProxy) as client:
        assert cast("MockSocket", cast("MockProxy", client).socket).address == (
            "beta",
            1,
        )


def test_peary_client_context_manager_exit_socket_closes(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setattr("socket.socket", MockSocket)

    mock_socket = MockSocket(socket_module.AF_INET, socket_module.SOCK_STREAM)
    with PearyClient("", proxy_class=MockProxy):
        pass
    assert mock_socket.is_connected is False


def test_peary_client_context_manager_exit_socket_shutdown(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setattr("socket.socket", MockSocket)

    mock_socket = MockSocket(socket_module.AF_INET, socket_module.SOCK_STREAM)
    with PearyClient("", proxy_class=MockProxy):
        pass
    assert mock_socket.is_shutdown is True
    assert mock_socket.how_shutdown == socket_module.SHUT_RDWR


def test_peary_client_context_manager_enter_socket_exit_gracefully(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setattr("socket.socket", MockSocket)

    class MockError(Exception):
        """Mock exception for testing purposes."""

    mock_socket = MockSocket(socket_module.AF_INET, socket_module.SOCK_STREAM)
    try:  # pylint: disable=too-many-try-statements
        with PearyClient("", proxy_class=MockProxy):
            raise MockError  # noqa: TRY301
    except MockError:
        assert mock_socket.is_connected is False
        assert mock_socket.is_shutdown is True
        assert mock_socket.how_shutdown == socket_module.SHUT_RDWR
