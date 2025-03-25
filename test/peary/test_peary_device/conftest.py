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
    def _customize_mock_device_request(
        index: int, *, req: str | None = None, resp: bytes | None = None
    ) -> PearyDevice:

        class MockPearyProtocol(PearyProtocol):
            """A Mock Peary Protocol."""

            def request(
                self, msg: str, *args: str, buffer_size: int = 4096  # noqa: ARG002
            ) -> bytes:
                if req:
                    assert " ".join([msg, *args]) == req
                if resp:
                    return resp
                else:
                    return " ".join([msg, *args]).encode("utf-8")

        return PearyDevice(
            index,
            MockPearyProtocol(socket.socket(), checks=PearyProtocol.Checks.CHECK_NONE),
        )

    return _customize_mock_device_request
