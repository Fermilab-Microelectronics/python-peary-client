from __future__ import annotations

import socket
from typing import TYPE_CHECKING

import pytest

from caribou.supply import Supply
from peary.peary_device import PearyDevice
from peary.peary_protocol import PearyProtocol

if TYPE_CHECKING:
    from collections.abc import Callable


class MockDevice(PearyDevice):
    """A Mock Peary Protocol."""

    def _request_name(self) -> str:
        return ""


class MockProtocol(PearyProtocol):
    """A Mock Peary Protocol."""

    def _verify_compatible_version(self) -> None:
        pass


@pytest.fixture(name="mock_device")
def _mock_device() -> Callable:

    def _mock_device_factory(index: int) -> MockDevice:
        return MockDevice(index, socket.socket(), MockProtocol)

    return _mock_device_factory


def test_supply_name(mock_device: Callable) -> None:
    assert Supply("alpha", mock_device(0)).name == "alpha"
    assert Supply("beta", mock_device(0)).name == "beta"


def test_supply_device(mock_device: Callable) -> None:
    assert Supply("", device := mock_device(0)).device is device
    assert Supply("", device := mock_device(1)).device is device
