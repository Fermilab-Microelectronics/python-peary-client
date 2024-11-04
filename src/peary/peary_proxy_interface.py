from __future__ import annotations

import abc
from typing import TYPE_CHECKING

from peary.peary_protocol import PearyProtocol

if TYPE_CHECKING:
    from socket import socket as socket_type

    from peary.peary_device import PearyDevice
    from peary.peary_protocol_interface import PearyProtocolInterface


# TODO(Jeff): Getter should throw and exception if something is not found


class PearyProxyInterface(abc.ABC):
    """Connect to a pearyd instance running somewhere else.

    The peary client supports the context manager protocol and should be
    used in a with statement for automatic connection closing on errors, i.e.

        with PearyClient(host='localhost') as client:
            # do something with the client

    """

    @abc.abstractmethod
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

    @abc.abstractmethod
    def keep_alive(self) -> bytes:
        """Send a keep-alive message to test the connection."""

    @abc.abstractmethod
    def add_device(self, name: str) -> PearyDevice:
        """Add a new device to the system.

        Args:
            name: Name of device to add.

        Returns:
            PearyDevice: instance of the added device.

        """

    @abc.abstractmethod
    def get_device(self, name: str) -> PearyDevice:
        """Get an existing device.

        Args:
            name: Name of device to get.

        Returns:
            PearyDevice: Instance of the device.

        """

    @abc.abstractmethod
    def clear_devices(self) -> bytes:
        """Clear and close all configured devices."""

    @abc.abstractmethod
    def list_devices(self) -> list[str]:
        """List all the added devices."""

    @abc.abstractmethod
    def list_devices(self) -> bytes:
        """List devices known to the remote server."""
