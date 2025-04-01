from __future__ import annotations

import socket
from typing import TYPE_CHECKING

import pytest

from peary.peary_device import PearyDevice
from peary.peary_protocol import PearyProtocol

if TYPE_CHECKING:
    from collections.abc import Callable


@pytest.fixture(name="mock_device")
def _mock_device() -> Callable:

    def _mock_device(index: int = 0, req: str = "", resp: bytes = b"") -> PearyDevice:

        class MockProtocol(PearyProtocol):
            """A Mock Peary Protocol."""

            def request(
                self, msg: str, *args: str, buffer_size: int = 4096  # noqa: ARG002
            ) -> bytes:
                assert " ".join([msg, *args]) == req
                return resp

        return PearyDevice(
            index, MockProtocol(socket.socket(), checks=PearyProtocol.Checks.CHECK_NONE)
        )

    return _mock_device
