from peary.peary_proxy_interface import PearyProxyInterface


# pylint: disable=W9015,W9016
class MockProxy(PearyProxyInterface):
    """Mock proxy class."""

    def __init__(self, socket):
        """Mock intializer"""
        self.socket = socket

    def request(self, cmd, *args):
        """Mock Request"""

    def keep_alive(self):
        """Mock keep alive."""

    def list_devices(self):
        """Mock list devices."""

    def clear_devices(self):
        """Mock clear devices."""

    def get_device(self, index: int):
        """Mock get device."""

    def add_device(self, name, *args):
        """Add a new device of the given type."""

    def ensure_device(self, name):
        """Ensure at least one device of the given type exists and return it.

        If there are multiple devices with the same name, the first one
        is returned.
        """
