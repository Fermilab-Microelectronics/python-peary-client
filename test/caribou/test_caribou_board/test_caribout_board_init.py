from __future__ import annotations

import socket
from typing import TYPE_CHECKING

import pytest

from caribou.caribou_board import CaribouBoard
from peary.peary_protocol import PearyProtocol

if TYPE_CHECKING:
    # ruff: noqa: ANN401
    from collections.abc import Callable
    from typing import Any


class MockProtocol(PearyProtocol):
    """A Mock Peary Protocol."""

    def request(
        self, msg: str, *args: str, buffer_size: int = 4096  # noqa: ARG002
    ) -> bytes:
        return " ".join([msg, *args]).encode("utf-8")

    def _verify_compatible_version(self) -> None:
        pass


@pytest.fixture(name="caribou_board")
def _caribou_board() -> Callable:

    def _initialize_caribou_board(index: int) -> CaribouBoard:
        return CaribouBoard(index, socket.socket(), MockProtocol)

    return _initialize_caribou_board


def test_caribou_board_init_index(caribou_board: Callable) -> None:
    assert caribou_board(0).index == 0
    assert caribou_board(1).index == 1


def test_caribou_board_init_name(caribou_board: Callable) -> None:
    assert caribou_board(0).name == "device.name 0"
    assert caribou_board(1).name == "device.name 1"


def test_caribou_board_init_repr(caribou_board: Callable) -> None:
    assert str(caribou_board(0)) == "device.name 0(0)"
    assert str(caribou_board(1)) == "device.name 1(1)"


def test_caribou_board_init_enable_power_supplies(
    monkeypatch: pytest.MonkeyPatch, caribou_board: Callable
) -> None:
    transactions = []

    def mock_write_i2c(*args: Any) -> None:
        nonlocal transactions
        transactions.append(" ".join([str(_) for _ in args]))

    monkeypatch.setattr(CaribouBoard, "write_i2c", mock_write_i2c)
    caribou_board(0)
    assert transactions == [
        "device.name 0(0) BusI2C.BUS_0 118 6 0",
        "device.name 0(0) BusI2C.BUS_0 118 7 0",
    ]
