from __future__ import annotations

from typing import TYPE_CHECKING

from caribou.voltage_bias import VoltageBias

if TYPE_CHECKING:
    from collections.abc import Callable


def test_voltage_bias_name(mock_device: Callable) -> None:
    assert VoltageBias("alpha", mock_device()).name == "alpha"
    assert VoltageBias("beta", mock_device()).name == "beta"


def test_voltage_bias_device(mock_device: Callable) -> None:
    assert VoltageBias("", device := mock_device()).device is device
    assert VoltageBias("", device := mock_device()).device is device


def test_voltage_bias_get_voltage(mock_device: Callable) -> None:
    for index, name, value in zip([0, 1], ["alpha", "beta"], [b"1.0", b"2.0"]):
        assert VoltageBias(
            name,
            mock_device(
                index=index, req=f"device.get_voltage {index} {name}", resp=value
            ),
        ).get_voltage() == float(value)


def test_voltage_bias_set_voltage(mock_device: Callable) -> None:
    for index, name, value in zip([0, 1], ["alpha", "beta"], [1.0, 2.0]):
        assert (
            VoltageBias(
                name,
                mock_device(
                    index=index, req=f"device.set_voltage {index} {name} {value}"
                ),
            ).set_voltage(float(value))
            == b""
        )


def test_voltage_bias_switch_on(mock_device: Callable) -> None:
    for index, name in zip([0, 1], ["alpha", "beta"]):
        assert (
            VoltageBias(
                name, mock_device(index=index, req=f"device.switch_on {index} {name}")
            ).switch_on()
            == b""
        )


def test_voltage_bias_switch_off(mock_device: Callable) -> None:
    for index, name in zip([0, 1], ["alpha", "beta"]):
        assert (
            VoltageBias(
                name, mock_device(index=index, req=f"device.switch_off {index} {name}")
            ).switch_off()
            == b""
        )
