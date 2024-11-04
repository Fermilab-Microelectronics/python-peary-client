from socket import socket as socket_type

import pytest

from peary.peary_device import PearyDevice
from peary.peary_protocol_interface import PearyProtocolInterface


# pylint: disable=missing-param-doc
class MockProtocol(PearyProtocolInterface):
    def __init__(self, socket: socket_type, timeout: int = 10):
        """Mock __init__"""

    def request(self, msg: str, *args: str, buffer_size: int = 4096):
        """Mock request"""


@pytest.fixture(name="mock_peary_device_getter_method")
def _mock_peary_device_getter_method(monkeypatch):
    def __mock_peary_device_getter_method(method, name, value):
        def mock_request_name(_):
            pass

        monkeypatch.setattr(PearyDevice, "_request_name", mock_request_name)

        def mock_request(method, name, value):
            def _mock_request(_, *args):
                nonlocal method
                nonlocal name
                assert " ".join(str(x) for x in args) == f"device.{method} 0 {name}"
                return value

            return _mock_request

        monkeypatch.setattr(MockProtocol, "request", mock_request(method, name, value))
        func = getattr(PearyDevice(0, None, MockProtocol), method)
        return func(name)

    return __mock_peary_device_getter_method


def test_peary_device_init_index(monkeypatch):
    def mock_request(_, *args):
        return " ".join(args).encode("utf-8")

    monkeypatch.setattr(MockProtocol, "request", mock_request)
    assert PearyDevice(0, None, MockProtocol).index == 0
    assert PearyDevice(1, None, MockProtocol).index == 1


def test_peary_device_init_name(monkeypatch):
    def mock_request(_, *args):
        return " ".join(args).encode("utf-8")

    monkeypatch.setattr(MockProtocol, "request", mock_request)
    assert PearyDevice(0, None, MockProtocol).name == "device.name 0"
    assert PearyDevice(1, None, MockProtocol).name == "device.name 1"


def test_peary_device_repr(monkeypatch):
    def mock_request(_, *args):
        return " ".join(args).encode("utf-8")

    monkeypatch.setattr(MockProtocol, "request", mock_request)
    assert str(PearyDevice(0, None, MockProtocol)) == "device.name 0(0)"
    assert str(PearyDevice(1, None, MockProtocol)) == "device.name 1(1)"


def test_peary_device_power_on(monkeypatch):
    def mock_request(_, *args):
        return " ".join(args).encode("utf-8")

    monkeypatch.setattr(MockProtocol, "request", mock_request)
    assert PearyDevice(0, None, MockProtocol).power_on() == b"device.power_on 0"
    assert PearyDevice(1, None, MockProtocol).power_on() == b"device.power_on 1"


def test_peary_device_power_off(monkeypatch):
    def mock_request(_, *args):
        return " ".join(args).encode("utf-8")

    monkeypatch.setattr(MockProtocol, "request", mock_request)
    assert PearyDevice(0, None, MockProtocol).power_off() == b"device.power_off 0"
    assert PearyDevice(1, None, MockProtocol).power_off() == b"device.power_off 1"


def test_peary_device_reset(monkeypatch):
    def mock_request(_, *args):
        return " ".join(args).encode("utf-8")

    monkeypatch.setattr(MockProtocol, "request", mock_request)
    assert PearyDevice(0, None, MockProtocol).reset() == b"device.reset 0"
    assert PearyDevice(1, None, MockProtocol).reset() == b"device.reset 1"


def test_peary_device_configure(monkeypatch):
    def mock_request(_, *args):
        return " ".join(args).encode("utf-8")

    monkeypatch.setattr(MockProtocol, "request", mock_request)
    assert PearyDevice(0, None, MockProtocol).configure() == b"device.configure 0"
    assert PearyDevice(1, None, MockProtocol).configure() == b"device.configure 1"


def test_peary_device_daq_start(monkeypatch):
    def mock_request(_, *args):
        return " ".join(args).encode("utf-8")

    monkeypatch.setattr(MockProtocol, "request", mock_request)
    assert PearyDevice(0, None, MockProtocol).daq_start() == b"device.daq_start 0"
    assert PearyDevice(1, None, MockProtocol).daq_start() == b"device.daq_start 1"


def test_peary_device_daq_stop(monkeypatch):
    def mock_request(_, *args):
        return " ".join(args).encode("utf-8")

    monkeypatch.setattr(MockProtocol, "request", mock_request)
    assert PearyDevice(0, None, MockProtocol).daq_stop() == b"device.daq_stop 0"
    assert PearyDevice(1, None, MockProtocol).daq_stop() == b"device.daq_stop 1"


