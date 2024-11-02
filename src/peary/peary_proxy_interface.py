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
    def list_devices(self) -> list[PearyDevice]:
        """List configured devices."""

    @abc.abstractmethod
    def clear_devices(self) -> bytes:
        """Clear and close all configured devices."""

    @abc.abstractmethod
    def get_device(self, index: int) -> PearyDevice:
        """Get the device object corresponding to the given index."""

    @abc.abstractmethod
    def add_device(self, name: str, *args: str) -> PearyDevice:
        """Add a new device of the given type."""

    @abc.abstractmethod
    def ensure_device(self, name: str) -> PearyDevice:
        """Ensure at least one device of the given type exists and return it.

        If there are multiple devices with the same name, the first one
        is returned.
        """
