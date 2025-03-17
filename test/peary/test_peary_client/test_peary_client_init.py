from __future__ import annotations

import socket as socket_module

from peary.peary_client import PearyClient
from peary.peary_proxy import PearyProxy

# TODO(Jeff): Rewrite tests using derived classes instead of monkey patching everything.


def test_peary_client_init_host() -> None:
    assert PearyClient("alpha").host == "alpha"
    assert PearyClient("beta").host == "beta"


def test_peary_client_init_port() -> None:
    assert PearyClient("").port == 12345
    assert PearyClient("", 0).port == 0
    assert PearyClient("", 1).port == 1


def test_peary_client_init_proxy_class() -> None:
    class MockProxy(PearyProxy):
        """Mock proxy class."""

    assert PearyClient("").proxy_class is PearyProxy
    assert PearyClient("", proxy_class=PearyProxy).proxy_class is PearyProxy
    assert PearyClient("", proxy_class=MockProxy).proxy_class is MockProxy


def test_peary_client_init_socket_class() -> None:
    class MockSocket(socket_module.socket):
        """Mock socket class."""

    assert PearyClient("").socket_class is socket_module.socket
    assert (
        PearyClient("", socket_class=socket_module.socket).socket_class
        is socket_module.socket
    )
    assert PearyClient("", socket_class=MockSocket).socket_class is MockSocket


def test_peary_client_init_socket() -> None:
    class MockSocket(socket_module.socket):
        """Mock socket class."""

    assert isinstance(PearyClient("").socket, socket_module.socket)
    assert isinstance(
        PearyClient("", socket_class=socket_module.socket).socket, socket_module.socket
    )
    assert isinstance(
        PearyClient("", socket_class=MockSocket).socket, socket_module.socket
    )
    assert PearyClient("").socket.family == socket_module.AF_INET
    assert PearyClient("").socket.type == socket_module.SOCK_STREAM
