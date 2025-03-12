from __future__ import annotations

import socket

from peary.peary_device import PearyDevice
from peary.peary_protocol import PearyProtocol


class MockPearyProtocol(PearyProtocol):
    """A Mock Peary Protocol."""

    def request(
        self, msg: str, *args: str, buffer_size: int = 4096  # noqa: ARG002
    ) -> bytes:
        return " ".join([msg, *args]).encode("utf-8")

    def _verify_compatible_version(self) -> None:
        pass


def test_peary_device_repr() -> None:
    assert str(PearyDevice(0, socket.socket(), MockPearyProtocol)) == "device.name 0(0)"
    assert str(PearyDevice(1, socket.socket(), MockPearyProtocol)) == "device.name 1(1)"
