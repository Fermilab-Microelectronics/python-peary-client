from __future__ import annotations

from typing import TYPE_CHECKING

from peary.peary_device import PearyDevice
from peary.peary_protocol import PearyProtocol
from peary.peary_proxy_interface import PearyProxyInterface

if TYPE_CHECKING:
    from socket import socket as socket_type

    from peary.peary_protocol_interface import PearyProtocolInterface


class PearyProxy(PearyProxyInterface):
    """Proxy for the remote peary server."""

    def __init__(
        self,
        socket: socket_type,
        protocol_class: type[PearyProtocolInterface] = PearyProtocol,
    ) -> None:
        """Initializes a new peary proxy.

        Args:
            socket: Socket connected to the remote peary server.
            protocol_class: Protocol used during communication with the peary server.

        """
        self._devices: dict[int, PearyDevice] = {}
        self._socket: socket_type = socket
        self._protocol_class = protocol_class

        self._protocol = self._protocol_class(socket)

    def keep_alive(self) -> bytes:
        """Send a keep-alive message to test the connection."""
        return self._protocol.request("")

    def get_device(self, index: int) -> PearyDevice:
        """Get the device object corresponding to the given index."""
        device = self._devices.get(index)
        if not device:
            device = self._devices.setdefault(
                index, PearyDevice(index, self._socket, self._protocol_class)
            )
        return device

    def list_devices(self) -> list[PearyDevice]:
        """List configured devices."""
        response = self._protocol.request("list_devices")
        indices = [int(_) for _ in response.split()]
        return [self.get_device(_) for _ in indices]

    def clear_devices(self) -> bytes:
        """Clear and close all configured devices."""
        return self._protocol.request("clear_devices")

    def add_device(self, name: str, *args: str) -> PearyDevice:
        """Add a new device of the given type."""
        response = self._protocol.request("add_device", name, *args)
        return self.get_device(int(response))

    def ensure_device(self, name: str) -> PearyDevice:
        """Ensure at least one device of the given type exists and return it.

        If there are multiple devices with the same name, the first one
        is returned.
        """
        devices_filtered = [d for d in self.list_devices() if d.name == name]
        devices_sorted = sorted(devices_filtered, key=lambda _: _.index)
        if devices_sorted:
            return devices_sorted[0]
        else:
            return self.add_device(name)
