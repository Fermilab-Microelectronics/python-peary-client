import pytest

from peary.peary_protocol import PearyProtocol


def test_peary_protocol_init_timeout_default(monkeypatch, mock_socket):
    def mock_verify(*_):
        pass

    monkeypatch.setattr(PearyProtocol, "_verify_compatible_version", mock_verify)
    PearyProtocol(mock_socket("", ""))
    assert mock_socket.timeout == 10


def test_peary_protocol_init_timeout_nondefault(monkeypatch, mock_socket):
    def mock_verify(*_):
        pass

    monkeypatch.setattr(PearyProtocol, "_verify_compatible_version", mock_verify)
    PearyProtocol(mock_socket("", ""), timeout=100)
    assert mock_socket.timeout == 100


def test_peary_protocol_init_version_supported(monkeypatch, mock_socket):
    def mock_request_protocol_version(_, msg):
        assert msg == "protocol_version"
        return b"1"

    monkeypatch.setattr(PearyProtocol, "request", mock_request_protocol_version)
    PearyProtocol(mock_socket("", ""))


def test_peary_protocol_init_version_unsupported(monkeypatch, mock_socket):
    def mock_request_protocol_version(_, msg):
        assert msg == "protocol_version"
        return b"0"

    monkeypatch.setattr(PearyProtocol, "request", mock_request_protocol_version)
    with pytest.raises(
        PearyProtocol.IncompatibleProtocolError,
        match="Unsupported protocol version: b'0'",
    ):
        PearyProtocol(mock_socket("", ""))
