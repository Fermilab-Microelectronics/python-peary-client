from __future__ import annotations

import struct
from typing import TYPE_CHECKING

from peary.peary_device import PearyDevice
from peary.peary_proxy_interface import PearyProxyInterface

if TYPE_CHECKING:
    from socket import socket as socket_type

# TODO(Jeff): Getter should throw and exception if something is not found


class PearyProxy(PearyProxyInterface):
    """Connect to a pearyd instance running somewhere else.

    The peary client supports the context manager protocol and should be
    used in a with statement for automatic connection closing on errors, i.e.

        with PearyClient(host='localhost') as client:
            # do something with the client

    """

    PROTOCOL_VERSION = b"1"
    STRUCT_REQUEST_HEADER = struct.Struct("!HH")
    STRUCT_REQUEST_LENGTH = struct.Struct("!L")
    RESPONSE_LENGTH = 4
    RESPONS_STATUS_OK = 0

    class PearyCommandError(Exception):
        """Exception for failing command."""

    class PearyProtocolError(Exception):
        """Exception for unsupported protocols."""

    class PearyResponseError(Exception):
        """Exception for reposnse errors."""

    def __init__(self, socket: socket_type) -> None:
        """Initializes a new peary client.

        Args:
            socket: Socket connected to the remote peary server.

        Raises:
            PearyProtocolError: If server and client protocols don't match.

        """
        self.devices: dict[int, PearyDevice] = {}
        self.sequence_number = 0
        self.socket: socket_type = socket

        version = self.request("protocol_version")
        if version != PearyProxy.PROTOCOL_VERSION:
            raise PearyProxy.PearyProtocolError(
                f"Unsupported protocol version: {version!r}"
            )

    # TODO(Jeff): This should be a private call
    def request(self, cmd: str, *args: str) -> bytes:
        """Send a command to the host and return the reply payload.

        Raises:
            PearyCommandError: If a command returns with a failing status code.
            PearyProtocolError: If communication protocols isn't supported.
            PearyResponseError: If response packet is recieved correctly.
            PearySockerError: If socket is not connected.
        """
        # 1. encode request
        # encode command and its arguments into message payload
        req_payload = " ".join([cmd] + [str(_) for _ in args]).encode("utf-8")
        # encode message header
        self.sequence_number += 1
        req_header = PearyProxy.STRUCT_REQUEST_HEADER.pack(
            self.sequence_number, PearyProxy.RESPONS_STATUS_OK
        )
        # encode message length for framing
        req_length = PearyProxy.STRUCT_REQUEST_LENGTH.pack(
            len(req_header) + len(req_payload)
        )

        # 2. send request
        self.socket.send(req_length)
        self.socket.send(req_header)
        self.socket.send(req_payload)

        # 3. wait for reply and unpack in opposite order
        (rep_length,) = PearyProxy.STRUCT_REQUEST_LENGTH.unpack(
            self.socket.recv(PearyProxy.RESPONSE_LENGTH)
        )
        if rep_length < PearyProxy.RESPONSE_LENGTH:
            raise PearyProxy.PearyResponseError(f"Reponse too small: {rep_length}")
        rep_msg = self.socket.recv(rep_length)
        rep_seq, rep_status = PearyProxy.STRUCT_REQUEST_HEADER.unpack(
            rep_msg[: PearyProxy.RESPONSE_LENGTH]
        )
        rep_payload = rep_msg[PearyProxy.RESPONSE_LENGTH :]

        if rep_status != PearyProxy.RESPONS_STATUS_OK:
            raise PearyProxy.PearyCommandError(
                f"Command '{cmd}' failed with status {rep_status}"
            )
        if rep_seq != self.sequence_number:
            msg = "Sequence number missmatch"
            raise PearyProxy.PearyResponseError(msg, self.sequence_number, rep_seq)
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
        device = self.devices.get(index)
        if not device:
            device = self.devices.setdefault(index, PearyDevice(self, index))
        return device

    def add_device(self, device_type: str, *args: str) -> PearyDevice:
        """Add a new device of the given type."""
        response = self.request("add_device", device_type, *args)
        return self.get_device(int(response))

    def ensure_device(self, device_type: str) -> PearyDevice:
        """Ensure at least one device of the given type exists and return it.

        If there are multiple devices with the same name, the first one
        is returned.
        """
        devices_filtered = [
            d for d in self.list_devices() if d.device_type == device_type
        ]
        devices_sorted = sorted(devices_filtered, key=lambda _: _.index)
        if devices_sorted:
            return devices_sorted[0]
        else:
            return self.add_device(device_type)
