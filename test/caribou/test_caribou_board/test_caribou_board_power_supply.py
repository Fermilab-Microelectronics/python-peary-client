from __future__ import annotations

import socket

from caribou.caribou_board import CaribouBoard
from caribou.power_supply import PowerSupply
from peary.peary_protocol import PearyProtocol


class MockProtocol(PearyProtocol):
    """A Mock Peary Protocol."""

    def request(
        self, msg: str, *args: str, buffer_size: int = 4096  # noqa: ARG002
    ) -> bytes:
        return " ".join([msg, *args]).encode("utf-8")

    def _verify_compatible_version(self) -> None:
        pass


def test_caribou_board_power_supply_constants() -> None:
    assert CaribouBoard.PWR_OUT_1.value == "PWR_OUT_1"
    assert CaribouBoard.PWR_OUT_2.value == "PWR_OUT_2"
    assert CaribouBoard.PWR_OUT_3.value == "PWR_OUT_3"
    assert CaribouBoard.PWR_OUT_4.value == "PWR_OUT_4"
    assert CaribouBoard.PWR_OUT_5.value == "PWR_OUT_5"
    assert CaribouBoard.PWR_OUT_6.value == "PWR_OUT_6"
    assert CaribouBoard.PWR_OUT_7.value == "PWR_OUT_7"
    assert CaribouBoard.PWR_OUT_8.value == "PWR_OUT_8"


def test_caribou_board_power_supply_type() -> None:
    caribou_board = CaribouBoard(0, socket.socket(), MockProtocol)
    assert isinstance(caribou_board.power_supply(CaribouBoard.PWR_OUT_1), PowerSupply)
    assert isinstance(caribou_board.power_supply(CaribouBoard.PWR_OUT_2), PowerSupply)
    assert isinstance(caribou_board.power_supply(CaribouBoard.PWR_OUT_3), PowerSupply)
    assert isinstance(caribou_board.power_supply(CaribouBoard.PWR_OUT_4), PowerSupply)
    assert isinstance(caribou_board.power_supply(CaribouBoard.PWR_OUT_5), PowerSupply)
    assert isinstance(caribou_board.power_supply(CaribouBoard.PWR_OUT_6), PowerSupply)
    assert isinstance(caribou_board.power_supply(CaribouBoard.PWR_OUT_7), PowerSupply)
    assert isinstance(caribou_board.power_supply(CaribouBoard.PWR_OUT_8), PowerSupply)


def test_caribou_board_power_supply_names() -> None:
    caribou_board = CaribouBoard(0, socket.socket(), MockProtocol)
    assert caribou_board.power_supply(CaribouBoard.PWR_OUT_1).name == "PWR_OUT_1"
    assert caribou_board.power_supply(CaribouBoard.PWR_OUT_2).name == "PWR_OUT_2"
    assert caribou_board.power_supply(CaribouBoard.PWR_OUT_3).name == "PWR_OUT_3"
    assert caribou_board.power_supply(CaribouBoard.PWR_OUT_4).name == "PWR_OUT_4"
    assert caribou_board.power_supply(CaribouBoard.PWR_OUT_5).name == "PWR_OUT_5"
    assert caribou_board.power_supply(CaribouBoard.PWR_OUT_6).name == "PWR_OUT_6"
    assert caribou_board.power_supply(CaribouBoard.PWR_OUT_7).name == "PWR_OUT_7"
    assert caribou_board.power_supply(CaribouBoard.PWR_OUT_8).name == "PWR_OUT_8"


def test_caribou_board_power_supply_devices() -> None:
    caribou_board = CaribouBoard(0, socket.socket(), MockProtocol)
    assert caribou_board.power_supply(CaribouBoard.PWR_OUT_1).device is caribou_board
    assert caribou_board.power_supply(CaribouBoard.PWR_OUT_2).device is caribou_board
    assert caribou_board.power_supply(CaribouBoard.PWR_OUT_3).device is caribou_board
    assert caribou_board.power_supply(CaribouBoard.PWR_OUT_4).device is caribou_board
    assert caribou_board.power_supply(CaribouBoard.PWR_OUT_5).device is caribou_board
    assert caribou_board.power_supply(CaribouBoard.PWR_OUT_6).device is caribou_board
    assert caribou_board.power_supply(CaribouBoard.PWR_OUT_7).device is caribou_board
    assert caribou_board.power_supply(CaribouBoard.PWR_OUT_8).device is caribou_board
