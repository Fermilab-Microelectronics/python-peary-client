from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from collections.abc import Callable


def test_peary_device_init_index(device: Callable) -> None:
    assert device(0).index == 0
    assert device(1).index == 1


def test_peary_device_init_name(device: Callable) -> None:
    assert device(0).name == "device.name 0"
    assert device(1).name == "device.name 1"
