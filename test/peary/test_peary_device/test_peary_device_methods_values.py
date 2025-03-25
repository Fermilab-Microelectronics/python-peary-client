from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from collections.abc import Callable


def test_peary_device_list_registers(mock_device: Callable) -> None:
    assert mock_device(
        index=0, req="device.list_registers 0", resp=b"alpha"
    ).list_registers() == ["alpha"]
    assert mock_device(
        index=1, req="device.list_registers 1", resp=b"alpha beta gamma"
    ).list_registers() == ["alpha", "beta", "gamma"]


def test_peary_device_get_register(mock_device: Callable) -> None:
    for index, name, value in zip([0, 1], ["alpha", "beta"], [b"0", b"1"]):
        assert mock_device(
            index=index, req=f"device.get_register {index} {name}", resp=value
        ).get_register(name) == int(value)


def test_peary_device_set_register(mock_device: Callable) -> None:
    for index, name, value in zip([0, 1], ["alpha", "beta"], [0, 1]):
        assert mock_device(index).set_register(
            name, value
        ) == f"device.set_register {index} {name} {value}".encode("utf-8")


def test_peary_device_get_memory(mock_device: Callable) -> None:
    for index, name, value in zip([0, 1], ["alpha", "beta"], [b"0", b"1"]):
        assert mock_device(
            index=index, req=f"device.get_memory {index} {name}", resp=value
        ).get_memory(name) == int(value)


def test_peary_device_set_memory(mock_device: Callable) -> None:
    for index, name, value in zip([0, 1], ["alpha", "beta"], [0, 1]):
        assert mock_device(index).set_memory(
            name, value
        ) == f"device.set_memory {index} {name} {value}".encode("utf-8")


def test_peary_device_get_current(mock_device: Callable) -> None:
    for index, name, value in zip([0, 1], ["alpha", "beta"], [b"1.0", b"2.0"]):
        assert mock_device(
            index=index, req=f"device.get_current {index} {name}", resp=value
        ).get_current(name) == float(value)


def test_peary_device_set_current(mock_device: Callable) -> None:
    for index, name, value in zip([0, 1], ["alpha", "beta"], [1.0, 2.0]):
        assert mock_device(index).set_current(
            name, value
        ) == f"device.set_current {index} {name} {value}".encode("utf-8")


def test_peary_device_get_voltage(mock_device: Callable) -> None:
    for index, name, value in zip([0, 1], ["alpha", "beta"], [b"1.0", b"2.0"]):
        assert mock_device(
            index=index, req=f"device.get_voltage {index} {name}", resp=value
        ).get_voltage(name) == float(value)


def test_peary_device_set_voltage(mock_device: Callable) -> None:
    for index, name, value in zip([0, 1], ["alpha", "beta"], [1.0, 2.0]):
        assert mock_device(index).set_voltage(
            name, value
        ) == f"device.set_voltage {index} {name} {value}".encode("utf-8")
