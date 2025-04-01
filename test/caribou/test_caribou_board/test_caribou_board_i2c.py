from __future__ import annotations

from typing import TYPE_CHECKING

from caribou.caribou_board import CaribouBoard

if TYPE_CHECKING:
    from collections.abc import Callable


def test_caribou_board_i2c_constants() -> None:
    assert CaribouBoard.BusI2C.BUS_0.value == 0
    assert CaribouBoard.BusI2C.BUS_1.value == 1
    assert CaribouBoard.BusI2C.BUS_2.value == 2
    assert CaribouBoard.BusI2C.BUS_3.value == 3


def test_peary_device_i2c_write_index(mock_caribou_board: Callable) -> None:
    assert (
        mock_caribou_board(0).write_i2c(CaribouBoard.BusI2C.BUS_0, 0, 0, 0)
        == b"device.car_i2c_write 0 0 0 0 0"
    )
    assert (
        mock_caribou_board(1).write_i2c(CaribouBoard.BusI2C.BUS_0, 0, 0, 0)
        == b"device.car_i2c_write 1 0 0 0 0"
    )


def test_peary_device_i2c_write_bus(mock_caribou_board: Callable) -> None:
    assert (
        mock_caribou_board(0).write_i2c(CaribouBoard.BusI2C.BUS_0, 0, 0, 0)
        == b"device.car_i2c_write 0 0 0 0 0"
    )
    assert (
        mock_caribou_board(0).write_i2c(CaribouBoard.BusI2C.BUS_1, 0, 0, 0)
        == b"device.car_i2c_write 0 1 0 0 0"
    )


def test_peary_device_i2c_write_component(mock_caribou_board: Callable) -> None:
    assert (
        mock_caribou_board(0).write_i2c(CaribouBoard.BusI2C.BUS_0, 0, 0, 0)
        == b"device.car_i2c_write 0 0 0 0 0"
    )
    assert (
        mock_caribou_board(0).write_i2c(CaribouBoard.BusI2C.BUS_0, 1, 0, 0)
        == b"device.car_i2c_write 0 0 1 0 0"
    )


def test_peary_device_i2c_write_address(mock_caribou_board: Callable) -> None:
    assert (
        mock_caribou_board(0).write_i2c(CaribouBoard.BusI2C.BUS_0, 0, 0, 0)
        == b"device.car_i2c_write 0 0 0 0 0"
    )
    assert (
        mock_caribou_board(0).write_i2c(CaribouBoard.BusI2C.BUS_0, 0, 1, 0)
        == b"device.car_i2c_write 0 0 0 1 0"
    )


def test_peary_device_i2c_write_data(mock_caribou_board: Callable) -> None:
    assert (
        mock_caribou_board(0).write_i2c(CaribouBoard.BusI2C.BUS_0, 0, 0, 0)
        == b"device.car_i2c_write 0 0 0 0 0"
    )
    assert (
        mock_caribou_board(0).write_i2c(CaribouBoard.BusI2C.BUS_0, 0, 0, 1)
        == b"device.car_i2c_write 0 0 0 0 1"
    )


def test_peary_device_i2c_read_index(mock_caribou_board: Callable) -> None:
    assert (
        mock_caribou_board(0).read_i2c(CaribouBoard.BusI2C.BUS_0, 0, 0, 0)
        == b"device.car_i2c_read 0 0 0 0 0"
    )
    assert (
        mock_caribou_board(1).read_i2c(CaribouBoard.BusI2C.BUS_0, 0, 0, 0)
        == b"device.car_i2c_read 1 0 0 0 0"
    )


def test_peary_device_i2c_read_bus(mock_caribou_board: Callable) -> None:
    assert (
        mock_caribou_board(0).read_i2c(CaribouBoard.BusI2C.BUS_0, 0, 0, 0)
        == b"device.car_i2c_read 0 0 0 0 0"
    )
    assert (
        mock_caribou_board(0).read_i2c(CaribouBoard.BusI2C.BUS_1, 0, 0, 0)
        == b"device.car_i2c_read 0 1 0 0 0"
    )


def test_peary_device_i2c_read_component(mock_caribou_board: Callable) -> None:
    assert (
        mock_caribou_board(0).read_i2c(CaribouBoard.BusI2C.BUS_0, 0, 0, 0)
        == b"device.car_i2c_read 0 0 0 0 0"
    )
    assert (
        mock_caribou_board(0).read_i2c(CaribouBoard.BusI2C.BUS_0, 1, 0, 0)
        == b"device.car_i2c_read 0 0 1 0 0"
    )


def test_peary_device_i2c_read_address(mock_caribou_board: Callable) -> None:
    assert (
        mock_caribou_board(0).read_i2c(CaribouBoard.BusI2C.BUS_0, 0, 0, 0)
        == b"device.car_i2c_read 0 0 0 0 0"
    )
    assert (
        mock_caribou_board(0).read_i2c(CaribouBoard.BusI2C.BUS_0, 0, 1, 0)
        == b"device.car_i2c_read 0 0 0 1 0"
    )


def test_peary_device_i2c_read_length(mock_caribou_board: Callable) -> None:
    assert (
        mock_caribou_board(0).read_i2c(CaribouBoard.BusI2C.BUS_0, 0, 0, 0)
        == b"device.car_i2c_read 0 0 0 0 0"
    )
    assert (
        mock_caribou_board(0).read_i2c(CaribouBoard.BusI2C.BUS_0, 0, 0, 1)
        == b"device.car_i2c_read 0 0 0 0 1"
    )
