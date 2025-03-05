from __future__ import annotations

from typing import TYPE_CHECKING

from caribou.caribou_board import CaribouBoard
from peary.peary_protocol_interface import PearyProtocolInterface

if TYPE_CHECKING:
    from socket import socket as socket_type


# pylint: disable=missing-param-doc
class MockProtocol(PearyProtocolInterface):
    def __init__(self, socket: socket_type, timeout: int = 10):
        """Mock __init__"""

    def request(self, msg: str, *args: str, buffer_size: int = 4096):
        """Mock request"""


def test_caribou_board_current_bias_constants():
    assert CaribouBoard.BusI2C.BUS_0.value == 0
    assert CaribouBoard.BusI2C.BUS_1.value == 1
    assert CaribouBoard.BusI2C.BUS_2.value == 2
    assert CaribouBoard.BusI2C.BUS_3.value == 3


def test_peary_device_write_i2c_bus(monkeypatch):
    def mock_request(_, *args):
        return " ".join(args).encode("utf-8")

    monkeypatch.setattr(MockProtocol, "request", mock_request)
    assert (
        CaribouBoard(0, None, MockProtocol).write_i2c(
            CaribouBoard.BusI2C.BUS_0.value, 0, 0, 0
        )
        == b"device.car_i2c_write 0 0 0 0 0"
    )
    assert (
        CaribouBoard(0, None, MockProtocol).write_i2c(
            CaribouBoard.BusI2C.BUS_1.value, 0, 0, 0
        )
        == b"device.car_i2c_write 0 1 0 0 0"
    )


def test_peary_device_write_i2c_component(monkeypatch):
    def mock_request(_, *args):
        return " ".join(args).encode("utf-8")

    monkeypatch.setattr(MockProtocol, "request", mock_request)
    assert (
        CaribouBoard(0, None, MockProtocol).write_i2c(
            CaribouBoard.BusI2C.BUS_0.value, 0, 0, 0
        )
        == b"device.car_i2c_write 0 0 0 0 0"
    )
    assert (
        CaribouBoard(0, None, MockProtocol).write_i2c(
            CaribouBoard.BusI2C.BUS_0.value, 1, 0, 0
        )
        == b"device.car_i2c_write 0 0 1 0 0"
    )


def test_peary_device_write_i2c_address(monkeypatch):
    def mock_request(_, *args):
        return " ".join(args).encode("utf-8")

    monkeypatch.setattr(MockProtocol, "request", mock_request)
    assert (
        CaribouBoard(0, None, MockProtocol).write_i2c(
            CaribouBoard.BusI2C.BUS_0.value, 0, 0, 0
        )
        == b"device.car_i2c_write 0 0 0 0 0"
    )
    assert (
        CaribouBoard(0, None, MockProtocol).write_i2c(
            CaribouBoard.BusI2C.BUS_0.value, 0, 1, 0
        )
        == b"device.car_i2c_write 0 0 0 1 0"
    )


def test_peary_device_write_i2c_data(monkeypatch):
    def mock_request(_, *args):
        return " ".join(args).encode("utf-8")

    monkeypatch.setattr(MockProtocol, "request", mock_request)
    assert (
        CaribouBoard(0, None, MockProtocol).write_i2c(
            CaribouBoard.BusI2C.BUS_0.value, 0, 0, 0
        )
        == b"device.car_i2c_write 0 0 0 0 0"
    )
    assert (
        CaribouBoard(0, None, MockProtocol).write_i2c(
            CaribouBoard.BusI2C.BUS_0.value, 0, 0, 1
        )
        == b"device.car_i2c_write 0 0 0 0 1"
    )


def test_peary_device_read_i2c_bus(monkeypatch):
    def mock_request(_, *args):
        return " ".join(args).encode("utf-8")

    monkeypatch.setattr(MockProtocol, "request", mock_request)
    assert (
        CaribouBoard(0, None, MockProtocol).read_i2c(
            CaribouBoard.BusI2C.BUS_0.value, 0, 0, 0
        )
        == b"device.car_i2c_read 0 0 0 0 0"
    )
    assert (
        CaribouBoard(0, None, MockProtocol).read_i2c(
            CaribouBoard.BusI2C.BUS_1.value, 0, 0, 0
        )
        == b"device.car_i2c_read 0 1 0 0 0"
    )


def test_peary_device_read_i2c_component(monkeypatch):
    def mock_request(_, *args):
        return " ".join(args).encode("utf-8")

    monkeypatch.setattr(MockProtocol, "request", mock_request)
    assert (
        CaribouBoard(0, None, MockProtocol).read_i2c(
            CaribouBoard.BusI2C.BUS_0.value, 0, 0, 0
        )
        == b"device.car_i2c_read 0 0 0 0 0"
    )
    assert (
        CaribouBoard(0, None, MockProtocol).read_i2c(
            CaribouBoard.BusI2C.BUS_0.value, 1, 0, 0
        )
        == b"device.car_i2c_read 0 0 1 0 0"
    )


def test_peary_device_read_i2c_address(monkeypatch):
    def mock_request(_, *args):
        return " ".join(args).encode("utf-8")

    monkeypatch.setattr(MockProtocol, "request", mock_request)
    assert (
        CaribouBoard(0, None, MockProtocol).read_i2c(
            CaribouBoard.BusI2C.BUS_0.value, 0, 0, 0
        )
        == b"device.car_i2c_read 0 0 0 0 0"
    )
    assert (
        CaribouBoard(0, None, MockProtocol).read_i2c(
            CaribouBoard.BusI2C.BUS_0.value, 0, 1, 0
        )
        == b"device.car_i2c_read 0 0 0 1 0"
    )


def test_peary_device_read_i2c_length(monkeypatch):
    def mock_request(_, *args):
        return " ".join(args).encode("utf-8")

    monkeypatch.setattr(MockProtocol, "request", mock_request)
    assert (
        CaribouBoard(0, None, MockProtocol).read_i2c(
            CaribouBoard.BusI2C.BUS_0.value, 0, 0, 0
        )
        == b"device.car_i2c_read 0 0 0 0 0"
    )
    assert (
        CaribouBoard(0, None, MockProtocol).read_i2c(
            CaribouBoard.BusI2C.BUS_0.value, 0, 0, 1
        )
        == b"device.car_i2c_read 0 0 0 0 1"
    )
