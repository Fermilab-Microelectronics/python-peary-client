from __future__ import annotations

import socket
from typing import TYPE_CHECKING

from peary.peary_proxy import PearyProxy

if TYPE_CHECKING:
    from peary.peary_proxy_interface import PearyProxyInterface


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
        proxy_class: type[PearyProxyInterface] = PearyProxy,
        socket_class: type[socket.socket] = socket.socket,
    ) -> None:
        """Initializes a new peary client.

        Args:
            host: Hostname of the remote peary server.
            port: Port number of the remote peary server. Defaults to 12345.
            proxy_class: Class used for the proxy. Defaults to PearyProxy.
            socket_class: Class used for the socket connection. Defaults to socket.

        """
        self._host = host
        self._port = port
        self._proxy_class = proxy_class
        self._socket = socket_class(socket.AF_INET, socket.SOCK_STREAM)

    @property
    def proxy_class(self) -> type[PearyProxyInterface]:
        """Returns the class used to contructuct the proxy."""
        return self._proxy_class

    @property
    def socket(self) -> socket.socket:
        """Returns the socket."""
        return self._socket

    def __enter__(self) -> PearyProxyInterface:
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

        return self.proxy_class(self.socket)

    def __exit__(self, *_: object) -> None:
        """Exits a context block.

        Args:
            _: Catches the usued arguments required for the __exit__ function.

        """
        self.socket.shutdown(socket.SHUT_RDWR)
        self.socket.close()
