from __future__ import annotations

import socket
from typing import TYPE_CHECKING

from caribou.caribou_board import CaribouBoard
from peary.peary_protocol import PearyProtocol

if TYPE_CHECKING:
    import pytest


class MockProtocol(PearyProtocol):
    """A Mock Peary Protocol."""

    def _verify_compatible_version(self) -> None:
        pass


def test_caribou_board_set_logic_level(monkeypatch: pytest.MonkeyPatch) -> None:
    transactions = []

    def mock_request(_: type, *args: str) -> bytes:
        nonlocal transactions
        transactions.append(" ".join([str(_) for _ in args]))
        return transactions[-1].encode("utf-8")

    monkeypatch.setattr(MockProtocol, "request", mock_request)
    CaribouBoard(0, socket.socket(), MockProtocol).set_logic_level(1.2)
    assert transactions[-2:] == [
        "device.setInputCMOSLevel 0 1.2",
        "device.setOutputCMOSLevel 0 1.2",
    ]
