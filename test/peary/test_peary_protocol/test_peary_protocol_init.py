from __future__ import annotations

from typing import TYPE_CHECKING

from peary.peary_protocol import PearyProtocol

if TYPE_CHECKING:
    from .conftest import MockSocket


class VerifiedPearyProtocol(PearyProtocol):
    """An extended PearyProtocol that bypasses compatibility checks."""

    def _verify_compatible_version(self) -> None:
        pass


def test_peary_protocol_init_timeout_default(mock_socket: type[MockSocket]) -> None:
    mock_socket().settimeout(None)
    assert mock_socket.timeout is None
    VerifiedPearyProtocol(mock_socket())
    assert mock_socket.timeout == 1


def test_peary_protocol_init_timeout_nondefault(mock_socket: type[MockSocket]) -> None:
    mock_socket().settimeout(None)
    assert mock_socket.timeout is None
    VerifiedPearyProtocol(mock_socket(), timeout=100)
    assert mock_socket.timeout == 100
