from socket import socket as socket_class

import pytest


# TODO(Jeff): This is more than just a mock socket. This is a mock server.
@pytest.fixture
def mock_socket():
    # pylint: disable=missing-type-doc
    class _MockSocket:
        """Mock socket class."""

        is_connected = None
        is_shutdown = None
        how_shutdown = None

        # pylint: disable-next=super-init-not-called,unused-argument
        def __init__(self, addr_family, socket_type, *args, **kwargs):  # noqa: ARG002
            self.addr_family = addr_family
            self.socket_type = socket_type
            self.address = None

            self._buffer_request = bytearray()
            self._buffer_response = bytearray()

        def connect(self, address):
            """Mock connect method."""
            _MockSocket.is_connected = True
            _MockSocket.is_shutdown = False
            self.address = address

        def recv(self, bufsize):
            """Mock recv method."""
            assert self._buffer_request == ["a"]

        def send(self, data):
            """Mock send method."""
            self._buffer_request.append(data)

        def shutdown(self, how):
            """Mock connect method."""
            _MockSocket.is_shutdown = True
            _MockSocket.how_shutdown = how

        def close(self):
            """Mock connect method."""
            _MockSocket.is_connected = False

    return _MockSocket
