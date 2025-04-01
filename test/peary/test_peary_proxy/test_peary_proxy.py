from __future__ import annotations

from typing import TYPE_CHECKING

import pytest

import peary
from peary.peary_device import PearyDevice

if TYPE_CHECKING:
    from collections.abc import Callable


def test_peary_proxy_keep_alive(mock_proxy: Callable) -> None:
    assert mock_proxy().keep_alive() == b""


def test_peary_proxy_add_device_unique_name(mock_proxy: Callable) -> None:
    for name, index in zip(["alpha", "beta"], [b"0", b"1"]):
        assert mock_proxy(req=f"add_device {name}", resp=index).add_device(
            name
        ).index == int(index)


def test_peary_proxy_add_device_repeated_name(mock_proxy: Callable) -> None:
    proxy = mock_proxy(resp=b"0")
    proxy.add_device("a")
    with pytest.raises(
        peary.peary_proxy.PearyProxy.PearyProxyAddDeviceError,
        match="Device already exists: a",
    ):
        proxy.add_device("a")


def test_peary_proxy_add_device_default_device_class(mock_proxy: Callable) -> None:
    assert isinstance(mock_proxy(resp=b"0").add_device(""), PearyDevice)


def test_peary_proxy_add_device_explicit_device_class(mock_proxy: Callable) -> None:
    assert isinstance(mock_proxy(resp=b"0").add_device("", PearyDevice), PearyDevice)


def test_peary_proxy_add_device_derived_device_class(mock_proxy: Callable) -> None:
    class MockDevice(PearyDevice):
        pass

    assert isinstance(mock_proxy(resp=b"0").add_device("", MockDevice), MockDevice)


def test_peary_proxy_get_device_known(mock_proxy: Callable) -> None:
    proxy = mock_proxy(resp=b"0")
    device = proxy.add_device("")
    assert device is proxy.get_device("")


def test_peary_proxy_get_device_unknown(mock_proxy: Callable) -> None:
    proxy = mock_proxy(resp=b"0")
    for name in ("alpha", "beta"):
        with pytest.raises(
            peary.peary_proxy.PearyProxy.PearyProxyGetDeviceError,
            match=f"Unknown device: {name}",
        ):
            proxy.get_device(name)


def test_peary_proxy_list_devices(mock_proxy: Callable) -> None:
    proxy = mock_proxy(resp=b"0")
    assert not proxy.list_devices()

    proxy.add_device("a")
    assert proxy.list_devices() == ["a"]

    proxy.add_device("b")
    assert sorted(proxy.list_devices()) == ["a", "b"]


def test_peary_proxy_clear_devices(mock_proxy: Callable) -> None:
    proxy = mock_proxy(resp=b"0")
    assert not proxy.list_devices()

    proxy.add_device("a")
    proxy.add_device("b")
    assert sorted(proxy.list_devices()) == ["a", "b"]

    proxy.clear_devices()
    assert not proxy.list_devices()


def test_peary_proxy_list_remote_devices(mock_proxy: Callable) -> None:
    assert mock_proxy().list_remote_devices() == b"list_devices"
