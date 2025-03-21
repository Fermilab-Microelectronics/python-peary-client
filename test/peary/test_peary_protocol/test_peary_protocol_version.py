from __future__ import annotations

from typing import TYPE_CHECKING

import pytest

from peary.peary_protocol import PearyProtocol

if TYPE_CHECKING:
    from collections.abc import Callable


def test_peary_protocol_version_request_message(mock_socket: Callable) -> None:

    class MockProtocol(PearyProtocol):

        def request(
            self, msg: str, *args: str, buffer_size: int = 4096  # noqa: ARG002
        ) -> bytes:
            assert msg == "protocol_version"
            return b"1"

    with mock_socket() as socket_class:
        MockProtocol(socket_class())


def test_peary_protocol_version_supported(mock_socket: Callable) -> None:

    class MockProtocol(PearyProtocol):

        def request(
            self, msg: str, *args: str, buffer_size: int = 4096  # noqa: ARG002
        ) -> bytes:
            return b"1"

    with mock_socket() as socket_class:
        MockProtocol(socket_class())


def test_peary_protocol_version_unsupported(mock_socket: Callable) -> None:

    class MockProtocol(PearyProtocol):

        def request(
            self, msg: str, *args: str, buffer_size: int = 4096  # noqa: ARG002
        ) -> bytes:
            return b"0"

    with mock_socket() as socket_class:
        with pytest.raises(
            PearyProtocol.VersionError, match="Unsupported protocol version: b'0'"
        ):
            MockProtocol(socket_class())
