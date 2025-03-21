from __future__ import annotations

import socket
from typing import TYPE_CHECKING

import pytest

from peary.peary_device import PearyDevice
from peary.peary_protocol import PearyProtocol

if TYPE_CHECKING:
    from collections.abc import Callable


class MockPearyProtocol(PearyProtocol):
    """A Mock Peary Protocol."""

    def request(
        self, msg: str, *args: str, buffer_size: int = 4096  # noqa: ARG002
    ) -> bytes:
        return " ".join([msg, *args]).encode("utf-8")


@pytest.fixture(name="device")
def _device() -> Callable:

    def _initialize_device(index: int) -> PearyDevice:
        return PearyDevice(
            index,
            MockPearyProtocol(socket.socket(), checks=PearyProtocol.Checks.CHECK_NONE),
        )

    return _initialize_device
