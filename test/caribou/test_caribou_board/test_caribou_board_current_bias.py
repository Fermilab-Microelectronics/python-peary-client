from __future__ import annotations

from typing import TYPE_CHECKING

from caribou.caribou_board import CaribouBoard
from caribou.current_bias import CurrentBias

if TYPE_CHECKING:
    from collections.abc import Callable


def test_caribou_board_current_bias_constants() -> None:
    assert CaribouBoard.IBIAS_1.value == "CUR_1"
    assert CaribouBoard.IBIAS_2.value == "CUR_2"
    assert CaribouBoard.IBIAS_3.value == "CUR_3"
    assert CaribouBoard.IBIAS_4.value == "CUR_4"
    assert CaribouBoard.IBIAS_5.value == "CUR_5"
    assert CaribouBoard.IBIAS_6.value == "CUR_6"
    assert CaribouBoard.IBIAS_7.value == "CUR_7"
    assert CaribouBoard.IBIAS_8.value == "CUR_8"


def test_caribou_board_current_bias_type(mock_caribou_board: Callable) -> None:
    caribou_board = mock_caribou_board(0)
    assert isinstance(caribou_board.current_bias(CaribouBoard.IBIAS_1), CurrentBias)
    assert isinstance(caribou_board.current_bias(CaribouBoard.IBIAS_2), CurrentBias)
    assert isinstance(caribou_board.current_bias(CaribouBoard.IBIAS_3), CurrentBias)
    assert isinstance(caribou_board.current_bias(CaribouBoard.IBIAS_4), CurrentBias)
    assert isinstance(caribou_board.current_bias(CaribouBoard.IBIAS_5), CurrentBias)
    assert isinstance(caribou_board.current_bias(CaribouBoard.IBIAS_6), CurrentBias)
    assert isinstance(caribou_board.current_bias(CaribouBoard.IBIAS_7), CurrentBias)
    assert isinstance(caribou_board.current_bias(CaribouBoard.IBIAS_8), CurrentBias)


def test_caribou_board_current_bias_names(mock_caribou_board: Callable) -> None:
    caribou_board = mock_caribou_board(0)
    assert caribou_board.current_bias(CaribouBoard.IBIAS_1).name == "CUR_1"
    assert caribou_board.current_bias(CaribouBoard.IBIAS_2).name == "CUR_2"
    assert caribou_board.current_bias(CaribouBoard.IBIAS_3).name == "CUR_3"
    assert caribou_board.current_bias(CaribouBoard.IBIAS_4).name == "CUR_4"
    assert caribou_board.current_bias(CaribouBoard.IBIAS_5).name == "CUR_5"
    assert caribou_board.current_bias(CaribouBoard.IBIAS_6).name == "CUR_6"
    assert caribou_board.current_bias(CaribouBoard.IBIAS_7).name == "CUR_7"
    assert caribou_board.current_bias(CaribouBoard.IBIAS_8).name == "CUR_8"


def test_caribou_board_current_bias_devices(mock_caribou_board: Callable) -> None:
    caribou_board = mock_caribou_board(0)
    assert caribou_board.current_bias(CaribouBoard.IBIAS_1).device is caribou_board
    assert caribou_board.current_bias(CaribouBoard.IBIAS_2).device is caribou_board
    assert caribou_board.current_bias(CaribouBoard.IBIAS_3).device is caribou_board
    assert caribou_board.current_bias(CaribouBoard.IBIAS_4).device is caribou_board
    assert caribou_board.current_bias(CaribouBoard.IBIAS_5).device is caribou_board
    assert caribou_board.current_bias(CaribouBoard.IBIAS_6).device is caribou_board
    assert caribou_board.current_bias(CaribouBoard.IBIAS_7).device is caribou_board
    assert caribou_board.current_bias(CaribouBoard.IBIAS_8).device is caribou_board
