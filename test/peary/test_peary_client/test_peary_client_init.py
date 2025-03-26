from __future__ import annotations

import socket as socket_module

from peary.peary_client import PearyClient


def test_peary_client_init_socket_class() -> None:
    class MockSocket(socket_module.socket):
        """Mock socket class."""

    assert isinstance(PearyClient("").socket, socket_module.socket)
    assert isinstance(
        PearyClient("", socket_class=socket_module.socket).socket, socket_module.socket
    )
    assert isinstance(PearyClient("", socket_class=MockSocket).socket, MockSocket)


def test_peary_client_init_socket_config() -> None:
    assert PearyClient("").socket.family == socket_module.AF_INET
    assert PearyClient("").socket.type == socket_module.SOCK_STREAM
