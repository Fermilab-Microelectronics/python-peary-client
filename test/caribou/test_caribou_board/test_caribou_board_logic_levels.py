from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from collections.abc import Callable


def test_caribou_board_set_logic_level(mock_caribou_board: Callable) -> None:
    caribou_board = mock_caribou_board(0)
    caribou_board.set_logic_level(1.2)
    assert caribou_board.transactions[-2:] == [
        "device.setInputCMOSLevel 0 1.2",
        "device.setOutputCMOSLevel 0 1.2",
    ]
