from __future__ import annotations

import socket

from caribou.caribou_board import CaribouBoard
from caribou.voltage_bias import VoltageBias
from peary.peary_protocol import PearyProtocol


class MockProtocol(PearyProtocol):
    """A Mock Peary Protocol."""

    def request(
        self, msg: str, *args: str, buffer_size: int = 4096  # noqa: ARG002
    ) -> bytes:
        return " ".join([msg, *args]).encode("utf-8")

    def _verify_compatible_version(self) -> None:
        pass


def test_caribou_board_voltage_bias_constants() -> None:
    assert CaribouBoard.VBIAS_1.value == "BIAS_1"
    assert CaribouBoard.VBIAS_2.value == "BIAS_2"
    assert CaribouBoard.VBIAS_3.value == "BIAS_3"
    assert CaribouBoard.VBIAS_4.value == "BIAS_4"
    assert CaribouBoard.VBIAS_5.value == "BIAS_5"


def test_caribou_board_voltage_bias_type() -> None:
    caribou_board = CaribouBoard(0, socket.socket(), MockProtocol)
    assert isinstance(caribou_board.voltage_bias(CaribouBoard.VBIAS_1), VoltageBias)
    assert isinstance(caribou_board.voltage_bias(CaribouBoard.VBIAS_2), VoltageBias)
    assert isinstance(caribou_board.voltage_bias(CaribouBoard.VBIAS_3), VoltageBias)
    assert isinstance(caribou_board.voltage_bias(CaribouBoard.VBIAS_4), VoltageBias)
    assert isinstance(caribou_board.voltage_bias(CaribouBoard.VBIAS_5), VoltageBias)


def test_caribou_board_voltage_bias_names() -> None:
    caribou_board = CaribouBoard(0, socket.socket(), MockProtocol)
    assert caribou_board.voltage_bias(CaribouBoard.VBIAS_1).name == "BIAS_1"
    assert caribou_board.voltage_bias(CaribouBoard.VBIAS_2).name == "BIAS_2"
    assert caribou_board.voltage_bias(CaribouBoard.VBIAS_3).name == "BIAS_3"
    assert caribou_board.voltage_bias(CaribouBoard.VBIAS_4).name == "BIAS_4"
    assert caribou_board.voltage_bias(CaribouBoard.VBIAS_5).name == "BIAS_5"


def test_caribou_board_voltage_bias_devices() -> None:
    caribou_board = CaribouBoard(0, socket.socket(), MockProtocol)
    assert caribou_board.voltage_bias(CaribouBoard.VBIAS_1).device is caribou_board
    assert caribou_board.voltage_bias(CaribouBoard.VBIAS_2).device is caribou_board
    assert caribou_board.voltage_bias(CaribouBoard.VBIAS_3).device is caribou_board
    assert caribou_board.voltage_bias(CaribouBoard.VBIAS_4).device is caribou_board
    assert caribou_board.voltage_bias(CaribouBoard.VBIAS_5).device is caribou_board
