from __future__ import annotations

import select
from typing import TYPE_CHECKING

import pytest

from peary.peary_protocol import PearyProtocol

if TYPE_CHECKING:
    from collections.abc import Callable
    from socket import socket as socket_type


def test_peary_protocol_recv_buffer_oversized(mock_socket: Callable) -> None:
    encoded_message = PearyProtocol.encode(b"alpha", 1, PearyProtocol.STATUS_OK)
    fake_socket = mock_socket(mock_recv=lambda _: encoded_message)
    assert (
        PearyProtocol(fake_socket(), checks=PearyProtocol.Checks.CHECK_NONE).request(
            "alpha", buffer_size=len(encoded_message) + 1
        )
        == b"alpha"
    )


def test_peary_protocol_recv_buffer_equalsized(
    monkeypatch: pytest.MonkeyPatch, mock_socket: Callable
) -> None:
    encoded_message = PearyProtocol.encode(b"alpha", 1, PearyProtocol.STATUS_OK)
    fake_socket = mock_socket(mock_recv=lambda _: encoded_message)

    def mock_select(*_: list[socket_type]) -> tuple[list, ...]:
        return [], [], []

    monkeypatch.setattr(select, "select", mock_select)
    assert (
        PearyProtocol(fake_socket(), checks=PearyProtocol.Checks.CHECK_NONE).request(
            "alpha", buffer_size=len(encoded_message)
        )
        == b"alpha"
    )


def test_peary_protocol_recv_buffer_undersized(
    monkeypatch: pytest.MonkeyPatch, mock_socket: Callable
) -> None:
    encoded_message = PearyProtocol.encode(b"alpha", 1, PearyProtocol.STATUS_OK)
    mock_select_generator = iter(range(len(encoded_message)))
    mock_recv_generator = iter(bytes([ii]) for ii in encoded_message)
    fake_socket = mock_socket(mock_recv=lambda _: next(mock_recv_generator))

    def mock_select(
        rlist: list[socket_type], *_: list[socket_type]
    ) -> tuple[list, ...]:
        if next(mock_select_generator) < len(encoded_message) - 1:
            return rlist, [], []
        else:
            return [], [], []

    monkeypatch.setattr(select, "select", mock_select)
    assert (
        PearyProtocol(fake_socket(), checks=PearyProtocol.Checks.CHECK_NONE).request(
            "alpha", buffer_size=1
        )
        == b"alpha"
    )


def test_peary_protocol_recv_error(mock_socket: Callable) -> None:
    fake_socket = mock_socket(mock_recv=lambda _: b"")

    with pytest.raises(
        PearyProtocol.ResponseReceiveError, match="Failed to receive response."
    ):
        PearyProtocol(fake_socket(), checks=PearyProtocol.Checks.CHECK_NONE).request("")
