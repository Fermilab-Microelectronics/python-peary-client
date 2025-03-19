from __future__ import annotations

from typing import TYPE_CHECKING

from peary.peary_protocol import PearyProtocol

if TYPE_CHECKING:
    from .conftest import MockSocket


def test_peary_protocol_init_timeout_default(mock_socket: type[MockSocket]) -> None:
    mock_socket.timeout = None
    PearyProtocol(mock_socket(), checks=PearyProtocol.Checks.CHECK_NONE)
    assert mock_socket.timeout == 1


def test_peary_protocol_init_timeout_nondefault(mock_socket: type[MockSocket]) -> None:
    mock_socket.timeout = None
    PearyProtocol(mock_socket(), timeout=100, checks=PearyProtocol.Checks.CHECK_NONE)
    assert mock_socket.timeout == 100
