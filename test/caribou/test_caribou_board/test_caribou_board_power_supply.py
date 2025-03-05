from caribou.caribou_board import CaribouBoard
from caribou.power_supply import PowerSupply


# pylint: disable=missing-param-doc
class MockProtocol:
    def __init__(self, *_):
        pass

    def request(self, *_):
        return "".encode("utf-8")


def test_caribou_board_power_supply_constants():
    assert CaribouBoard.PWR_OUT_1.value == "PWR_OUT_1"
    assert CaribouBoard.PWR_OUT_2.value == "PWR_OUT_2"
    assert CaribouBoard.PWR_OUT_3.value == "PWR_OUT_3"
    assert CaribouBoard.PWR_OUT_4.value == "PWR_OUT_4"
    assert CaribouBoard.PWR_OUT_5.value == "PWR_OUT_5"
    assert CaribouBoard.PWR_OUT_6.value == "PWR_OUT_6"
    assert CaribouBoard.PWR_OUT_7.value == "PWR_OUT_7"
    assert CaribouBoard.PWR_OUT_8.value == "PWR_OUT_8"


def test_caribou_board_power_supply_type():
    caribou_board = CaribouBoard(None, None, MockProtocol)
    assert isinstance(caribou_board.power_supply(CaribouBoard.PWR_OUT_1), PowerSupply)
    assert isinstance(caribou_board.power_supply(CaribouBoard.PWR_OUT_2), PowerSupply)
    assert isinstance(caribou_board.power_supply(CaribouBoard.PWR_OUT_3), PowerSupply)
    assert isinstance(caribou_board.power_supply(CaribouBoard.PWR_OUT_4), PowerSupply)
    assert isinstance(caribou_board.power_supply(CaribouBoard.PWR_OUT_5), PowerSupply)
    assert isinstance(caribou_board.power_supply(CaribouBoard.PWR_OUT_6), PowerSupply)
    assert isinstance(caribou_board.power_supply(CaribouBoard.PWR_OUT_7), PowerSupply)
    assert isinstance(caribou_board.power_supply(CaribouBoard.PWR_OUT_8), PowerSupply)


def test_caribou_board_power_supply_names():
    caribou_board = CaribouBoard(None, None, MockProtocol)
    assert caribou_board.power_supply(CaribouBoard.PWR_OUT_1).name == "PWR_OUT_1"
    assert caribou_board.power_supply(CaribouBoard.PWR_OUT_2).name == "PWR_OUT_2"
    assert caribou_board.power_supply(CaribouBoard.PWR_OUT_3).name == "PWR_OUT_3"
    assert caribou_board.power_supply(CaribouBoard.PWR_OUT_4).name == "PWR_OUT_4"
    assert caribou_board.power_supply(CaribouBoard.PWR_OUT_5).name == "PWR_OUT_5"
    assert caribou_board.power_supply(CaribouBoard.PWR_OUT_6).name == "PWR_OUT_6"
    assert caribou_board.power_supply(CaribouBoard.PWR_OUT_7).name == "PWR_OUT_7"
    assert caribou_board.power_supply(CaribouBoard.PWR_OUT_8).name == "PWR_OUT_8"


def test_caribou_board_power_supply_devices():
    caribou_board = CaribouBoard(None, None, MockProtocol)
    assert caribou_board.power_supply(CaribouBoard.PWR_OUT_1).device is caribou_board
    assert caribou_board.power_supply(CaribouBoard.PWR_OUT_2).device is caribou_board
    assert caribou_board.power_supply(CaribouBoard.PWR_OUT_3).device is caribou_board
    assert caribou_board.power_supply(CaribouBoard.PWR_OUT_4).device is caribou_board
    assert caribou_board.power_supply(CaribouBoard.PWR_OUT_5).device is caribou_board
    assert caribou_board.power_supply(CaribouBoard.PWR_OUT_6).device is caribou_board
    assert caribou_board.power_supply(CaribouBoard.PWR_OUT_7).device is caribou_board
    assert caribou_board.power_supply(CaribouBoard.PWR_OUT_8).device is caribou_board
