from __future__ import annotations

from caribou.caribou_board import CaribouBoard

# TODO(Jeff): Test that the enables are declared are outputs at initialization


# pylint: disable=missing-param-doc
class MockProtocol:
    def __init__(self, socket, **_):
        self._socket = socket

    def request(self, *_):
        return self._socket.encode("utf-8")


def test_caribou_board_init_index(monkeypatch):
    def mock_request(_, *args):
        return " ".join(args).encode("utf-8")

    monkeypatch.setattr(MockProtocol, "request", mock_request)
    assert CaribouBoard(0, None, MockProtocol).index == 0
    assert CaribouBoard(1, None, MockProtocol).index == 1


def test_caribou_board_init_name(monkeypatch):
    def mock_request(_, *args):
        return " ".join(args).encode("utf-8")

    monkeypatch.setattr(MockProtocol, "request", mock_request)
    assert CaribouBoard(0, None, MockProtocol).name == "device.name 0"
    assert CaribouBoard(1, None, MockProtocol).name == "device.name 1"


def test_caribou_board_init_repr(monkeypatch):
    def mock_request(_, *args):
        return " ".join(args).encode("utf-8")

    monkeypatch.setattr(MockProtocol, "request", mock_request)
    assert str(CaribouBoard(0, None, MockProtocol)) == "device.name 0(0)"
    assert str(CaribouBoard(1, None, MockProtocol)) == "device.name 1(1)"


def test_caribou_board_init_socket():
    assert CaribouBoard(0, "alpha", MockProtocol).name == "alpha"
    assert CaribouBoard(1, "beta", MockProtocol).name == "beta"


def test_caribou_board_init_enable_power_supplies(monkeypatch):
    transactions = []

    def mock_write_i2c(*args):
        nonlocal transactions
        transactions.append(" ".join([str(_) for _ in args]))

    def mock_request(_, *args):
        return " ".join(args).encode("utf-8")

    monkeypatch.setattr(MockProtocol, "request", mock_request)
    monkeypatch.setattr(CaribouBoard, "write_i2c", mock_write_i2c)
    CaribouBoard(0, None, MockProtocol)
    assert transactions == [
        "device.name 0(0) BusI2C.BUS_0 118 6 0",
        "device.name 0(0) BusI2C.BUS_0 118 7 0",
    ]
