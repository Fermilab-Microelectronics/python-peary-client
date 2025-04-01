from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from collections.abc import Callable


def test_caribou_board_init_index(mock_caribou_board: Callable) -> None:
    assert mock_caribou_board(0).index == 0
    assert mock_caribou_board(1).index == 1


def test_caribou_board_init_name(mock_caribou_board: Callable) -> None:
    assert mock_caribou_board(0).name == "device.name 0"
    assert mock_caribou_board(1).name == "device.name 1"


def test_caribou_board_init_repr(mock_caribou_board: Callable) -> None:
    assert str(mock_caribou_board(0)) == "device.name 0(0)"
    assert str(mock_caribou_board(1)) == "device.name 1(1)"


def test_caribou_board_init_enable_power_supplies(mock_caribou_board: Callable) -> None:
    caribou_board = mock_caribou_board(0)
    assert caribou_board.transactions[-2:] == [
        "device.car_i2c_write 0 0 118 6 0",
        "device.car_i2c_write 0 0 118 7 0",
    ]
