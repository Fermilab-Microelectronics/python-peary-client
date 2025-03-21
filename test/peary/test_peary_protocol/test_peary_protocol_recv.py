from __future__ import annotations

from typing import TYPE_CHECKING

import pytest

from peary.peary_protocol import PearyProtocol

if TYPE_CHECKING:
    from collections.abc import Callable
    from socket import socket as socket_type


def test_peary_protocol_recv_buffer_oversized(patch_socket: Callable) -> None:
    encoded_message = PearyProtocol.encode(b"alpha", 1, PearyProtocol.STATUS_OK)
    with patch_socket(mock_recv=lambda _: encoded_message) as socket_class:
        assert (
            PearyProtocol(
                socket_class(), checks=PearyProtocol.Checks.CHECK_NONE
            ).request("alpha", buffer_size=len(encoded_message) + 1)
            == b"alpha"
        )


def test_peary_protocol_recv_buffer_equalsized(patch_socket: Callable) -> None:
    encoded_message = PearyProtocol.encode(b"alpha", 1, PearyProtocol.STATUS_OK)
    with patch_socket(
        mock_recv=lambda _: encoded_message, mock_select=lambda *_: ([], [], [])
    ) as socket_class:
        assert (
            PearyProtocol(
                socket_class(), checks=PearyProtocol.Checks.CHECK_NONE
            ).request("alpha", buffer_size=len(encoded_message))
            == b"alpha"
        )


def test_peary_protocol_recv_buffer_undersized(patch_socket: Callable) -> None:
    encoded_message = PearyProtocol.encode(b"alpha", 1, PearyProtocol.STATUS_OK)
    mock_recv_generator = iter(bytes([ii]) for ii in encoded_message)
    mock_select_generator = iter(range(len(encoded_message)))

    def mock_recv(_: int) -> bytes:
        return next(mock_recv_generator)

    def mock_select(
        rlist: list[socket_type], *_: list[socket_type]
    ) -> tuple[list, ...]:
        if next(mock_select_generator) < len(encoded_message) - 1:
            return rlist, [], []
        else:
            return [], [], []

    with patch_socket(mock_recv=mock_recv, mock_select=mock_select) as socket_class:
        assert (
            PearyProtocol(
                socket_class(), checks=PearyProtocol.Checks.CHECK_NONE
            ).request("alpha", buffer_size=1)
            == b"alpha"
        )


def test_peary_protocol_recv_error(patch_socket: Callable) -> None:
    with patch_socket(mock_recv=lambda _: b"") as socket_class:
        with pytest.raises(
            PearyProtocol.ResponseReceiveError, match="Failed to receive response."
        ):
            PearyProtocol(
                socket_class(), checks=PearyProtocol.Checks.CHECK_NONE
            ).request("")
