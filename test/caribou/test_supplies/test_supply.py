from __future__ import annotations

from typing import TYPE_CHECKING

from caribou.supply import Supply

if TYPE_CHECKING:
    from collections.abc import Callable


def test_supply_name(mock_device: Callable) -> None:
    assert Supply("alpha", mock_device(0)).name == "alpha"
    assert Supply("beta", mock_device(0)).name == "beta"


def test_supply_device(mock_device: Callable) -> None:
    assert Supply("", device := mock_device(0)).device is device
    assert Supply("", device := mock_device(1)).device is device
