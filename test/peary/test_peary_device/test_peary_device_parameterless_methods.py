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

    def _verify_compatible_version(self) -> None:
        pass


@pytest.fixture(name="device")
def _device() -> Callable:

    def _initialize_device(index: int) -> PearyDevice:
        return PearyDevice(index, socket.socket(), MockPearyProtocol)

    return _initialize_device


def test_peary_device_power_on(device: Callable) -> None:
    assert device(0).power_on() == b"device.power_on 0"
    assert device(1).power_on() == b"device.power_on 1"


def test_peary_device_power_off(device: Callable) -> None:
    assert device(0).power_off() == b"device.power_off 0"
    assert device(1).power_off() == b"device.power_off 1"


def test_peary_device_reset(device: Callable) -> None:
    assert device(0).reset() == b"device.reset 0"
    assert device(1).reset() == b"device.reset 1"


def test_peary_device_configure(device: Callable) -> None:
    assert device(0).configure() == b"device.configure 0"
    assert device(1).configure() == b"device.configure 1"


def test_peary_device_daq_start(device: Callable) -> None:
    assert device(0).daq_start() == b"device.daq_start 0"
    assert device(1).daq_start() == b"device.daq_start 1"


def test_peary_device_daq_stop(device: Callable) -> None:
    assert device(0).daq_stop() == b"device.daq_stop 0"
    assert device(1).daq_stop() == b"device.daq_stop 1"


def test_peary_device_list_registers(device: Callable) -> None:
    assert (
        device(0).list_registers() == b"device.list_registers 0".decode("utf-8").split()
    )
    assert (
        device(1).list_registers() == b"device.list_registers 1".decode("utf-8").split()
    )
