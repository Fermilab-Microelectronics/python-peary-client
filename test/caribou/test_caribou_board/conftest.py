from __future__ import annotations

import socket
from typing import TYPE_CHECKING

import pytest

from caribou.caribou_board import CaribouBoard
from peary.peary_protocol import PearyProtocol

if TYPE_CHECKING:
    from collections.abc import Callable


TRANSACTIONS: list[str] = []


class MockCaribouBoard(CaribouBoard):
    """A Mock Caribou Board."""

    def __init__(self, index: int, protocol: PearyProtocol) -> None:
        super().__init__(index, protocol)
        # pylint: disable-next=redefined-outer-name,invalid-name,unused-variable
        TRANSACTIONS: list[str] = []  # noqa: F841, N806

    @property
    def transactions(self) -> list[str]:
        return TRANSACTIONS


@pytest.fixture(name="mock_caribou_board")
def _mock_caribou_board() -> Callable:
    def _customize_mock_caribou_board_request(index: int = 0) -> MockCaribouBoard:

        class MockProtocol(PearyProtocol):
            """A Mock Peary Protocol."""

            def request(
                self, msg: str, *args: str, buffer_size: int = 4096  # noqa: ARG002
            ) -> bytes:
                TRANSACTIONS.append(" ".join([str(_) for _ in (msg, *args)]))
                return " ".join([msg, *args]).encode("utf-8")

        return MockCaribouBoard(
            index, MockProtocol(socket.socket(), checks=PearyProtocol.Checks.CHECK_NONE)
        )

    return _customize_mock_caribou_board_request
