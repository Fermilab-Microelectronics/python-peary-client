from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from collections.abc import Callable


def test_peary_device_repr(device: Callable) -> None:
    assert str(device(0)) == "device.name 0(0)"
    assert str(device(1)) == "device.name 1(1)"
