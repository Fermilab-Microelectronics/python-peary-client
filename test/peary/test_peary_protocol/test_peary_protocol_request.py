import select

import pytest

from peary.peary_protocol import PearyProtocol


class MockSocket:
    def __init__(self, *args, **kwargs):
        """mock init"""

    def recv(self, *args):
        """mock recv"""

    def send(self, data):
        return len(data)

    def settimeout(self, *args):
        """mock settimeout"""


def test_peary_protocol_request_sent_message_without_args(monkeypatch):
    def mock_verify(*_):
        pass

    def mock_send(_, data):
        assert data == PearyProtocol.encode(b"alpha", 1, PearyProtocol.STATUS_OK)
        return len(data)

    def mock_recv(*_):
        return PearyProtocol.encode(b"", 1, 0)

    monkeypatch.setattr(PearyProtocol, "_verify_compatible_version", mock_verify)
    monkeypatch.setattr(MockSocket, "send", mock_send)
    monkeypatch.setattr(MockSocket, "recv", mock_recv)
    PearyProtocol(MockSocket()).request("alpha")


def test_peary_protocol_request_sent_message_with_args(monkeypatch):
    def mock_verify(*_):
        pass

    def mock_send(_, data):
        assert data == PearyProtocol.encode(
            b"alpha beta gamma", 1, PearyProtocol.STATUS_OK
        )
        return len(data)

    def mock_recv(*_):
        return PearyProtocol.encode(b"", 1, 0)

    monkeypatch.setattr(PearyProtocol, "_verify_compatible_version", mock_verify)
    monkeypatch.setattr(MockSocket, "send", mock_send)
    monkeypatch.setattr(MockSocket, "recv", mock_recv)
    PearyProtocol(MockSocket()).request("alpha", "beta", "gamma")


def test_peary_protocol_request_sending_error(monkeypatch):
    def mock_verify(*_):
        pass

    def mock_send(_, data):
        return len(data) - 1

    monkeypatch.setattr(PearyProtocol, "_verify_compatible_version", mock_verify)
    monkeypatch.setattr(MockSocket, "send", mock_send)

    with pytest.raises(
        PearyProtocol.RequestSendError, match="Failed to send request:*"
    ):
        PearyProtocol(MockSocket()).request("")


def test_peary_protocol_request_recieved_response_buffer_oversized(monkeypatch):
    def mock_verify(*_):
        pass

    def mock_send(_, data):
        return len(data)

    def mock_recv(*_):
        return PearyProtocol.encode(b"alpha", 1, 0)

    monkeypatch.setattr(PearyProtocol, "_verify_compatible_version", mock_verify)
    monkeypatch.setattr(MockSocket, "send", mock_send)
    monkeypatch.setattr(MockSocket, "recv", mock_recv)
    assert (
        PearyProtocol(MockSocket()).request("alpha", buffer_size=4096)
        == PearyProtocol.decode(PearyProtocol.encode(b"alpha", 1, 0)).payload
    )


def test_peary_protocol_request_recieved_response_buffer_undersized(monkeypatch):
    enocded_message = PearyProtocol.encode(b"alpha", 1, 0)

    def mock_verify(*_):
        pass

    select_counter = iter(range(len(enocded_message)))

    def mock_select(rlist, *_):
        if next(select_counter) < len(enocded_message) - 1:
            return rlist, [], []
        else:
            return [], [], []

    def mock_send(_, data):
        return len(data)

    def mock_recv_generator():
        for byte_char in enocded_message:
            yield [byte_char]

    recv_generator = mock_recv_generator()

    def mock_recv(*_):
        nonlocal recv_generator
        return next(recv_generator)

    monkeypatch.setattr(PearyProtocol, "_verify_compatible_version", mock_verify)
    monkeypatch.setattr(select, "select", mock_select)
    monkeypatch.setattr(MockSocket, "send", mock_send)
    monkeypatch.setattr(MockSocket, "recv", mock_recv)
    assert (
        PearyProtocol(MockSocket()).request("alpha", buffer_size=1)
        == PearyProtocol.decode(enocded_message).payload
    )


def test_peary_protocol_request_receive_error(monkeypatch):
    def mock_verify(*_):
        pass

    def mock_recv(*_):
        return b""

    monkeypatch.setattr(PearyProtocol, "_verify_compatible_version", mock_verify)
    monkeypatch.setattr(MockSocket, "recv", mock_recv)

    with pytest.raises(
        PearyProtocol.ResponseReceiveError, match="Failed to receive response."
    ):
        PearyProtocol(MockSocket()).request("")


def test_peary_protocol_request_response_status_error(monkeypatch):
    def mock_verify(*_):
        pass

    def mock_recv_generator():
        yield PearyProtocol.encode(b"", 0, 1)

    recv_generator = mock_recv_generator()

    def mock_recv(*_):
        nonlocal recv_generator
        return next(recv_generator)

    monkeypatch.setattr(PearyProtocol, "_verify_compatible_version", mock_verify)
    monkeypatch.setattr(MockSocket, "recv", mock_recv)

    with pytest.raises(
        PearyProtocol.ResponseStatusError, match="Failed response status 1*"
    ):
        PearyProtocol(MockSocket()).request("")


def test_peary_protocol_request_response_sequence_error(monkeypatch):
    def mock_verify(*_):
        pass

    def mock_recv_generator():
        yield PearyProtocol.encode(b"", 10, 0)

    recv_generator = mock_recv_generator()

    def mock_recv(*_):
        nonlocal recv_generator
        return next(recv_generator)

    monkeypatch.setattr(PearyProtocol, "_verify_compatible_version", mock_verify)
    monkeypatch.setattr(MockSocket, "recv", mock_recv)

    with pytest.raises(
        PearyProtocol.ResponseSequenceError,
        match="Recieved out of order repsonse from*",
    ):
        PearyProtocol(MockSocket()).request("")
