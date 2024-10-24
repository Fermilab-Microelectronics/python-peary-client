import socket

import peary

from .mock_proxy import MockProxy
from .mock_socket import MockSocket


# pylint: disable=no-member
def test_peary_client_init_host():
    assert peary.PearyClient("alpha").host == "alpha"
    assert peary.PearyClient("beta").host == "beta"


def test_peary_client_init_port():
    assert peary.PearyClient("").port == 12345
    assert peary.PearyClient("", 12345).port == 12345
    assert peary.PearyClient("", 54321).port == 54321


def test_peary_client_init_proxy_class():
    assert peary.PearyClient("").proxy_class is peary.peary_proxy.PearyProxy
    assert peary.PearyClient("", proxy_class=MockProxy).proxy_class is MockProxy


def test_peary_client_init_socket(monkeypatch):
    monkeypatch.setattr("socket.socket", MockSocket)
    assert peary.PearyClient("").socket.family == socket.AF_INET
    assert peary.PearyClient("").socket.type == socket.SOCK_STREAM
    assert peary.PearyClient("").socket.address is None
    assert peary.PearyClient("").socket.is_connected is None
    assert peary.PearyClient("").socket.is_shutdown is None


def test_peary_client_context_manager_enter_proxy(monkeypatch):
    monkeypatch.setattr("socket.socket", MockSocket)
    with peary.PearyClient("", proxy_class=MockProxy) as client:
        assert isinstance(client, peary.peary_proxy.PearyProxy)


def test_peary_client_context_manager_enter_socket_connect(monkeypatch):
    monkeypatch.setattr("socket.socket", MockSocket)
    with peary.PearyClient("", proxy_class=MockProxy) as client:
        assert client.socket.is_connected == "as"
        assert client.socket.is_shutdown == "asd"
