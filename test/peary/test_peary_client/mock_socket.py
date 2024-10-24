from socket import socket as socket_class


# pylint: disable=missing-type-doc
class MockSocket(socket_class):
    """Mock socket class."""

    is_connected = None
    is_shutdown = None
    how_shutdown = None

    def __init__(self, addr_family, socket_type, proto=0, fileno=None):
        """Mock initializer."""
        super().__init__(addr_family, socket_type, proto, fileno)
        self.addr_family = addr_family
        self.socket_type = socket_type
        self.address = None

    def connect(self, address):
        """Mock connect method."""
        MockSocket.is_connected = True
        MockSocket.is_shutdown = False
        self.address = address

    def recv(self, bufsize):
        """Mock recv method."""

    def send(self, data):
        """Mock send method."""

    def shutdown(self, how):
        """Mock connect method."""
        MockSocket.is_shutdown = True
        MockSocket.how_shutdown = how

    def close(self):
        """Mock connect method."""
        MockSocket.is_connected = False
