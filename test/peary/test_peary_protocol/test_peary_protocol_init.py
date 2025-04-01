from __future__ import annotations

from typing import TYPE_CHECKING

from peary.peary_protocol import PearyProtocol

if TYPE_CHECKING:
    from collections.abc import Callable


def test_peary_protocol_init_timeout_default(socket_class_context: Callable) -> None:
    with socket_class_context() as socket_class:
        socket_class.timeout = None
        PearyProtocol(socket_class(), checks=PearyProtocol.Checks.CHECK_NONE)
        assert socket_class.timeout == 1


def test_peary_protocol_init_timeout_nondefault(socket_class_context: Callable) -> None:
    with socket_class_context() as socket_class:
        socket_class.timeout = None
        PearyProtocol(
            socket_class(), timeout=100, checks=PearyProtocol.Checks.CHECK_NONE
        )
        assert socket_class.timeout == 100
