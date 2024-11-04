from socket import socket as socket_type

import pytest

import peary
from peary.peary_protocol_interface import PearyProtocolInterface
from peary.peary_proxy import PearyProxy


class MockSocket:
    def __init__(self, *args, **kwargs):
        pass


class MockProtocol(PearyProtocolInterface):
    def __init__(self, socket: socket_type, timeout: int = 10):
        """Mock __init__"""

    def request(self, msg: str, *args: str, buffer_size: int = 4096):
        """Mock request"""


def test_peary_proxy_keep_alive(monkeypatch):
    def mock_request(encoded_request, return_value):
        def _mock_request(_, msg, *args):
            nonlocal encoded_request
            nonlocal return_value
            assert " ".join([msg, *args]).encode("utf-8") == encoded_request
            return return_value

        return _mock_request

    monkeypatch.setattr(MockProtocol, "request", mock_request(b"", b""))
    assert PearyProxy(MockSocket(), MockProtocol).keep_alive() == b""


def test_peary_proxy_add_device_unique_name(monkeypatch):
    def mock_request_name(_):
        return "name"

    monkeypatch.setattr(
        peary.peary_device.PearyDevice, "_request_name", mock_request_name
    )

    def mock_request(encoded_request, return_value):
        def _mock_request(_, *args):
            nonlocal encoded_request
            nonlocal return_value
            assert " ".join(args).encode("utf-8") == encoded_request
            return return_value

        return _mock_request

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


def test_peary_proxy_add_device_repeated_name(monkeypatch):
    def mock_request_name(_):
        return "name"

    monkeypatch.setattr(
        peary.peary_device.PearyDevice, "_request_name", mock_request_name
    )

    def mock_request(encoded_request, return_value):
        def _mock_request(_, *args):
            nonlocal encoded_request
            nonlocal return_value
            assert " ".join(args).encode("utf-8") == encoded_request
            return return_value

        return _mock_request

    proxy = PearyProxy(MockSocket(), MockProtocol)
    monkeypatch.setattr(MockProtocol, "request", mock_request(b"add_device a", b"0"))
    proxy.add_device("a")
    with pytest.raises(
        peary.peary_proxy.PearyProxy.PearyProxyAddDeviceError,
        match="Device already exists: a",
    ):
        proxy.add_device("a")


def test_peary_proxy_get_device_known(monkeypatch):
    def mock_request_name(_):
        return "name"

    monkeypatch.setattr(
        peary.peary_device.PearyDevice, "_request_name", mock_request_name
    )

    def mock_request(_, *args):
        return b"0"

    proxy = PearyProxy(MockSocket(), MockProtocol)
    monkeypatch.setattr(MockProtocol, "request", mock_request)
    device = proxy.add_device("a")
    assert device.index == proxy.get_device("a").index
    assert device.name == proxy.get_device("a").name


def test_peary_proxy_get_device_unknown(monkeypatch):
    for name in ["alpha", "beta"]:
        with pytest.raises(
            peary.peary_proxy.PearyProxy.PearyProxyGetDeviceError,
            match=f"Unknown device: {name}",
        ):
            PearyProxy(MockSocket(), MockProtocol).get_device(name)


def test_peary_proxy_clear_devices(monkeypatch):
    def mock_request_name(_):
        return "name"

    monkeypatch.setattr(
        peary.peary_device.PearyDevice, "_request_name", mock_request_name
    )

    def mock_request(encoded_request, return_value):
        def _mock_request(_, *args):
            nonlocal encoded_request
            nonlocal return_value
            assert " ".join(args).encode("utf-8") == encoded_request
            return return_value

        return _mock_request

    proxy = PearyProxy(MockSocket(), MockProtocol)
    assert not proxy.list_devices()

    monkeypatch.setattr(MockProtocol, "request", mock_request(b"add_device a", b"0"))
    device = proxy.add_device("a")
    assert proxy.list_devices() == ["a"]

    monkeypatch.setattr(MockProtocol, "request", mock_request(b"add_device b", b"1"))
    device = proxy.add_device("b")
    assert set(proxy.list_devices()) == set(["a", "b"])

    monkeypatch.setattr(MockProtocol, "request", mock_request(b"clear_devices", b""))
    proxy.clear_devices()
    assert not proxy.list_devices()


def test_peary_proxy_list_devices(monkeypatch):
    def mock_request_name(_):
        return "name"

    monkeypatch.setattr(
        peary.peary_device.PearyDevice, "_request_name", mock_request_name
    )

    def mock_request(_, *args):
        return b"0"

    proxy = PearyProxy(MockSocket(), MockProtocol)
    monkeypatch.setattr(MockProtocol, "request", mock_request)
    assert not proxy.list_devices()
    device = proxy.add_device("a")
    assert proxy.list_devices() == ["a"]
    device = proxy.add_device("b")
    assert set(proxy.list_devices()) == set(["a", "b"])


def test_peary_proxy_list_remote_devices(monkeypatch):
    def mock_request(encoded_request, return_value):
        def _mock_request(_, *args):
            nonlocal encoded_request
            nonlocal return_value
            assert " ".join(args).encode("utf-8") == encoded_request
            return return_value

        return _mock_request

    proxy = PearyProxy(MockSocket(), MockProtocol)
    monkeypatch.setattr(
        MockProtocol, "request", mock_request(b"list_devices", b"response-bytes")
    )
    assert (
        PearyProxy(MockSocket(), MockProtocol).list_remote_devices()
        == b"response-bytes"
    )
