from __future__ import annotations

from typing import TYPE_CHECKING

import pytest

from peary.peary_protocol import PearyProtocol

if TYPE_CHECKING:
    from collections.abc import Callable


def test_peary_protocol_send_okay(mock_socket: Callable) -> None:
    # pylint: disable-next=unnecessary-lambda
    fake_socket = mock_socket(mock_send=lambda _: len(_))
    PearyProtocol(fake_socket(), checks=PearyProtocol.Checks.CHECK_NONE).request("")


def test_peary_protocol_send_error(mock_socket: Callable) -> None:
    fake_socket = mock_socket(mock_send=lambda _: len(_) - 1)
    with pytest.raises(
        PearyProtocol.RequestSendError, match="Failed to send request:*"
    ):
        PearyProtocol(fake_socket(), checks=PearyProtocol.Checks.CHECK_NONE).request("")
