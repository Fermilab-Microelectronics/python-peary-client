from __future__ import annotations

import socket
from typing import TYPE_CHECKING

import pytest

from peary.peary_device import PearyDevice
from peary.peary_protocol import PearyProtocol

if TYPE_CHECKING:
    from collections.abc import Callable


class MockPearyDevice(PearyDevice):
    """A Mock Peary Protocol."""


@pytest.fixture(name="mock_device")
def _mock_device() -> Callable:

    def _mock_device(index: int, req: str, resp: bytes = b"") -> MockPearyDevice:

        class MockPearyProtocol(PearyProtocol):
            """A Mock Peary Protocol."""

            def request(
                self, msg: str, *args: str, buffer_size: int = 4096  # noqa: ARG002
            ) -> bytes:
                assert " ".join([msg, *args]) == req
                return resp

        return MockPearyDevice(
            index,
            MockPearyProtocol(socket.socket(), checks=PearyProtocol.Checks.CHECK_NONE),
        )

    return _mock_device


def test_peary_device_list_registers(mock_device: Callable) -> None:
    assert mock_device(
        index=0, req="device.list_registers 0", resp=b"alpha"
    ).list_registers() == ["alpha"]
    assert mock_device(
        index=1, req="device.list_registers 1", resp=b"alpha beta gamma"
    ).list_registers() == ["alpha", "beta", "gamma"]


def test_peary_device_get_register(mock_device: Callable) -> None:
    for index, name, value in zip([0, 1], ["alpha", "beta"], [b"0", b"1"]):
        assert mock_device(
            index=index, req=f"device.get_register {index} {name}", resp=value
        ).get_register(name) == int(value)


def test_peary_device_set_register(mock_device: Callable) -> None:
    for index, name, value in zip([0, 1], ["alpha", "beta"], [0, 1]):
        assert (
            mock_device(
                index=index, req=f"device.set_register {index} {name} {value}", resp=b""
            ).set_register(name, value)
            == b""
        )


def test_peary_device_get_memory(mock_device: Callable) -> None:
    for index, name, value in zip([0, 1], ["alpha", "beta"], [b"0", b"1"]):
        assert mock_device(
            index=index, req=f"device.get_memory {index} {name}", resp=value
        ).get_memory(name) == int(value)


def test_peary_device_set_memory(mock_device: Callable) -> None:
    for index, name, value in zip([0, 1], ["alpha", "beta"], [0, 1]):
        assert (
            mock_device(
                index=index, req=f"device.set_memory {index} {name} {value}", resp=b""
            ).set_memory(name, value)
            == b""
        )


def test_peary_device_get_current(mock_device: Callable) -> None:
    for index, name, value in zip([0, 1], ["alpha", "beta"], [b"1.0", b"2.0"]):
        assert mock_device(
            index=index, req=f"device.get_current {index} {name}", resp=value
        ).get_current(name) == float(value)


def test_peary_device_set_current(mock_device: Callable) -> None:
    for index, name, value in zip([0, 1], ["alpha", "beta"], [0, 1]):
        assert (
            mock_device(
                index=index, req=f"device.set_current {index} {name} {value}", resp=b""
            ).set_current(name, value)
            == b""
        )


def test_peary_device_get_voltage(mock_device: Callable) -> None:
    for index, name, value in zip([0, 1], ["alpha", "beta"], [b"1.0", b"2.0"]):
        assert mock_device(
            index=index, req=f"device.get_voltage {index} {name}", resp=value
        ).get_voltage(name) == float(value)


def test_peary_device_set_voltage(mock_device: Callable) -> None:
    for index, name, value in zip([0, 1], ["alpha", "beta"], [0, 1]):
        assert (
            mock_device(
                index=index, req=f"device.set_voltage {index} {name} {value}", resp=b""
            ).set_voltage(name, value)
            == b""
        )


def test_peary_device_switch_on(mock_device: Callable) -> None:
    for index, name, value in zip([0, 1], ["alpha", "beta"], [b"0", b"1"]):
        assert (
            mock_device(
                index=index, req=f"device.switch_on {index} {name}", resp=value
            ).switch_on(name)
            == value
        )


def test_peary_device_switch_off(mock_device: Callable) -> None:
    for index, name, value in zip([0, 1], ["alpha", "beta"], [b"0", b"1"]):
        assert (
            mock_device(
                index=index, req=f"device.switch_off {index} {name}", resp=value
            ).switch_off(name)
            == value
        )
