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


def test_peary_device_init_index() -> None:
    assert PearyDevice(0, socket.socket(), MockPearyProtocol).index == 0
    assert PearyDevice(1, socket.socket(), MockPearyProtocol).index == 1


def test_peary_device_init_name() -> None:
    assert PearyDevice(0, socket.socket(), MockPearyProtocol).name == "device.name 0"
    assert PearyDevice(1, socket.socket(), MockPearyProtocol).name == "device.name 1"
