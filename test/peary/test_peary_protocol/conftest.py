from __future__ import annotations

import socket as socket_module
from typing import TYPE_CHECKING

import pytest

if TYPE_CHECKING:
    from typing_extensions import Buffer


class MockSocket(socket_module.socket):
    timeout = None

    # pylint: disable-next=W0613
    def recv(self, size: int, flags: int = 0) -> bytes:  # noqa: ARG002
        return b""

    # pylint: disable-next=W0613
    def send(self, data: Buffer, flags: int = 0) -> int:  # noqa: ARG002
        return len(bytes(data))

    def settimeout(self, value: float | None = None) -> None:
        MockSocket.timeout = value


@pytest.fixture(name="mock_socket")
def _mock_socket() -> type[socket_module.socket]:
    return MockSocket
