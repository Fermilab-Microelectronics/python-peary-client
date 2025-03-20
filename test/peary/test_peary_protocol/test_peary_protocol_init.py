from __future__ import annotations

from typing import TYPE_CHECKING

from peary.peary_protocol import PearyProtocol

if TYPE_CHECKING:
    from collections.abc import Callable


def test_peary_protocol_init_timeout_default(mock_socket: Callable) -> None:
    fake_socket = mock_socket()
    fake_socket.timeout = None
    PearyProtocol(fake_socket(), checks=PearyProtocol.Checks.CHECK_NONE)
    assert fake_socket.timeout == 1


def test_peary_protocol_init_timeout_nondefault(mock_socket: Callable) -> None:
    fake_socket = mock_socket()
    fake_socket.timeout = None
    PearyProtocol(fake_socket(), timeout=100, checks=PearyProtocol.Checks.CHECK_NONE)
    assert fake_socket.timeout == 100
