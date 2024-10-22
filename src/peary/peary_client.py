from __future__ import annotations

import socket
import struct
from typing import TYPE_CHECKING

import peary

if TYPE_CHECKING:
    from typing_extensions import Self

    from peary.peary_device import PearyDevice

# TODO(Jeff): Clean up this file and reference it from the CERN repo
PEARY_PROTOCOL_VERSION = b"1"
PEARY_REQUEST_HEADER = struct.Struct("!HH")
PEARY_REQUEST_LENGTH = struct.Struct("!L")
PEARY_STATUS_OK = 0


class UnsupportedProtocolError(Exception):
    """Exception for unsupported protocols."""


class InvalidReplyError(Exception):
    """Exception for receiving and invalid reply."""


class FailureError(Exception):
    """Exception for failing return code."""

    def __init__(self, cmd: str, code: int, reason: str) -> None:
        """Initializer for a failure exception.

        Args:
            cmd: Name of the failing command.
            code: Return value for the failing command.
            reason: Reason for the failure.
        """
        msg = f"Command '{cmd}' failed with code {code} '{reason}'"
        super().__init__(msg)


class PearyClient:
    """Connect to a pearyd instance running somewhere else.

    The peary client supports the context manager protocol and should be
    used in a with statement for automatic connection closing on errors, i.e.

        with PearyClient(host='localhost') as client:
            # do something with the client

    """

    def __init__(self, host: str, port: int = 12345) -> None:
        """Initializes a new peary client.

        Args:
            host: Hostname of the remote peary server.
            port: Port number used by the remote peary server. Defaults to 12345.

        Raises:
            InvalidReplyError: XXX
            UnsupportedProtocolError: XXX
            FailureError: XXX
        """
        self.host = host
        self.port = port
        # Cache of available device objects to avoid recreating them
        self._devices: dict[int, PearyDevice] = {}
        self._sequence_number = 0
        self._socket = socket.create_connection((self.host, self.port))
        # check connection and protocol
        version = self.request("protocol_version")
        if version != PEARY_PROTOCOL_VERSION:
            raise UnsupportedProtocolError(version)

    def __del__(self) -> None:
        """Deconstructs the peary client."""
        self._close()

    # support with statements
    def __enter__(self) -> Self:
        """Enters a context block.

        Returns:
            Registry: Return this peary client.
        """
        return self

    def __exit__(self, *_: object) -> bool:
        """Exits a context block.

        Args:
            _: Catches the usued arguments required for the __exit__ function.

        Returns:
            bool: Exceptions are not handled so always returns true.
        """
        self._close()
        return True

    def _close(self) -> None:
        """Close the connection."""
        # is there a better way to allow double-close?
        if self._socket.fileno() != -1:
            # hard shutdown, no more sending or receiving
            self._socket.shutdown(socket.SHUT_RDWR)
            self._socket.close()

    @property
    def peername(self) -> str:
        """Returns the connectinos peer name."""
        return self._socket.getpeername()

    def request(self, cmd: str, *args: str) -> bytes:
        """Send a command to the host and return the reply payload."""
        # 1. encode request
        # encode command and its arguments into message payload
        req_payload = " ".join([cmd] + [str(_) for _ in args]).encode("utf-8")
        # encode message header
        self._sequence_number += 1
        req_header = PEARY_REQUEST_HEADER.pack(self._sequence_number, PEARY_STATUS_OK)
        # encode message length for framing
        req_length = PEARY_REQUEST_LENGTH.pack(len(req_header) + len(req_payload))
        # 2. send request
        self._socket.send(req_length)
        self._socket.send(req_header)
        self._socket.send(req_payload)
        # 3. wait for reply and unpack in opposite order
        (rep_length,) = PEARY_REQUEST_LENGTH.unpack(self._socket.recv(4))
        if rep_length < 4:  # noqa: PLR2004
            msg = "Length too small"
            raise InvalidReplyError(msg)
        rep_msg = self._socket.recv(rep_length)
        rep_seq, rep_status = PEARY_REQUEST_HEADER.unpack(rep_msg[:4])
        rep_payload = rep_msg[4:]
        if rep_status != PEARY_STATUS_OK:
            raise FailureError(cmd, rep_status, rep_payload.decode("utf-8"))
        if rep_seq != self._sequence_number:
            msg = "Sequence number missmatch"
            raise InvalidReplyError(msg, self._sequence_number, rep_seq)
        return rep_payload

    def keep_alive(self) -> bytes:
        """Send a keep-alive message to test the connection."""
        return self.request("")

    def list_devices(self) -> list[PearyDevice]:
        """List configured devices."""
        response = self.request("list_devices")
        indices = [int(_) for _ in response.split()]
        return [self.get_device(_) for _ in indices]

    def clear_devices(self) -> bytes:
        """Clear and close all configured devices."""
        return self.request("clear_devices")

    def get_device(self, index: int) -> PearyDevice:
        """Get the device object corresponding to the given index."""
        device = self._devices.get(index)
        if not device:
            device = self._devices.setdefault(
                index, peary.peary_device.PearyDevice(self, index)
            )
        return device

    def add_device(
        self, device_type: str, config_path: str | None = None
    ) -> PearyDevice:
        """Add a new device of the given type."""
        if config_path:
            # removed these: print("device w/ cfg")
            response = self.request("add_device", device_type, config_path)
        else:
            # removed these: print("device w/o cfg")
            response = self.request("add_device", device_type)
        return self.get_device(int(response))

    def ensure_device(self, device_type: str) -> PearyDevice:
        """Ensure at least one device of the given type exists and return it.

        If there are multiple devices with the same name, the first one
        is returned.
        """
        devices_all: list[PearyDevice] = self.list_devices()
        devices_filtered = filter(lambda _: _.device_type == device_type, devices_all)
        devices_sorted = sorted(devices_filtered, key=lambda _: _.index)
        if devices_sorted:
            return devices_sorted[0]
        else:
            return self.add_device(device_type)
