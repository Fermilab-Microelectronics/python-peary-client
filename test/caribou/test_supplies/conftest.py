from __future__ import annotations

import socket
from typing import TYPE_CHECKING

import pytest

from peary.peary_device import PearyDevice
from peary.peary_protocol import PearyProtocol

if TYPE_CHECKING:
    from collections.abc import Callable


class MockDevice(PearyDevice):
    """A Mock Peary Protocol."""

    def _request_name(self) -> str:
        return ""


@pytest.fixture(name="mock_device")
def _mock_device() -> Callable:

    def _mock_device(index: int = 0, req: str = "", resp: bytes = b"") -> MockDevice:

        class MockProtocol(PearyProtocol):
            """A Mock Peary Protocol."""

            def request(
                self, msg: str, *args: str, buffer_size: int = 4096  # noqa: ARG002
            ) -> bytes:
                assert " ".join([msg, *args]) == req
                return resp

            def _verify_compatible_version(self) -> None:
                pass

        return MockDevice(index, socket.socket(), MockProtocol)

    return _mock_device