def test_peary_device_list_registers(monkeypatch):
    def mock_request(_, *args):
        return " ".join(args).encode("utf-8")

    monkeypatch.setattr(MockProtocol, "request", mock_request)
    assert PearyDevice(0, None, MockProtocol).list_registers() == [
        "device.list_registers",
        "0",
    ]
    assert PearyDevice(1, None, MockProtocol).list_registers() == [
        "device.list_registers",
        "1",
    ]


def test_peary_device_get_register(mock_peary_device_getter_method):
    assert mock_peary_device_getter_method("get_register", "alpha", 0) == 0
    assert mock_peary_device_getter_method("get_register", "alpha", 1) == 1
    assert mock_peary_device_getter_method("get_register", "beta", 0) == 0
    assert mock_peary_device_getter_method("get_register", "beta", 1) == 1


def test_peary_device_set_register(monkeypatch):
    def mock_request(_, *args):
        return " ".join(args).encode("utf-8")

    monkeypatch.setattr(MockProtocol, "request", mock_request)

    for index, name, value in zip([0, 1], ["alpha", "beta"], [0, 1]):
        assert (
            PearyDevice(index, None, MockProtocol)
            .set_register(name, value)
            .decode("utf-8")
            == f"device.set_register {index} {name} {value}"
        )


def test_peary_device_get_memory(mock_peary_device_getter_method):
    assert mock_peary_device_getter_method("get_memory", "alpha", 0) == 0
    assert mock_peary_device_getter_method("get_memory", "alpha", 1) == 1
    assert mock_peary_device_getter_method("get_memory", "beta", 0) == 0
    assert mock_peary_device_getter_method("get_memory", "beta", 1) == 1


def test_peary_device_set_memory(monkeypatch):
    def mock_request(_, *args):
        return " ".join(args).encode("utf-8")

    monkeypatch.setattr(MockProtocol, "request", mock_request)

    for index, name, value in zip([0, 1], ["alpha", "beta"], [0, 1]):
        assert (
            PearyDevice(index, None, MockProtocol)
            .set_memory(name, value)
            .decode("utf-8")
            == f"device.set_memory {index} {name} {value}"
        )


def test_peary_device_get_current(mock_peary_device_getter_method):
    assert mock_peary_device_getter_method("get_current", "alpha", 0) == 0
    assert mock_peary_device_getter_method("get_current", "alpha", 1) == 1
    assert mock_peary_device_getter_method("get_current", "beta", 0) == 0
    assert mock_peary_device_getter_method("get_current", "beta", 1) == 1


def test_peary_device_set_current(monkeypatch):
    def mock_request(_, *args):
        return " ".join(args).encode("utf-8")

    monkeypatch.setattr(MockProtocol, "request", mock_request)

    for index, name, value in zip([0, 1], ["alpha", "beta"], [0, 1]):
        assert (
            PearyDevice(index, None, MockProtocol)
            .set_current(name, value)
            .decode("utf-8")
            == f"device.set_current {index} {name} {value}"
        )


def test_peary_device_get_voltage(mock_peary_device_getter_method):
    assert mock_peary_device_getter_method("get_voltage", "alpha", 0) == 0
    assert mock_peary_device_getter_method("get_voltage", "alpha", 1) == 1
    assert mock_peary_device_getter_method("get_voltage", "beta", 0) == 0
    assert mock_peary_device_getter_method("get_voltage", "beta", 1) == 1


def test_peary_device_set_voltage(monkeypatch):
    def mock_request(_, *args):
        return " ".join(args).encode("utf-8")

    monkeypatch.setattr(MockProtocol, "request", mock_request)

    for index, name, value in zip([0, 1], ["alpha", "beta"], [0, 1]):
        assert (
            PearyDevice(index, None, MockProtocol)
            .set_voltage(name, value)
            .decode("utf-8")
            == f"device.set_voltage {index} {name} {value}"
        )


def test_peary_device_switch_on(monkeypatch):
    def mock_request(_, *args):
        return " ".join(args).encode("utf-8")

    monkeypatch.setattr(MockProtocol, "request", mock_request)
    for index, name in zip([0, 1], ["alpha", "beta"]):
        assert (
            PearyDevice(index, None, MockProtocol).switch_on(name).decode("utf-8")
            == f"device.switch_on {index} {name}"
        )


def test_peary_device_switch_off(monkeypatch):
    def mock_request(_, *args):
        return " ".join(args).encode("utf-8")

    monkeypatch.setattr(MockProtocol, "request", mock_request)
    for index, name in zip([0, 1], ["alpha", "beta"]):
        assert (
            PearyDevice(index, None, MockProtocol).switch_off(name).decode("utf-8")
            == f"device.switch_off {index} {name}"
        )
