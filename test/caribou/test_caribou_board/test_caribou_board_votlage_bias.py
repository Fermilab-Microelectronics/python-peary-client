from caribou.caribou_board import CaribouBoard
from caribou.voltage_bias import VoltageBias


# pylint: disable=missing-param-doc
class MockProtocol:
    def __init__(self, *_):
        pass

    def request(self, *_):
        return "".encode("utf-8")


def test_caribou_board_voltage_bias_constants():
    assert CaribouBoard.VBIAS_1.value == "BIAS_1"
    assert CaribouBoard.VBIAS_2.value == "BIAS_2"
    assert CaribouBoard.VBIAS_3.value == "BIAS_3"
    assert CaribouBoard.VBIAS_4.value == "BIAS_4"
    assert CaribouBoard.VBIAS_5.value == "BIAS_5"


def test_caribou_board_voltage_bias_type():
    caribou_board = CaribouBoard(None, None, MockProtocol)
    assert isinstance(caribou_board.voltage_bias(CaribouBoard.VBIAS_1), VoltageBias)
    assert isinstance(caribou_board.voltage_bias(CaribouBoard.VBIAS_2), VoltageBias)
    assert isinstance(caribou_board.voltage_bias(CaribouBoard.VBIAS_3), VoltageBias)
    assert isinstance(caribou_board.voltage_bias(CaribouBoard.VBIAS_4), VoltageBias)
    assert isinstance(caribou_board.voltage_bias(CaribouBoard.VBIAS_5), VoltageBias)


def test_caribou_board_voltage_bias_names():
    caribou_board = CaribouBoard(None, None, MockProtocol)
    assert caribou_board.voltage_bias(CaribouBoard.VBIAS_1).name == "BIAS_1"
    assert caribou_board.voltage_bias(CaribouBoard.VBIAS_2).name == "BIAS_2"
    assert caribou_board.voltage_bias(CaribouBoard.VBIAS_3).name == "BIAS_3"
    assert caribou_board.voltage_bias(CaribouBoard.VBIAS_4).name == "BIAS_4"
    assert caribou_board.voltage_bias(CaribouBoard.VBIAS_5).name == "BIAS_5"


def test_caribou_board_voltage_bias_devices():
    caribou_board = CaribouBoard(None, None, MockProtocol)
    assert caribou_board.voltage_bias(CaribouBoard.VBIAS_1).device is caribou_board
    assert caribou_board.voltage_bias(CaribouBoard.VBIAS_2).device is caribou_board
    assert caribou_board.voltage_bias(CaribouBoard.VBIAS_3).device is caribou_board
    assert caribou_board.voltage_bias(CaribouBoard.VBIAS_4).device is caribou_board
    assert caribou_board.voltage_bias(CaribouBoard.VBIAS_5).device is caribou_board
