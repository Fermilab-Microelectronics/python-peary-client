from __future__ import annotations

from typing import TYPE_CHECKING

import pytest

from peary.peary_protocol import PearyProtocol

if TYPE_CHECKING:
    from .conftest import MockSocket


def test_peary_protocol_request_send_message_without_args(
    monkeypatch: pytest.MonkeyPatch, mock_socket: type[MockSocket]
) -> None:

    def mock_send(_self: PearyProtocol, data: bytes) -> int:
        assert data == PearyProtocol.encode(b"alpha", 1, PearyProtocol.STATUS_OK)
        return len(data)

    monkeypatch.setattr(mock_socket, "send", mock_send)
    PearyProtocol(mock_socket(), checks=PearyProtocol.Checks.CHECK_NONE).request(
        "alpha"
    )


def test_peary_protocol_request_send_message_with_args(
    monkeypatch: pytest.MonkeyPatch, mock_socket: type[MockSocket]
) -> None:
    def mock_send(_self: PearyProtocol, data: bytes) -> int:
        assert data == PearyProtocol.encode(
            b"alpha beta gamma", 1, PearyProtocol.STATUS_OK
        )
        return len(data)

    monkeypatch.setattr(mock_socket, "send", mock_send)
    PearyProtocol(mock_socket(), checks=PearyProtocol.Checks.CHECK_NONE).request(
        "alpha", "beta", "gamma"
    )


def test_peary_protocol_request_response_status_okay(
    monkeypatch: pytest.MonkeyPatch, mock_socket: type[MockSocket]
) -> None:
    def mock_recv(_self: PearyProtocol, _size: int) -> bytes:
        return PearyProtocol.encode(b"", 1, PearyProtocol.STATUS_OK)

    monkeypatch.setattr(mock_socket, "recv", mock_recv)
    PearyProtocol(mock_socket(), checks=PearyProtocol.Checks.CHECK_NONE).request("")


def test_peary_protocol_request_response_status_error(
    monkeypatch: pytest.MonkeyPatch, mock_socket: type[MockSocket]
) -> None:
    def mock_recv(_self: PearyProtocol, _size: int) -> bytes:
        return PearyProtocol.encode(b"", 1, not PearyProtocol.STATUS_OK)

    monkeypatch.setattr(mock_socket, "recv", mock_recv)
    with pytest.raises(
        PearyProtocol.ResponseStatusError, match="Failed response status 1*"
    ):
        PearyProtocol(mock_socket(), checks=PearyProtocol.Checks.CHECK_NONE).request("")


def test_peary_protocol_request_response_sequence_okay(
    monkeypatch: pytest.MonkeyPatch, mock_socket: type[MockSocket]
) -> None:
    num_requests = 10
    mock_recv_generator = (
        PearyProtocol.encode(b"", ii + 1, PearyProtocol.STATUS_OK)
        for ii in range(num_requests)
    )

    def mock_recv(_self: PearyProtocol, _size: int) -> bytes:
        return next(mock_recv_generator)

    monkeypatch.setattr(mock_socket, "recv", mock_recv)
    protocol = PearyProtocol(mock_socket(), checks=PearyProtocol.Checks.CHECK_NONE)
    for _ in range(num_requests):
        protocol.request("")


def test_peary_protocol_request_response_sequence_error(
    monkeypatch: pytest.MonkeyPatch, mock_socket: type[MockSocket]
) -> None:

    def mock_recv(_self: PearyProtocol, _size: int) -> bytes:
        return PearyProtocol.encode(b"", 0, PearyProtocol.STATUS_OK)

    monkeypatch.setattr(mock_socket, "recv", mock_recv)
    with pytest.raises(
        PearyProtocol.ResponseSequenceError,
        match="Recieved out of order repsonse from*",
    ):
        PearyProtocol(mock_socket(), checks=PearyProtocol.Checks.CHECK_NONE).request("")
