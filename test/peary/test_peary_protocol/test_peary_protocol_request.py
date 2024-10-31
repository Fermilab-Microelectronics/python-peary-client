import pytest

from peary.peary_protocol import PearyProtocol


def test_peary_protocol_request_sent_message_without_args(monkeypatch, mock_socket):
    def mock_verify(*_):
        pass

    def mock_send(_, data):
        assert data == PearyProtocol.encode(b"alpha", 1, PearyProtocol.STATUS_OK)
        return len(data)

    def mock_recv_generator():
        yield PearyProtocol.encode(b"", 1, 0)
        yield b""

    recv_generator = mock_recv_generator()

    def mock_recv(*_):
        nonlocal recv_generator
        return next(recv_generator)

    monkeypatch.setattr(PearyProtocol, "_verify_compatible_version", mock_verify)
    monkeypatch.setattr(mock_socket, "send", mock_send)
    monkeypatch.setattr(mock_socket, "recv", mock_recv)
    PearyProtocol(mock_socket("", "")).request("alpha")


def test_peary_protocol_request_sent_message_with_args(monkeypatch, mock_socket):
    def mock_verify(*_):
        pass

    def mock_send(_, data):
        assert data == PearyProtocol.encode(
            b"alpha beta gamma", 1, PearyProtocol.STATUS_OK
        )
        return len(data)

    def mock_recv_generator():
        yield PearyProtocol.encode(b"", 1, 0)
        yield b""

    recv_generator = mock_recv_generator()

    def mock_recv(*_):
        nonlocal recv_generator
        return next(recv_generator)

    monkeypatch.setattr(PearyProtocol, "_verify_compatible_version", mock_verify)
    monkeypatch.setattr(mock_socket, "send", mock_send)
    monkeypatch.setattr(mock_socket, "recv", mock_recv)
    PearyProtocol(mock_socket("", "")).request("alpha", "beta", "gamma")


def test_peary_protocol_request_recieved_response(monkeypatch, mock_socket):
    def mock_verify(*_):
        pass

    def mock_send(_, data):
        return len(data)

    def mock_recv_generator():
        yield PearyProtocol.encode(b"alpha", 1, 0)
        yield b""

    recv_generator = mock_recv_generator()

    def mock_recv(*_):
        nonlocal recv_generator
        return next(recv_generator)

    monkeypatch.setattr(PearyProtocol, "_verify_compatible_version", mock_verify)
    monkeypatch.setattr(mock_socket, "send", mock_send)
    monkeypatch.setattr(mock_socket, "recv", mock_recv)
    assert (
        PearyProtocol(mock_socket("", "")).request("alpha")
        == PearyProtocol.decode(PearyProtocol.encode(b"alpha", 1, 0)).payload
    )


def test_peary_protocol_request_sending_error(monkeypatch, mock_socket):
    def mock_verify(*_):
        pass

    def mock_send(_, data):
        return len(data) - 1

    monkeypatch.setattr(PearyProtocol, "_verify_compatible_version", mock_verify)
    monkeypatch.setattr(mock_socket, "send", mock_send)

    with pytest.raises(
        PearyProtocol.RequestSendError, match="Failed to send request:*"
    ):
        PearyProtocol(mock_socket("", "")).request("")


def test_peary_protocol_request_receive_error(monkeypatch, mock_socket):
    def mock_verify(*_):
        pass

    def mock_recv(*_):
        return b""

    monkeypatch.setattr(PearyProtocol, "_verify_compatible_version", mock_verify)
    monkeypatch.setattr(mock_socket, "recv", mock_recv)

    with pytest.raises(
        PearyProtocol.ResponseReceiveError, match="Failed to receive response."
    ):
        PearyProtocol(mock_socket("", "")).request("")


def test_peary_protocol_request_response_status_error(monkeypatch, mock_socket):
    def mock_verify(*_):
        pass

    def mock_recv_generator():
        yield PearyProtocol.encode(b"", 0, 1)
        yield b""

    recv_generator = mock_recv_generator()

    def mock_recv(*_):
        nonlocal recv_generator
        return next(recv_generator)

    monkeypatch.setattr(PearyProtocol, "_verify_compatible_version", mock_verify)
    monkeypatch.setattr(mock_socket, "recv", mock_recv)

    with pytest.raises(
        PearyProtocol.ResponseStatusError, match="Failed response status 1*"
    ):
        PearyProtocol(mock_socket("", "")).request("")


def test_peary_protocol_request_response_sequence_error(monkeypatch, mock_socket):
    def mock_verify(*_):
        pass

    def mock_recv_generator():
        yield PearyProtocol.encode(b"", 10, 0)
        yield b""

    recv_generator = mock_recv_generator()

    def mock_recv(*_):
        nonlocal recv_generator
        return next(recv_generator)

    monkeypatch.setattr(PearyProtocol, "_verify_compatible_version", mock_verify)
    monkeypatch.setattr(mock_socket, "recv", mock_recv)

    with pytest.raises(
        PearyProtocol.ResponseSequenceError,
        match="Recieved out of order repsonse from*",
    ):
        PearyProtocol(mock_socket("", "")).request("")
