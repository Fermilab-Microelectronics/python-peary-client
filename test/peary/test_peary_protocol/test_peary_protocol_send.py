from __future__ import annotations

from typing import TYPE_CHECKING

import pytest

from peary.peary_protocol import PearyProtocol

if TYPE_CHECKING:
    from .conftest import MockSocket


class VerifiedPearyProtocol(PearyProtocol):
    """An extended PearyProtocol that bypasses compatibility checks."""

    def _verify_compatible_version(self) -> None:
        pass


def test_peary_protocol_request_send_okay(
    monkeypatch: pytest.MonkeyPatch, mock_socket: type[MockSocket]
) -> None:
    def mock_send(_self: PearyProtocol, data: bytes) -> int:
        return len(data)

    monkeypatch.setattr(mock_socket, "send", mock_send)
    VerifiedPearyProtocol(mock_socket()).request("")


def test_peary_protocol_request_send_error(
    monkeypatch: pytest.MonkeyPatch, mock_socket: type[MockSocket]
) -> None:
    def mock_send(_self: PearyProtocol, data: bytes) -> int:
        return len(data) - 1

    monkeypatch.setattr(mock_socket, "send", mock_send)
    with pytest.raises(
        PearyProtocol.RequestSendError, match="Failed to send request:*"
    ):
        VerifiedPearyProtocol(mock_socket()).request("")
