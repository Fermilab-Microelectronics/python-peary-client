from __future__ import annotations

import abc
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from socket import socket as socket_type


# pylint: disable=too-few-public-methods
class PearyProtocolInterface(abc.ABC):
    """Interface class for the peary communication protocol."""

    @abc.abstractmethod
    def __init__(self, socket: socket_type, timeout: int = 10) -> None:
        """Initializes a new peary proxy.

        Args:
            socket: Socket connected to the remote peary server.
            timeout: Socket timeout value in seconds. Defaults to 10.

        """

    @abc.abstractmethod
    def request(self, msg: str, *args: str, buffer_size: int = 4096) -> bytes:
        """Initiates a requst to the connected peary server.

        Args:
            msg: The request message to be sent.
            *args: Additiona message argumnets.
            buffer_size: Size of the reciever buffer.

        Returns:
            bytes: The received response.

        """
