from __future__ import annotations

import abc


class PearyClientInterface(abc.ABC):  # pylint: disable=too-few-public-methods
    """Peary client interfac3."""

    @abc.abstractmethod
    def request(self, cmd: str, *args: str) -> bytes:
        """Send a command to the host and return the reply payload."""
