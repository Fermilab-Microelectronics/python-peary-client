import struct

import pytest


# TODO(Jeff): This is more than just a mock socket. This is a mock server.
@pytest.fixture
def mock_socket():
    # pylint: disable=missing-type-doc
    class _MockSocket:
        """Mock socket class."""

        NUM_BITS_PACKET_ID = 2
        NUM_BITS_PACKET_LENGTH = 4
        NUM_BITS_PACKET_STATUS = 2
        PROTOCOL_VERSION = b"1"
        RESPONSE_STATUS_OK = 0
        STRUCT_PACKET_HEADER = struct.Struct("!HH")
        STRUCT_PACKET_LENGTH = struct.Struct("!L")

        is_connected = None
        is_shutdown = None
        how_shutdown = None
        timeout = None

        # pylint: disable-next=super-init-not-called,unused-argument
        def __init__(self, addr_family, socket_type, *args, **kwargs):  # noqa: ARG002
            self.addr_family = addr_family
            self.socket_type = socket_type
            self.address = None

        def connect(self, address):
            """Mock connect method."""
            _MockSocket.is_connected = True
            _MockSocket.is_shutdown = False
            self.address = address

        # pylint: disable-next=unused-argument
        def recv(self, size) -> bytes:
            """Mock recv method."""
            return b" " * size

        def send(self, data) -> int:
            """Mock send method."""
            return len(data)

        def shutdown(self, how):
            """Mock connect method."""
            _MockSocket.is_shutdown = True
            _MockSocket.how_shutdown = how

        def settimeout(self, value):
            """Mock timeout method."""
            _MockSocket.timeout = value

        def close(self):
            """Mock connect method."""
            _MockSocket.is_connected = False

    return _MockSocket
