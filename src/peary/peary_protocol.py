from __future__ import annotations

import select
import struct
from enum import Flag, auto
from typing import TYPE_CHECKING, NamedTuple

if TYPE_CHECKING:
    from socket import socket as socket_type


class DecodedBytes(NamedTuple):
    """Return type for decoded bytes."""

    payload: bytes
    tag: int
    status: int


class PearyProtocol:
    """Protocol for encoding and decoding communication with a remote peary server."""

    class DecodeError(Exception):
        """Exception for failing decode."""

    class ResponseReceiveError(Exception):
        """Exception for failing to receive responses."""

    class ResponseSequenceError(Exception):
        """Exception for response out of order."""

    class ResponseStatusError(Exception):
        """Exception for response with failing status."""

    class RequestSendError(Exception):
        """Exception for requests failing to send."""

    class VersionError(Exception):
        """Exception for incompatible client and server protocols."""

    class Checks(Flag):
        """Collection of protocol checks that can be performed."""

        CHECK_NONE = auto()
        CHECK_VERSION = auto()

    STATUS_OK = 0
    STRUCT_HEADER = struct.Struct("!HH")
    STRUCT_LENGTH = struct.Struct("!L")
    VERSION = b"1"

    def __init__(
        self,
        socket: socket_type,
        *,
        timeout: int = 1,
        checks: Checks = Checks.CHECK_VERSION,
    ) -> None:
        """Initializes a new peary proxy.

        Args:
            socket: Socket connected to the remote peary server.
            timeout: Socket timeout value in seconds. Defaults to 1.
            checks: Checks performed during initialization. Defaults to CHECK_VERSION.

        Raises:
            VersionError: If protocol version doesn match with remote host.

        """
        self._tag: int = 0
        self._socket = socket

        self._socket.settimeout(timeout)
        if PearyProtocol.Checks.CHECK_VERSION in checks:
            self._verify_compatible_version()

    @staticmethod
    def encode(payload: bytes, tag: int, status: int) -> bytes:
        """Encodes a request into a sequence of bytes.

        Args:
            payload: The data payload encoded into the sequence.
            tag: Identifier encoded into the sequence.
            status: Status encoded into the sequence.

        Returns:
            bytes: The encoded sequence of bytes.

        """
        header = PearyProtocol.STRUCT_HEADER.pack(tag, status)
        length = PearyProtocol.STRUCT_LENGTH.pack(len(header) + len(payload))
        return b"".join([length, header, payload])

    @staticmethod
    def decode(data: bytes) -> DecodedBytes:
        """Decodes data into a sequence of bytes.

        Args:
            data: The encoded bytes

        Returns:
            A tuple containing the response message, response id, and response status.

        """
        if len(data) < PearyProtocol.STRUCT_LENGTH.size:
            raise PearyProtocol.DecodeError(
                f"Insufficent number of bytes: {len(data)}."
            )
        (length,) = PearyProtocol.STRUCT_LENGTH.unpack(
            data[: PearyProtocol.STRUCT_LENGTH.size]
        )

        if len(data) != (PearyProtocol.STRUCT_LENGTH.size + length):
            raise PearyProtocol.DecodeError("Incorrect number of bytes")
        tag, status = PearyProtocol.STRUCT_HEADER.unpack(
            data[
                PearyProtocol.STRUCT_LENGTH.size : PearyProtocol.STRUCT_LENGTH.size
                + PearyProtocol.STRUCT_HEADER.size
            ]
        )
        payload = data[PearyProtocol.STRUCT_HEADER.size - length :]
        return DecodedBytes(payload, tag, status)

    def request(self, msg: str, *args: str, buffer_size: int = 4096) -> bytes:
        """Initiates a requst to the connected peary server.

        Args:
            msg: The request message to be sent.
            *args: Additiona message argumnets.
            buffer_size: Size of the reciever buffer.

        Returns:
            bytes: The received response.

        Raises:
            ResponseStatusError: If response returns a failing status.
            ResponseSequenceError: If response id different than request id.

        """
        self._tag += 1
        self._send(
            PearyProtocol.encode(
                " ".join([msg, *args]).encode("utf-8"), self._tag, self.STATUS_OK
            )
        )
        resp, resp_id, resp_status = PearyProtocol.decode(self._recv(buffer_size))

        if resp_status != PearyProtocol.STATUS_OK:
            raise PearyProtocol.ResponseStatusError(
                f"Failed response status {resp_status} from request '{msg!r}'"
            )
        if resp_id != self._tag:
            raise PearyProtocol.ResponseSequenceError(
                f"Recieved out of order repsonse from '{msg}': {resp_id} != {self._tag}"
            )

        return resp

    def _send(self, data: bytes) -> int:
        """Sends data through the connected socket.

        Args:
            data: Bytes to be sent.

        Returns:
            int: The number of sent bytes.

        Raises:
            RequestSendError: If the data failed to send

        """
        if (size := self._socket.send(data)) != len(data):
            raise PearyProtocol.RequestSendError(f"Failed to send request: {data!r}")
        return size

    def _recv(self, buffer_size: int) -> bytes:
        """Receive data from the connected socket.

        Args:
            buffer_size: Number of bytes to receive.

        Returns:
            bytes: The received data.

        Raises:
            ResponseReceiveError: If failed to receive response.

        """
        data = bytearray()
        while True:  # pylint: disable=while-used
            block: bytes = self._socket.recv(buffer_size)
            data.extend(block)
            if len(block) < buffer_size:
                break
            readable, _, _ = select.select([self._socket], [], [], 0)
            if self._socket not in readable:
                break
        if not data:
            raise PearyProtocol.ResponseReceiveError("Failed to receive response.")
        return bytes(data)

    def _verify_compatible_version(self) -> None:
        """Verify the remote version is suppoted by this protocol.

        Raises:
            VersionError: If versions are incompatible.

        """
        if (version := self.request("protocol_version")) != self.VERSION:
            raise PearyProtocol.VersionError(
                f"Unsupported protocol version: {version!r}"
            )
