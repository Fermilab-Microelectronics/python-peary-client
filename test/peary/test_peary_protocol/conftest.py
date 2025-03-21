from __future__ import annotations

import select
import socket as socket_module
from contextlib import contextmanager
from typing import TYPE_CHECKING, cast

import pytest

from peary.peary_protocol import PearyProtocol

if TYPE_CHECKING:
    from collections.abc import Callable, Generator
    from socket import socket as socket_type

    from typing_extensions import Buffer


class MockSocketInterface(socket_module.socket):
    timeout: float | None = None


@pytest.fixture(name="patch_socket")
def _patch_socket(monkeypatch: pytest.MonkeyPatch) -> Callable:

    @contextmanager
    def _patch_socket_context(
        # pylint: disable-next=unnecessary-lambda
        mock_send: Callable[[bytes], int] = lambda _: len(_),
        mock_recv: Callable[[int], bytes] = lambda _: PearyProtocol.encode(
            b"", 1, PearyProtocol.STATUS_OK
        ),
        mock_select: Callable[
            [list[socket_type]], tuple[list, list, list]
        ] = lambda *_: ([], [], []),
    ) -> Generator[type[MockSocketInterface]]:

        class MockSocket(MockSocketInterface):

            # pylint: disable-next=W0613
            def send(self, data: Buffer, flags: int = 0) -> int:  # noqa: ARG002
                return mock_send(cast("bytes", data))

            # pylint: disable-next=W0613
            def recv(self, size: int, flags: int = 0) -> bytes:  # noqa: ARG002
                return mock_recv(size)

            def settimeout(self, value: float | None = None) -> None:
                MockSocket.timeout = value

        with monkeypatch.context() as m:
            m.setattr(select, "select", mock_select)
            yield MockSocket

    return _patch_socket_context
