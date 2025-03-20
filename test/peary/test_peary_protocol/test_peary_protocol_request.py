from __future__ import annotations

from typing import TYPE_CHECKING

import pytest

from peary.peary_protocol import PearyProtocol

if TYPE_CHECKING:
    from collections.abc import Callable


def test_peary_protocol_request_send_message_without_args(
    mock_socket: Callable,
) -> None:

    def mock_send(data: bytes) -> int:
        assert data == PearyProtocol.encode(b"alpha", 1, PearyProtocol.STATUS_OK)
        return len(data)

    fake_socket = mock_socket(mock_send=mock_send)
    PearyProtocol(fake_socket(), checks=PearyProtocol.Checks.CHECK_NONE).request(
        "alpha"
    )


def test_peary_protocol_request_send_message_with_args(mock_socket: Callable) -> None:
    def mock_send(data: bytes) -> int:
        assert data == PearyProtocol.encode(
            b"alpha beta gamma", 1, PearyProtocol.STATUS_OK
        )
        return len(data)

    fake_socket = mock_socket(mock_send=mock_send)
    PearyProtocol(fake_socket(), checks=PearyProtocol.Checks.CHECK_NONE).request(
        "alpha", "beta", "gamma"
    )


def test_peary_protocol_request_response_status_okay(mock_socket: Callable) -> None:
    fake_socket = mock_socket(
        mock_recv=lambda _: PearyProtocol.encode(b"", 1, PearyProtocol.STATUS_OK)
    )
    PearyProtocol(fake_socket(), checks=PearyProtocol.Checks.CHECK_NONE).request("")


def test_peary_protocol_request_response_status_error(mock_socket: Callable) -> None:
    def mock_recv(_: int) -> bytes:
        return PearyProtocol.encode(b"", 1, not PearyProtocol.STATUS_OK)

    fake_socket = mock_socket(mock_recv=mock_recv)
    with pytest.raises(
        PearyProtocol.ResponseStatusError, match="Failed response status 1*"
    ):
        PearyProtocol(fake_socket(), checks=PearyProtocol.Checks.CHECK_NONE).request("")


def test_peary_protocol_request_response_sequence_okay(mock_socket: Callable) -> None:
    num_requests = 10
    mock_recv_generator = (
        PearyProtocol.encode(b"", ii + 1, PearyProtocol.STATUS_OK)
        for ii in range(num_requests)
    )

    def mock_recv(_: int) -> bytes:
        return next(mock_recv_generator)

    fake_socket = mock_socket(mock_recv=mock_recv)
    protocol = PearyProtocol(fake_socket(), checks=PearyProtocol.Checks.CHECK_NONE)
    for _ in range(num_requests):
        protocol.request("")


def test_peary_protocol_request_response_sequence_error(mock_socket: Callable) -> None:

    def mock_recv(_: int) -> bytes:
        return PearyProtocol.encode(b"", 0, PearyProtocol.STATUS_OK)

    fake_socket = mock_socket(mock_recv=mock_recv)
    with pytest.raises(
        PearyProtocol.ResponseSequenceError,
        match="Recieved out of order repsonse from*",
    ):
        PearyProtocol(fake_socket(), checks=PearyProtocol.Checks.CHECK_NONE).request("")
