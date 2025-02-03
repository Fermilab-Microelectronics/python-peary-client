import pytest

from peary.peary_protocol import PearyProtocol


class MockSocket:
    timeout = None

    def __init__(self, *args, **kwargs):
        pass

    def settimeout(self, value):
        MockSocket.timeout = value


def test_peary_protocol_init_timeout_default(monkeypatch):
    def mock_verify(*_):
        pass

    monkeypatch.setattr(PearyProtocol, "_verify_compatible_version", mock_verify)
    PearyProtocol(MockSocket())
    assert MockSocket.timeout == 1


def test_peary_protocol_init_timeout_nondefault(monkeypatch):
    def mock_verify(*_):
        pass

    monkeypatch.setattr(PearyProtocol, "_verify_compatible_version", mock_verify)
    PearyProtocol(MockSocket(), timeout=100)
    assert MockSocket.timeout == 100


def test_peary_protocol_init_version_supported(monkeypatch):
    def mock_request_protocol_version(_, msg):
        assert msg == "protocol_version"
        return b"1"

    monkeypatch.setattr(PearyProtocol, "request", mock_request_protocol_version)
    PearyProtocol(MockSocket())


def test_peary_protocol_init_version_unsupported(monkeypatch):
    def mock_request_protocol_version(_, msg):
        assert msg == "protocol_version"
        return b"0"

    monkeypatch.setattr(PearyProtocol, "request", mock_request_protocol_version)
    with pytest.raises(
        PearyProtocol.IncompatibleProtocolError,
        match="Unsupported protocol version: b'0'",
    ):
        PearyProtocol(MockSocket())
