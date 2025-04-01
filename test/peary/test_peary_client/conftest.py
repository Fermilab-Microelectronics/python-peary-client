from __future__ import annotations

import socket as socket_module
from typing import TYPE_CHECKING, cast

import pytest

from peary.peary_protocol import PearyProtocol

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


@pytest.fixture(name="mock_socket_class")
def _mock_socket_class() -> type[MockSocket]:
    return MockSocket
