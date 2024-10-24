from socket import socket as socket_class


# pylint: disable=missing-type-doc
class MockSocket(socket_class):
    """Mock socket class."""

    def __init__(self, addr_family, socket_type, proto=0, fileno=None):
        """Mock initializer."""
        super().__init__(addr_family, socket_type, proto, fileno)
        self.addr_family = addr_family
        self.socket_type = socket_type
        self.address = None
        self.is_connected = None
        self.is_shutdown = None
        self.how_shutdown = None

    def connect(self, address):
        """Mock connect method."""
        self.address = address
        self.is_connected = True
        self.is_shutdown = False

    def recv(self, bufsize):
        """Mock recv method."""

    def send(self, data):
        """Mock send method."""

    def shutdown(self, how):
        """Mock connect method."""
        self.is_shutdown = True
        self.how_shutdown = how

    def close(self):
        """Mock connect method."""
        self.is_connected = False
