from __future__ import annotations

import select
import socket as socket_module
from typing import TYPE_CHECKING

import pytest

from peary.peary_protocol import PearyProtocol

if TYPE_CHECKING:
    from collections.abc import Generator
    from socket import socket as socket_type

    from typing_extensions import Buffer


# ruff: noqa: ARG002
# pylint: disable=W0613
class MockSocket(socket_module.socket):

    def recv(self, size: int, flags: int = 0) -> bytes:
        return b""

    def send(self, data: Buffer, flags: int = 0) -> int:
        return len(bytes(data))

    def settimeout(self, value: float | None = None) -> None:
        pass


def test_peary_protocol_request_sent_message_without_args(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    def mock_verify(_: PearyProtocol) -> None:
        pass

    def mock_send(_: PearyProtocol, data: bytes) -> int:
        assert data == PearyProtocol.encode(b"alpha", 1, PearyProtocol.STATUS_OK)
        return len(data)

    def mock_recv(_: PearyProtocol, *__: bytes) -> bytes:
        return PearyProtocol.encode(b"", 1, 0)

    monkeypatch.setattr(PearyProtocol, "_verify_compatible_version", mock_verify)
    monkeypatch.setattr(MockSocket, "send", mock_send)
    monkeypatch.setattr(MockSocket, "recv", mock_recv)
    PearyProtocol(MockSocket()).request("alpha")


def test_peary_protocol_request_sent_message_with_args(
    monkeypatch: pytest.MonkeyPatch,
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
    monkeypatch.setattr(MockSocket, "send", mock_send)
    monkeypatch.setattr(MockSocket, "recv", mock_recv)
    PearyProtocol(MockSocket()).request("alpha", "beta", "gamma")


def test_peary_protocol_request_sending_error(monkeypatch: pytest.MonkeyPatch) -> None:
    def mock_verify(_: PearyProtocol) -> None:
        pass

    def mock_send(_: PearyProtocol, data: bytes) -> int:
        return len(data) - 1

    monkeypatch.setattr(PearyProtocol, "_verify_compatible_version", mock_verify)
    monkeypatch.setattr(MockSocket, "send", mock_send)

    with pytest.raises(
        PearyProtocol.RequestSendError, match="Failed to send request:*"
    ):
        PearyProtocol(MockSocket()).request("")


def test_peary_protocol_request_recieved_response_buffer_oversized(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    def mock_verify(_: PearyProtocol) -> None:
        pass

    def mock_send(_: PearyProtocol, data: bytes) -> int:
        return len(data)

    def mock_recv(_: PearyProtocol, *__: bytes) -> bytes:
        return PearyProtocol.encode(b"alpha", 1, 0)

    monkeypatch.setattr(PearyProtocol, "_verify_compatible_version", mock_verify)
    monkeypatch.setattr(MockSocket, "send", mock_send)
    monkeypatch.setattr(MockSocket, "recv", mock_recv)
    assert (
        PearyProtocol(MockSocket()).request("alpha", buffer_size=4096)
        == PearyProtocol.decode(PearyProtocol.encode(b"alpha", 1, 0)).payload
    )


def test_peary_protocol_request_recieved_response_buffer_undersized(
    monkeypatch: pytest.MonkeyPatch,
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
    monkeypatch.setattr(MockSocket, "send", mock_send)
    monkeypatch.setattr(MockSocket, "recv", mock_recv)
    assert (
        PearyProtocol(MockSocket()).request("alpha", buffer_size=1)
        == PearyProtocol.decode(enocded_message).payload
    )


def test_peary_protocol_request_receive_error(monkeypatch: pytest.MonkeyPatch) -> None:
    def mock_verify(_: PearyProtocol) -> None:
        pass

    def mock_recv(_: PearyProtocol, *__: bytes) -> bytes:
        return b""

    monkeypatch.setattr(PearyProtocol, "_verify_compatible_version", mock_verify)
    monkeypatch.setattr(MockSocket, "recv", mock_recv)

    with pytest.raises(
        PearyProtocol.ResponseReceiveError, match="Failed to receive response."
    ):
        PearyProtocol(MockSocket()).request("")


def test_peary_protocol_request_response_status_error(
    monkeypatch: pytest.MonkeyPatch,
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
    monkeypatch.setattr(MockSocket, "recv", mock_recv)

    with pytest.raises(
        PearyProtocol.ResponseStatusError, match="Failed response status 1*"
    ):
        PearyProtocol(MockSocket()).request("")


def test_peary_protocol_request_response_sequence_error(
    monkeypatch: pytest.MonkeyPatch,
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
    monkeypatch.setattr(MockSocket, "recv", mock_recv)

    with pytest.raises(
        PearyProtocol.ResponseSequenceError,
        match="Recieved out of order repsonse from*",
    ):
        PearyProtocol(MockSocket()).request("")
