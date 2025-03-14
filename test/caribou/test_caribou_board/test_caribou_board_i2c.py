from __future__ import annotations

import socket
from typing import TYPE_CHECKING

from caribou.caribou_board import CaribouBoard
from peary.peary_protocol import PearyProtocol

if TYPE_CHECKING:
    import pytest


class MockProtocol(PearyProtocol):
    """A Mock Peary Protocol."""

    def _verify_compatible_version(self) -> None:
        pass


def test_caribou_board_current_bias_constants() -> None:
    assert CaribouBoard.BusI2C.BUS_0.value == 0
    assert CaribouBoard.BusI2C.BUS_1.value == 1
    assert CaribouBoard.BusI2C.BUS_2.value == 2
    assert CaribouBoard.BusI2C.BUS_3.value == 3


def test_peary_device_write_i2c_bus(monkeypatch: pytest.MonkeyPatch) -> None:
    def mock_request(_: type, *args: str) -> bytes:
        return " ".join(args).encode("utf-8")

    monkeypatch.setattr(MockProtocol, "request", mock_request)
    assert (
        CaribouBoard(0, socket.socket(), MockProtocol).write_i2c(
            CaribouBoard.BusI2C.BUS_0, 0, 0, 0
        )
        == b"device.car_i2c_write 0 0 0 0 0"
    )
    assert (
        CaribouBoard(0, socket.socket(), MockProtocol).write_i2c(
            CaribouBoard.BusI2C.BUS_1, 0, 0, 0
        )
        == b"device.car_i2c_write 0 1 0 0 0"
    )


def test_peary_device_write_i2c_component(monkeypatch: pytest.MonkeyPatch) -> None:
    def mock_request(_: type, *args: str) -> bytes:
        return " ".join(args).encode("utf-8")

    monkeypatch.setattr(MockProtocol, "request", mock_request)
    assert (
        CaribouBoard(0, socket.socket(), MockProtocol).write_i2c(
            CaribouBoard.BusI2C.BUS_0, 0, 0, 0
        )
        == b"device.car_i2c_write 0 0 0 0 0"
    )
    assert (
        CaribouBoard(0, socket.socket(), MockProtocol).write_i2c(
            CaribouBoard.BusI2C.BUS_0, 1, 0, 0
        )
        == b"device.car_i2c_write 0 0 1 0 0"
    )


def test_peary_device_write_i2c_address(monkeypatch: pytest.MonkeyPatch) -> None:
    def mock_request(_: type, *args: str) -> bytes:
        return " ".join(args).encode("utf-8")

    monkeypatch.setattr(MockProtocol, "request", mock_request)
    assert (
        CaribouBoard(0, socket.socket(), MockProtocol).write_i2c(
            CaribouBoard.BusI2C.BUS_0, 0, 0, 0
        )
        == b"device.car_i2c_write 0 0 0 0 0"
    )
    assert (
        CaribouBoard(0, socket.socket(), MockProtocol).write_i2c(
            CaribouBoard.BusI2C.BUS_0, 0, 1, 0
        )
        == b"device.car_i2c_write 0 0 0 1 0"
    )


def test_peary_device_write_i2c_data(monkeypatch: pytest.MonkeyPatch) -> None:
    def mock_request(_: type, *args: str) -> bytes:
        return " ".join(args).encode("utf-8")

    monkeypatch.setattr(MockProtocol, "request", mock_request)
    assert (
        CaribouBoard(0, socket.socket(), MockProtocol).write_i2c(
            CaribouBoard.BusI2C.BUS_0, 0, 0, 0
        )
        == b"device.car_i2c_write 0 0 0 0 0"
    )
    assert (
        CaribouBoard(0, socket.socket(), MockProtocol).write_i2c(
            CaribouBoard.BusI2C.BUS_0, 0, 0, 1
        )
        == b"device.car_i2c_write 0 0 0 0 1"
    )


def test_peary_device_read_i2c_bus(monkeypatch: pytest.MonkeyPatch) -> None:
    def mock_request(_: type, *args: str) -> bytes:
        return " ".join(args).encode("utf-8")

    monkeypatch.setattr(MockProtocol, "request", mock_request)
    assert (
        CaribouBoard(0, socket.socket(), MockProtocol).read_i2c(
            CaribouBoard.BusI2C.BUS_0, 0, 0, 0
        )
        == b"device.car_i2c_read 0 0 0 0 0"
    )
    assert (
        CaribouBoard(0, socket.socket(), MockProtocol).read_i2c(
            CaribouBoard.BusI2C.BUS_1, 0, 0, 0
        )
        == b"device.car_i2c_read 0 1 0 0 0"
    )


def test_peary_device_read_i2c_component(monkeypatch: pytest.MonkeyPatch) -> None:
    def mock_request(_: type, *args: str) -> bytes:
        return " ".join(args).encode("utf-8")

    monkeypatch.setattr(MockProtocol, "request", mock_request)
    assert (
        CaribouBoard(0, socket.socket(), MockProtocol).read_i2c(
            CaribouBoard.BusI2C.BUS_0, 0, 0, 0
        )
        == b"device.car_i2c_read 0 0 0 0 0"
    )
    assert (
        CaribouBoard(0, socket.socket(), MockProtocol).read_i2c(
            CaribouBoard.BusI2C.BUS_0, 1, 0, 0
        )
        == b"device.car_i2c_read 0 0 1 0 0"
    )


def test_peary_device_read_i2c_address(monkeypatch: pytest.MonkeyPatch) -> None:
    def mock_request(_: type, *args: str) -> bytes:
        return " ".join(args).encode("utf-8")

    monkeypatch.setattr(MockProtocol, "request", mock_request)
    assert (
        CaribouBoard(0, socket.socket(), MockProtocol).read_i2c(
            CaribouBoard.BusI2C.BUS_0, 0, 0, 0
        )
        == b"device.car_i2c_read 0 0 0 0 0"
    )
    assert (
        CaribouBoard(0, socket.socket(), MockProtocol).read_i2c(
            CaribouBoard.BusI2C.BUS_0, 0, 1, 0
        )
        == b"device.car_i2c_read 0 0 0 1 0"
    )


def test_peary_device_read_i2c_length(monkeypatch: pytest.MonkeyPatch) -> None:
    def mock_request(_: type, *args: str) -> bytes:
        return " ".join(args).encode("utf-8")

    monkeypatch.setattr(MockProtocol, "request", mock_request)
    assert (
        CaribouBoard(0, socket.socket(), MockProtocol).read_i2c(
            CaribouBoard.BusI2C.BUS_0, 0, 0, 0
        )
        == b"device.car_i2c_read 0 0 0 0 0"
    )
    assert (
        CaribouBoard(0, socket.socket(), MockProtocol).read_i2c(
            CaribouBoard.BusI2C.BUS_0, 0, 0, 1
        )
        == b"device.car_i2c_read 0 0 0 0 1"
    )
