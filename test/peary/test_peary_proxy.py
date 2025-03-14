from __future__ import annotations

import socket as socket_module
from typing import TYPE_CHECKING

import pytest

import peary
from peary.peary_device import PearyDevice
from peary.peary_protocol import PearyProtocol
from peary.peary_proxy import PearyProxy

if TYPE_CHECKING:
    from collections.abc import Callable
    from socket import socket as socket_type

# TODO(Jeff): Rewrite tests using derived classes instead of monkey patching everything.


class MockProtocol(PearyProtocol):

    # pylint: disable-next=W0231
    def __init__(self, socket: socket_type, timeout: int = 1) -> None:
        """Mock initializer."""


class MockSocket(socket_module.socket):

    # pylint: disable-next=W0231
    def __init__(self) -> None:
        """Mock initializer."""


@pytest.fixture(name="mock_request")
def _mock_request() -> Callable:
    def __mock_request(encoded_request: bytes, return_value: bytes) -> Callable:
        def mock_request_assert_encoded_result(_, *args: str) -> bytes:  # noqa: ANN001
            nonlocal encoded_request
            nonlocal return_value
            assert " ".join(args).encode("utf-8") == encoded_request
            return return_value

        return mock_request_assert_encoded_result

    return __mock_request


def test_peary_proxy_keep_alive(
    monkeypatch: pytest.MonkeyPatch, mock_request: Callable
) -> None:
    monkeypatch.setattr(MockProtocol, "request", mock_request(b"", b""))
    assert PearyProxy(MockSocket(), MockProtocol).keep_alive() == b""


def test_peary_proxy_add_device_unique_name(
    monkeypatch: pytest.MonkeyPatch, mock_request: Callable
) -> None:
    monkeypatch.setattr(
        peary.peary_device.PearyDevice, "_request_name", lambda _: "name"
    )
    proxy = PearyProxy(MockSocket(), MockProtocol)
    for name, index in zip(["alpha", "beta"], [0, 1]):
        monkeypatch.setattr(
            MockProtocol,
            "request",
            mock_request(
                f"add_device {name}".encode("utf-8"), f"{index}".encode("utf-8")
            ),
        )
        assert str(proxy.add_device(name)) == f"name({index})"


def test_peary_proxy_add_device_repeated_name(
    monkeypatch: pytest.MonkeyPatch, mock_request: Callable
) -> None:
    monkeypatch.setattr(
        peary.peary_device.PearyDevice, "_request_name", lambda _: "name"
    )
    proxy = PearyProxy(MockSocket(), MockProtocol)
    monkeypatch.setattr(MockProtocol, "request", mock_request(b"add_device a", b"0"))
    proxy.add_device("a")
    with pytest.raises(
        peary.peary_proxy.PearyProxy.PearyProxyAddDeviceError,
        match="Device already exists: a",
    ):
        proxy.add_device("a")


def test_peary_proxy_add_device_default_device_class(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setattr(
        peary.peary_device.PearyDevice, "_request_name", lambda _: "name"
    )
    monkeypatch.setattr(MockProtocol, "request", lambda *_: 0)
    proxy = PearyProxy(MockSocket(), MockProtocol)
    assert isinstance(proxy.add_device("name"), PearyDevice)


def test_peary_proxy_add_device_explicit_device_class(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setattr(peary.peary_device.PearyDevice, "_request_name", lambda _: "")
    monkeypatch.setattr(MockProtocol, "request", lambda *_: 0)
    proxy = PearyProxy(MockSocket(), MockProtocol)
    assert isinstance(proxy.add_device("name", PearyDevice), PearyDevice)


def test_peary_proxy_add_device_derived_device_class(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    class MockDevice(PearyDevice):
        pass

    monkeypatch.setattr(peary.peary_device.PearyDevice, "_request_name", lambda _: "")
    monkeypatch.setattr(MockProtocol, "request", lambda *_: 0)
    proxy = PearyProxy(MockSocket(), MockProtocol)
    assert isinstance(proxy.add_device("", MockDevice), MockDevice)


def test_peary_proxy_get_device_known(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(peary.peary_device.PearyDevice, "_request_name", lambda _: "")
    proxy = PearyProxy(MockSocket(), MockProtocol)
    monkeypatch.setattr(MockProtocol, "request", lambda *_: b"0")
    device = proxy.add_device("a")
    assert device.index == proxy.get_device("a").index
    assert device.name == proxy.get_device("a").name


def test_peary_proxy_get_device_unknown() -> None:
    for name in ("alpha", "beta"):
        with pytest.raises(
            peary.peary_proxy.PearyProxy.PearyProxyGetDeviceError,
            match=f"Unknown device: {name}",
        ):
            PearyProxy(MockSocket(), MockProtocol).get_device(name)


def test_peary_proxy_clear_devices(
    monkeypatch: pytest.MonkeyPatch, mock_request: Callable
) -> None:
    monkeypatch.setattr(peary.peary_device.PearyDevice, "_request_name", lambda _: "")

    proxy = PearyProxy(MockSocket(), MockProtocol)
    assert not proxy.list_devices()

    monkeypatch.setattr(MockProtocol, "request", mock_request(b"add_device a", b"0"))
    _ = proxy.add_device("a")
    assert proxy.list_devices() == ["a"]

    monkeypatch.setattr(MockProtocol, "request", mock_request(b"add_device b", b"1"))
    _ = proxy.add_device("b")
    assert set(proxy.list_devices()) == {"a", "b"}

    monkeypatch.setattr(MockProtocol, "request", mock_request(b"clear_devices", b""))
    proxy.clear_devices()
    assert not proxy.list_devices()


def test_peary_proxy_list_devices(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(peary.peary_device.PearyDevice, "_request_name", lambda _: "")
    proxy = PearyProxy(MockSocket(), MockProtocol)
    monkeypatch.setattr(MockProtocol, "request", lambda *_: b"0")

    assert not proxy.list_devices()
    _ = proxy.add_device("a")
    assert proxy.list_devices() == ["a"]
    _ = proxy.add_device("b")
    assert set(proxy.list_devices()) == {"a", "b"}


def test_peary_proxy_list_remote_devices(
    monkeypatch: pytest.MonkeyPatch, mock_request: Callable
) -> None:
    monkeypatch.setattr(
        MockProtocol, "request", mock_request(b"list_devices", b"response-bytes")
    )
    assert (
        PearyProxy(MockSocket(), MockProtocol).list_remote_devices()
        == b"response-bytes"
    )
