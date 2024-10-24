from peary.peary_proxy_interface import PearyProxyInterface


class MockProxy(PearyProxyInterface):  # pylint: disable=W9016
    """Mock proxy class."""

    def __init__(self, socket):  # pylint: disable=W9016
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

    def add_device(self, device_type, *args):
        """Add a new device of the given type."""

    def ensure_device(self, device_type):
        """Ensure at least one device of the given type exists and return it.

        If there are multiple devices with the same name, the first one
        is returned.
        """
