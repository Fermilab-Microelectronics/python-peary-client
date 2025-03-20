from __future__ import annotations

import socket as socket_module
from typing import TYPE_CHECKING, cast

import pytest

from peary.peary_protocol import PearyProtocol

if TYPE_CHECKING:
    from collections.abc import Callable

    from typing_extensions import Buffer


class MockSocketInterface(socket_module.socket):
    timeout: float | None = None


@pytest.fixture(name="mock_socket")
def _mock_socket() -> Callable:

    def _patched_mock_socket(
        # pylint: disable-next=unnecessary-lambda
        mock_send: Callable[[bytes], int] = lambda _: len(_),
        mock_recv: Callable[[int], bytes] = lambda _: PearyProtocol.encode(
            b"", 1, PearyProtocol.STATUS_OK
        ),
    ) -> type[MockSocketInterface]:

        class MockSocket(MockSocketInterface):

            # pylint: disable-next=W0613
            def send(self, data: Buffer, flags: int = 0) -> int:  # noqa: ARG002
                return mock_send(cast("bytes", data))

            # pylint: disable-next=W0613
            def recv(self, size: int, flags: int = 0) -> bytes:  # noqa: ARG002
                return mock_recv(size)

            def settimeout(self, value: float | None = None) -> None:
                MockSocket.timeout = value

        return MockSocket

    return _patched_mock_socket
