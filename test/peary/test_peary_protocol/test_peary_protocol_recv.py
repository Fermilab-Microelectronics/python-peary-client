from __future__ import annotations

import select
from typing import TYPE_CHECKING

import pytest

from peary.peary_protocol import PearyProtocol

if TYPE_CHECKING:
    from socket import socket as socket_type

    from .conftest import MockSocket


class VerifiedPearyProtocol(PearyProtocol):
    """An extended PearyProtocol that bypasses compatibility checks."""

    def _verify_compatible_version(self) -> None:
        pass


def test_peary_protocol_request_recieved_response_buffer_oversized(
    monkeypatch: pytest.MonkeyPatch, mock_socket: type[MockSocket]
) -> None:
    encoded_message = PearyProtocol.encode(b"alpha", 1, PearyProtocol.STATUS_OK)

    def mock_recv(_self: PearyProtocol, _size: int) -> bytes:
        return encoded_message

    monkeypatch.setattr(mock_socket, "recv", mock_recv)
    assert (
        VerifiedPearyProtocol(mock_socket()).request(
            "alpha", buffer_size=len(encoded_message) + 1
        )
        == b"alpha"
    )


def test_peary_protocol_request_recieved_response_buffer_equalsized(
    monkeypatch: pytest.MonkeyPatch, mock_socket: type[MockSocket]
) -> None:
    encoded_message = PearyProtocol.encode(b"alpha", 1, PearyProtocol.STATUS_OK)

    def mock_select(*_: list[socket_type]) -> tuple[list, ...]:
        return [], [], []

    def mock_recv(_self: PearyProtocol, _size: int) -> bytes:
        return encoded_message

    monkeypatch.setattr(select, "select", mock_select)
    monkeypatch.setattr(mock_socket, "recv", mock_recv)
    assert (
        VerifiedPearyProtocol(mock_socket()).request(
            "alpha", buffer_size=len(encoded_message)
        )
        == b"alpha"
    )


def test_peary_protocol_request_recieved_response_buffer_undersized(
    monkeypatch: pytest.MonkeyPatch, mock_socket: type[MockSocket]
) -> None:
    encoded_message = PearyProtocol.encode(b"alpha", 1, PearyProtocol.STATUS_OK)
    mock_select_generator = iter(range(len(encoded_message)))
    mock_recv_generator = iter(bytes([ii]) for ii in encoded_message)

    def mock_select(
        rlist: list[socket_type], *_: list[socket_type]
    ) -> tuple[list, ...]:
        if next(mock_select_generator) < len(encoded_message) - 1:
            return rlist, [], []
        else:
            return [], [], []

    def mock_recv(_self: PearyProtocol, _size: int) -> bytes:
        return next(mock_recv_generator)

    monkeypatch.setattr(select, "select", mock_select)
    monkeypatch.setattr(mock_socket, "recv", mock_recv)
    assert (
        VerifiedPearyProtocol(mock_socket()).request("alpha", buffer_size=1) == b"alpha"
    )


def test_peary_protocol_request_receive_error(
    monkeypatch: pytest.MonkeyPatch, mock_socket: type[MockSocket]
) -> None:
    def mock_recv(_self: PearyProtocol, _size: int) -> bytes:
        return b""

    monkeypatch.setattr(mock_socket, "recv", mock_recv)
    with pytest.raises(
        PearyProtocol.ResponseReceiveError, match="Failed to receive response."
    ):
        VerifiedPearyProtocol(mock_socket()).request("")
