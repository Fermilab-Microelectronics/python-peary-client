from __future__ import annotations

import socket as socket_module
from typing import TYPE_CHECKING

import pytest

from peary.peary_protocol import PearyProtocol
from peary.peary_proxy import PearyProxy

if TYPE_CHECKING:
    from collections.abc import Callable


@pytest.fixture(name="mock_proxy")
def _mock_proxy() -> Callable:
    def _customize_mock_proxy_request(
        *, req: str | None = None, resp: bytes | None = None
    ) -> PearyProxy:

        class MockPearyProtocol(PearyProtocol):
            """A Mock Peary Protocol."""

            def request(
                self, msg: str, *args: str, buffer_size: int = 4096  # noqa: ARG002
            ) -> bytes:
                if req:
                    assert " ".join([msg, *args]) == req
                if resp:
                    return resp
                else:
                    return " ".join([msg, *args]).encode("utf-8")

        return PearyProxy(
            MockPearyProtocol(
                socket_module.socket(), checks=PearyProtocol.Checks.CHECK_NONE
            )
        )

    return _customize_mock_proxy_request
