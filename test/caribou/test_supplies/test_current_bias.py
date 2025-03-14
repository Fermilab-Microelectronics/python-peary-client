from __future__ import annotations

from typing import TYPE_CHECKING

from caribou.current_bias import CurrentBias

if TYPE_CHECKING:
    from collections.abc import Callable


def test_current_bias_name(mock_device: Callable) -> None:
    assert CurrentBias("alpha", mock_device()).name == "alpha"
    assert CurrentBias("beta", mock_device()).name == "beta"


def test_current_bias_device(mock_device: Callable) -> None:
    assert CurrentBias("", device := mock_device()).device is device
    assert CurrentBias("", device := mock_device()).device is device


def test_current_bias_get_current(mock_device: Callable) -> None:
    for index, name, value in zip([0, 1], ["alpha", "beta"], [b"1.0", b"2.0"]):
        assert CurrentBias(
            name,
            mock_device(
                index=index, req=f"device.get_current {index} {name}", resp=value
            ),
        ).get_current() == float(value)


def test_current_bias_set_current(mock_device: Callable) -> None:
    for index, name, value in zip([0, 1], ["alpha", "beta"], [1.0, 2.0]):
        assert (
            CurrentBias(
                name,
                mock_device(
                    index=index, req=f"device.set_current {index} {name} {value}"
                ),
            ).set_current(float(value))
            == b""
        )


def test_current_bias_switch_on(mock_device: Callable) -> None:
    for index, name in zip([0, 1], ["alpha", "beta"]):
        assert (
            CurrentBias(
                name, mock_device(index=index, req=f"device.switch_on {index} {name}")
            ).switch_on()
            == b""
        )


def test_current_bias_switch_off(mock_device: Callable) -> None:
    for index, name in zip([0, 1], ["alpha", "beta"]):
        assert (
            CurrentBias(
                name, mock_device(index=index, req=f"device.switch_off {index} {name}")
            ).switch_off()
            == b""
        )
