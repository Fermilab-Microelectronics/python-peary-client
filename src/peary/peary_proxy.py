from __future__ import annotations

from typing import TYPE_CHECKING

from peary.peary_device import PearyDevice

if TYPE_CHECKING:
    from peary.peary_protocol import PearyProtocol


class PearyProxy:
    """Proxy for the remote peary server."""

    class PearyProxyAddDeviceError(Exception):
        """Exception for device related errors."""

    class PearyProxyGetDeviceError(Exception):
        """Exception for device related errors."""

    def __init__(self, protocol: PearyProtocol) -> None:
        """Initializes a new peary proxy.

        Args:
            protocol: Protocol connected to the remote peary server.

        """
        self._devices: dict[str, PearyDevice] = {}
        self._protocol = protocol

    def keep_alive(self) -> bytes:
        """Send a keep-alive message to test the connection."""
        return self._protocol.request("")

    def add_device(
        self, name: str, device_class: type[PearyDevice] = PearyDevice
    ) -> PearyDevice:
        """Add a new device.

        Args:
            name: Name of device to add.
            device_class: Class used to construct the device. Defaults to PearyDevice.

        Returns:
            PearyDevice: Instance of the added device.

        Raises:
            PearyProxyAddDeviceError: If device already exists

        """
        if name in self._devices:
            raise PearyProxy.PearyProxyAddDeviceError(f"Device already exists: {name}")
        index = int(self._protocol.request("add_device", name))
        self._devices[name] = device_class(index, self._protocol)
        return self._devices[name]

    def get_device(self, name: str) -> PearyDevice:
        """Get an existing device.

        Args:
            name: Name of device to get.

        Returns:
            PearyDevice: Instance of the device.

        Raises:
            PearyProxyGetDeviceError: If name is unknown.

        """
        try:
            return self._devices[name]
        except KeyError as e:
            raise PearyProxy.PearyProxyGetDeviceError(f"Unknown device: {name}") from e

    def clear_devices(self) -> None:
        """Clear and close all configured devices."""
        _ = self._protocol.request("clear_devices")
        self._devices.clear()

    def list_devices(self) -> list[str]:
        """List all the added devices."""
        return [*self._devices]

    def list_remote_devices(self) -> bytes:
        """List devices known to the remote server."""
        return self._protocol.request("list_devices")
