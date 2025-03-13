from __future__ import annotations

import socket
from contextlib import contextmanager
from typing import TYPE_CHECKING

import pytest

from peary.peary_device import PearyDevice
from peary.peary_protocol import PearyProtocol

if TYPE_CHECKING:
    from collections.abc import Callable, Generator


class MockPearyProtocol(PearyProtocol):
    """A Mock Peary Protocol."""

    def _verify_compatible_version(self) -> None:
        pass


class MockPearyDevice(PearyDevice):
    """A Mock Peary Protocol."""

    def _request_name(self) -> str:
        return ""


@pytest.fixture(name="mock_device_request")
def _mock_device_request(monkeypatch: pytest.MonkeyPatch) -> Callable:

    @contextmanager
    def _mock_device_request_context(
        index: int, req: str, resp: bytes = b""
    ) -> Generator:

        def _mock_protocol_request(_: MockPearyProtocol, *args: str) -> bytes:
            assert " ".join(args) == req
            return resp

        with monkeypatch.context() as m:
            m.setattr(MockPearyProtocol, "request", _mock_protocol_request)
            yield MockPearyDevice(index, socket.socket(), MockPearyProtocol)

    return _mock_device_request_context


def test_peary_device_list_registers(mock_device_request: Callable) -> None:
    with mock_device_request(
        index=0, req="device.list_registers 0", resp=b"alpha"
    ) as device:
        assert device.list_registers() == ["alpha"]
    with mock_device_request(
        index=1, req="device.list_registers 1", resp=b"alpha beta gamma"
    ) as device:
        assert device.list_registers() == ["alpha", "beta", "gamma"]


def test_peary_device_get_register(mock_device_request: Callable) -> None:
    for index, name, value in zip([0, 1], ["alpha", "beta"], [b"0", b"1"]):
        with mock_device_request(
            index=index, req=f"device.get_register {index} {name}", resp=value
        ) as device:
            assert device.get_register(name) == int(value)


def test_peary_device_set_register(mock_device_request: Callable) -> None:
    for index, name, value in zip([0, 1], ["alpha", "beta"], [0, 1]):
        with mock_device_request(
            index=index, req=f"device.set_register {index} {name} {value}", resp=b""
        ) as device:
            assert device.set_register(name, value) == b""


def test_peary_device_get_memory(mock_device_request: Callable) -> None:
    for index, name, value in zip([0, 1], ["alpha", "beta"], [b"0", b"1"]):
        with mock_device_request(
            index=index, req=f"device.get_memory {index} {name}", resp=value
        ) as device:
            assert device.get_memory(name) == int(value)


def test_peary_device_set_memory(mock_device_request: Callable) -> None:
    for index, name, value in zip([0, 1], ["alpha", "beta"], [0, 1]):
        with mock_device_request(
            index=index, req=f"device.set_memory {index} {name} {value}", resp=b""
        ) as device:
            assert device.set_memory(name, value) == b""


def test_peary_device_get_current(mock_device_request: Callable) -> None:
    for index, name, value in zip([0, 1], ["alpha", "beta"], [b"0", b"1"]):
        with mock_device_request(
            index=index, req=f"device.get_current {index} {name}", resp=value
        ) as device:
            assert device.get_current(name) == int(value)


def test_peary_device_set_current(mock_device_request: Callable) -> None:
    for index, name, value in zip([0, 1], ["alpha", "beta"], [0, 1]):
        with mock_device_request(
            index=index, req=f"device.set_current {index} {name} {value}", resp=b""
        ) as device:
            assert device.set_current(name, value) == b""


def test_peary_device_get_voltage(mock_device_request: Callable) -> None:
    for index, name, value in zip([0, 1], ["alpha", "beta"], [b"0", b"1"]):
        with mock_device_request(
            index=index, req=f"device.get_voltage {index} {name}", resp=value
        ) as device:
            assert device.get_voltage(name) == int(value)


def test_peary_device_set_voltage(mock_device_request: Callable) -> None:
    for index, name, value in zip([0, 1], ["alpha", "beta"], [0, 1]):
        with mock_device_request(
            index=index, req=f"device.set_voltage {index} {name} {value}", resp=b""
        ) as device:
            assert device.set_voltage(name, value) == b""
