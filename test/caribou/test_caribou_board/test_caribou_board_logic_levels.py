from __future__ import annotations

from typing import TYPE_CHECKING

from caribou.caribou_board import CaribouBoard
from peary.peary_protocol_interface import PearyProtocolInterface

if TYPE_CHECKING:
    from socket import socket as socket_type


# pylint: disable=missing-param-doc
class MockProtocol(PearyProtocolInterface):
    def __init__(self, socket: socket_type, timeout: int = 10):
        """Mock __init__"""

    def request(self, msg: str, *args: str, buffer_size: int = 4096):
        """Mock request"""


def test_caribou_board_set_logic_level(monkeypatch):
    transactions = []

    def mock_request(_, *args):
        nonlocal transactions
        transactions.append(" ".join([str(_) for _ in args]))
        return transactions[-1].encode("utf-8")

    monkeypatch.setattr(MockProtocol, "request", mock_request)
    CaribouBoard(0, None, MockProtocol).set_logic_level(1.2)
    assert transactions[-2:] == [
        "device.setInputCMOSLevel 0 1.2",
        "device.setOutputCMOSLevel 0 1.2",
    ]
