from __future__ import annotations

from typing import TYPE_CHECKING

from peary.peary_protocol import PearyProtocol

if TYPE_CHECKING:
    from socket import socket as socket_type

    from peary.peary_protocol_interface import PearyProtocolInterface


class PearyDevice:
    """A Peary device."""

    def __init__(
        self,
        index: int,
        socket: socket_type,
        protocol_class: type[PearyProtocolInterface] = PearyProtocol,
    ) -> None:
        """Initializes a remote peary device.

        Args:
            socket: Socket connected to the remote peary server.
            protocol_class: Protocol used during communication with the peary server.
            index: Numerical identifier for the device.

        """
        self._index = index
        self._protocol = protocol_class(socket)
        self._name = self._request_name()

    def __repr__(self) -> str:
        """Returns a string representation for the device.

        Returns:
            String: The string representation of the device instance.

        """
        return f"{self.name}({self.index})"

    @property
    def index(self) -> int:
        """Returns the device index."""
        return self._index

    @property
    def name(self) -> str:
        """Returns the device type."""
        return self._name

    def _request(self, cmd: str, *args: str) -> bytes:
        """Send a per-device request to the host and returns response payload.

        Args:
            cmd: The device command to be performed by the host.
            args: Additional device command arguments sent to host.

        Returns:
            bytes: response payload.

        """
        return self._protocol.request(f"device.{cmd}", str(self.index), *args)

    def _request_name(self) -> str:
        """Requests the name of the device."""
        return self._request("name").decode("utf-8")

    # fixed device functionality is added explicitely with
    # additional return value decoding where appropriate

    def power_on(self) -> bytes:
        """Power on the device."""
        return self._request("power_on")

    def power_off(self) -> bytes:
        """Power off the device."""
        return self._request("power_off")

    def reset(self) -> bytes:
        """Reset the device."""
        return self._request("reset")

    def configure(self) -> bytes:
        """Initialize and configure the device."""
        return self._request("configure")

    def daq_start(self) -> bytes:
        """Start data aquisition for the device."""
        return self._request("daq_start")

    def daq_stop(self) -> bytes:
        """Stop data aquisition for the device."""
        return self._request("daq_stop")

    def list_registers(self) -> list[str]:
        """List all available registers by name."""
        return self._request("list_registers").decode("utf-8").split()

    def get_register(self, name: str) -> int:
        """Get the value of a named register."""
        return int(self._request("get_register", name))

    def set_register(self, name: str, value: int) -> bytes:
        """Set the value of a named register."""
        return self._request("set_register", name, str(value))

    def get_memory(self, name: str) -> int:
        """Get the value of a named memory."""
        return int(self._request("get_memory", name))

    def set_memory(self, name: str, value: int) -> bytes:
        """Set the value of a named memory."""
        return self._request("set_memory", name, str(value))

    def get_current(self, name: str) -> float:
        """Get the measured current of a named periphery port."""
        return float(self._request("get_current", name))

    def set_current(self, name: str, value: float) -> bytes:
        """Set the current of a named periphery port."""
        return self._request("set_current", name, str(value))

    def get_voltage(self, name: str) -> float:
        """Get the measured voltage of a named periphery port."""
        return float(self._request("get_voltage", name))

    def set_voltage(self, name: str, value: float) -> bytes:
        """Set the voltage of a named periphery port."""
        return self._request("set_voltage", name, str(value))

    def switch_on(self, name: str) -> bytes:
        """Switch on a periphery port."""
        return self._request("switch_on", name)

    def switch_off(self, name: str) -> bytes:
        """Switch off a periphery port."""
        return self._request("switch_off", name)
