from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from collections.abc import Callable


def test_peary_device_name(mock_device: Callable) -> None:
    assert mock_device(0).name == "device.name 0"
    assert mock_device(1).name == "device.name 1"


def test_peary_device_repr(mock_device: Callable) -> None:
    assert str(mock_device(0)) == "device.name 0(0)"
    assert str(mock_device(1)) == "device.name 1(1)"
