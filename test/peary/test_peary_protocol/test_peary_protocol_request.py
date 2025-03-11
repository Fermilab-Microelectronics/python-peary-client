from __future__ import annotations

import select
from typing import TYPE_CHECKING

import pytest

from peary.peary_protocol import PearyProtocol

if TYPE_CHECKING:
    from collections.abc import Generator
    from socket import socket as socket_type

    from .conftest import MockSocket


def test_peary_protocol_request_sent_message_without_args(
    monkeypatch: pytest.MonkeyPatch, mock_socket: type[MockSocket]
) -> None:
    def mock_verify(_: PearyProtocol) -> None:
        pass

    def mock_send(_: PearyProtocol, data: bytes) -> int:
        assert data == PearyProtocol.encode(b"alpha", 1, PearyProtocol.STATUS_OK)
        return len(data)

    def mock_recv(_: PearyProtocol, *__: bytes) -> bytes:
        return PearyProtocol.encode(b"", 1, 0)

    monkeypatch.setattr(PearyProtocol, "_verify_compatible_version", mock_verify)
    monkeypatch.setattr(mock_socket, "send", mock_send)
    monkeypatch.setattr(mock_socket, "recv", mock_recv)
    PearyProtocol(mock_socket()).request("alpha")


def test_peary_protocol_request_sent_message_with_args(
    monkeypatch: pytest.MonkeyPatch, mock_socket: type[MockSocket]
) -> None:
    def mock_verify(_: PearyProtocol) -> None:
        pass

    def mock_send(_: PearyProtocol, data: bytes) -> int:
        assert data == PearyProtocol.encode(
            b"alpha beta gamma", 1, PearyProtocol.STATUS_OK
        )
        return len(data)

    def mock_recv(_: PearyProtocol, *__: bytes) -> bytes:
        return PearyProtocol.encode(b"", 1, 0)

    monkeypatch.setattr(PearyProtocol, "_verify_compatible_version", mock_verify)
    monkeypatch.setattr(mock_socket, "send", mock_send)
    monkeypatch.setattr(mock_socket, "recv", mock_recv)
    PearyProtocol(mock_socket()).request("alpha", "beta", "gamma")


def test_peary_protocol_request_sending_error(
    monkeypatch: pytest.MonkeyPatch, mock_socket: type[MockSocket]
) -> None:
    def mock_verify(_: PearyProtocol) -> None:
        pass

    def mock_send(_: PearyProtocol, data: bytes) -> int:
        return len(data) - 1

    monkeypatch.setattr(PearyProtocol, "_verify_compatible_version", mock_verify)
    monkeypatch.setattr(mock_socket, "send", mock_send)

    with pytest.raises(
        PearyProtocol.RequestSendError, match="Failed to send request:*"
    ):
        PearyProtocol(mock_socket()).request("")


def test_peary_protocol_request_recieved_response_buffer_oversized(
    monkeypatch: pytest.MonkeyPatch, mock_socket: type[MockSocket]
) -> None:
    def mock_verify(_: PearyProtocol) -> None:
        pass

    def mock_send(_: PearyProtocol, data: bytes) -> int:
        return len(data)

    def mock_recv(_: PearyProtocol, *__: bytes) -> bytes:
        return PearyProtocol.encode(b"alpha", 1, 0)

    monkeypatch.setattr(PearyProtocol, "_verify_compatible_version", mock_verify)
    monkeypatch.setattr(mock_socket, "send", mock_send)
    monkeypatch.setattr(mock_socket, "recv", mock_recv)
    assert (
        PearyProtocol(mock_socket()).request("alpha", buffer_size=4096)
        == PearyProtocol.decode(PearyProtocol.encode(b"alpha", 1, 0)).payload
    )


def test_peary_protocol_request_recieved_response_buffer_undersized(
    monkeypatch: pytest.MonkeyPatch, mock_socket: type[MockSocket]
) -> None:
    enocded_message = PearyProtocol.encode(b"alpha", 1, 0)

    def mock_verify(_: PearyProtocol) -> None:
        pass

    select_counter = iter(range(len(enocded_message)))

    def mock_select(
        rlist: list[socket_type], *_: list[socket_type]
    ) -> tuple[list, ...]:
        if next(select_counter) < len(enocded_message) - 1:
            return rlist, [], []
        else:
            return [], [], []

    def mock_send(_: PearyProtocol, data: bytes) -> int:
        return len(data)

    def mock_recv_generator() -> Generator:
        for byte_char in enocded_message:
            yield [byte_char]

    recv_generator = mock_recv_generator()

    def mock_recv(_: PearyProtocol, *__: bytes) -> bytes:
        nonlocal recv_generator
        return next(recv_generator)

    monkeypatch.setattr(PearyProtocol, "_verify_compatible_version", mock_verify)
    monkeypatch.setattr(select, "select", mock_select)
    monkeypatch.setattr(mock_socket, "send", mock_send)
    monkeypatch.setattr(mock_socket, "recv", mock_recv)
    assert (
        PearyProtocol(mock_socket()).request("alpha", buffer_size=1)
        == PearyProtocol.decode(enocded_message).payload
    )


def test_peary_protocol_request_receive_error(
    monkeypatch: pytest.MonkeyPatch, mock_socket: type[MockSocket]
) -> None:
    def mock_verify(_: PearyProtocol) -> None:
        pass

    def mock_recv(_: PearyProtocol, *__: bytes) -> bytes:
        return b""

    monkeypatch.setattr(PearyProtocol, "_verify_compatible_version", mock_verify)
    monkeypatch.setattr(mock_socket, "recv", mock_recv)

    with pytest.raises(
        PearyProtocol.ResponseReceiveError, match="Failed to receive response."
    ):
        PearyProtocol(mock_socket()).request("")


def test_peary_protocol_request_response_status_error(
    monkeypatch: pytest.MonkeyPatch, mock_socket: type[MockSocket]
) -> None:
    def mock_verify(_: PearyProtocol) -> None:
        pass

    def mock_recv_generator() -> Generator:
        yield PearyProtocol.encode(b"", 0, 1)

    recv_generator = mock_recv_generator()

    def mock_recv(_: PearyProtocol, *__: bytes) -> bytes:
        nonlocal recv_generator
        return next(recv_generator)

    monkeypatch.setattr(PearyProtocol, "_verify_compatible_version", mock_verify)
    monkeypatch.setattr(mock_socket, "recv", mock_recv)

    with pytest.raises(
        PearyProtocol.ResponseStatusError, match="Failed response status 1*"
    ):
        PearyProtocol(mock_socket()).request("")


def test_peary_protocol_request_response_sequence_error(
    monkeypatch: pytest.MonkeyPatch, mock_socket: type[MockSocket]
) -> None:
    def mock_verify(_: PearyProtocol) -> None:
        pass

    def mock_recv_generator() -> Generator:
        yield PearyProtocol.encode(b"", 10, 0)

    recv_generator = mock_recv_generator()

    def mock_recv(_: PearyProtocol, *__: bytes) -> bytes:
        nonlocal recv_generator
        return next(recv_generator)

    monkeypatch.setattr(PearyProtocol, "_verify_compatible_version", mock_verify)
    monkeypatch.setattr(mock_socket, "recv", mock_recv)

    with pytest.raises(
        PearyProtocol.ResponseSequenceError,
        match="Recieved out of order repsonse from*",
    ):
        PearyProtocol(mock_socket()).request("")
