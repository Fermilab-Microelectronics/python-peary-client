from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from collections.abc import Callable


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
