from __future__ import annotations

import socket as socket_module

from peary.peary_protocol import PearyProtocol
from peary.peary_proxy import PearyProxy


class PearyClient:
    """Connect to a remote peary server instance.

    The peary client supports the context manager protocol and should be
    used in a with statement for automatic connection closing on errors, i.e.

        with PearyClient(host='localhost') as client:
            # do something with the client

    """

    class PearySockerError(Exception):
        """Exception for socket errors."""

    def __init__(
        self,
        host: str,
        port: int = 12345,
        *,
        protocol_class: type[PearyProtocol] = PearyProtocol,
        socket_class: type[socket_module.socket] = socket_module.socket,
    ) -> None:
        """Initializes a new peary client.

        Args:
            host: Hostname of the remote peary server.
            port: Port number of the remote peary server. Defaults to 12345.
            socket_class: Class used for the remote socket. Defaults to socket.
            protocol_class: Class used for the protocol. Defaults to PearyProtocol.

        """
        self._host = host
        self._port = port
        self._protocol_class = protocol_class
        self._socket = socket_class(socket_module.AF_INET, socket_module.SOCK_STREAM)

    @property
    def socket(self) -> socket_module.socket:
        """Returns the socket."""
        return self._socket

    def __enter__(self) -> PearyProxy:
        """Enters a connection with a peary server.

        Returns:
            Self: Returns peary client with new socket.

        Raises:
            PearySockerError: If client cannot not connect to remote host.

        """
        try:
            self.socket.connect((self._host, self._port))
        except Exception as e:
            raise PearyClient.PearySockerError(
                f"Unable to connect to host {self._host} using port {self._port}."
            ) from e

        return PearyProxy(self._protocol_class(self.socket))

    def __exit__(self, *_: object) -> None:
        """Exits a context block.

        Args:
            _: Catches the usued arguments required for the __exit__ function.

        """
        self.socket.shutdown(socket_module.SHUT_RDWR)
        self.socket.close()
