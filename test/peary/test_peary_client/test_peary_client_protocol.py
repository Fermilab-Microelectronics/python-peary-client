from __future__ import annotations

from typing import TYPE_CHECKING

from peary.peary_client import PearyClient
from peary.peary_protocol import PearyProtocol

if TYPE_CHECKING:
    import socket as socket_module


def test_peary_client_protocol_class(
    mock_socket_class: type[socket_module.socket],
) -> None:
    request_collection = []

    class MockProtocol(PearyProtocol):
        """A Mock Protocol."""

        def request(
            self, msg: str, *args: str, buffer_size: int = 4096  # noqa: ARG002
        ) -> bytes:
            request_collection.append(" ".join([msg, *args]))
            return b"1"

    with PearyClient(
        "", protocol_class=MockProtocol, socket_class=mock_socket_class
    ) as client:
        client.keep_alive()
    assert request_collection == ["protocol_version", ""]
