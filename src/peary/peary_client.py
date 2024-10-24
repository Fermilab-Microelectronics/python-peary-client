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
    ) -> None:
        """Initializes a new peary client.

        Args:
            host: Hostname of the remote peary server.
            port: Port number used by the remote peary server. Defaults to 12345.
            proxy_class: Class used to construct the proxy. Defaults to PearyProxy.
        """
        self.host = host
        self.port = port
        self.proxy_class = proxy_class
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def __enter__(self) -> PearyProxyInterface:
        """Enters a connection with a peary server.

        Returns:
            Self: Returns peary client with new socket.

        """
        # TODO(Jeff): verify the connection is open
        self.socket.connect((self.host, self.port))
        return self.proxy_class(self.socket)

    def __exit__(self, *_: object) -> None:
        """Exits a context block.

        Args:
            _: Catches the usued arguments required for the __exit__ function.

        """
        self.socket.shutdown(socket.SHUT_RDWR)
        self.socket.close()
