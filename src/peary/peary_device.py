from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from peary.peary_client_interface import PearyClientInterface


# TODO(Jeff): Clean up this file and reference it from the CERN repo
class PearyDevice:
    """A Peary device.

    This object acts as a proxy that forwards all function calls to the
    device specified by the device index using the client object.
    """

    def __init__(self, client: PearyClientInterface, index: int) -> None:
        """Initializes a remote peary device.

        Args:
            client: Peary client used to connect to the remote peary server.
            index: Numerical identifier for the device.

        """
        self._client = client
        self.index = index
        # internal name is actualy <name>Device, but we only use <name>
        # to generate it. remove the suffix for consistency
        self.device_type = self._run_command("name").decode("utf-8")

        # TODO(Jeff): This secret suffixes are annoying, comment out for now
        # sss if self.device_type.endswith("Device"):
        # sss    self.device_type = self.device_type[:-6]

    def __repr__(self) -> str:
        """Returns a string representation for the device.

        Returns:
            String: The string representation of the device instance.

        """
        return f"{self.device_type}_Device({self.index})"

    def _client_request(self, cmd: str, *args: str) -> bytes:
        """Send a per-device request to the host and returns response payload.

        Args:
            cmd: The device command to be performed by the host.
            args: Additional device command arguments sent to host.

        Returns:
            bytes: Client response.

        """
        return self._client.request(f"device.{cmd}", str(self.index), *args)

    def _run_command(self, cmd: str, *args: str) -> bytes:
        """Run a device command.

        Args:
            cmd: The device command to run.
            args: Additional command arguments.

        Returns:
            bytes: Command response.

        """
        return self._client_request(cmd, *args)

    def _run_setter(self, cmd: str, key: str, value: str) -> bytes:
        """Request a nullary operation from the device."""
        return self._client_request(cmd, key, value)

    def _run_getter(self, cmd: str, key: str) -> bytes:
        """Request a nullary operation from the device."""
        return self._client_request(cmd, key)

    # fixed device functionality is added explicitely with
    # additional return value decoding where appropriate

    def power_on(self) -> bytes:
        """Power on the device."""
        return self._run_command("power_on")

    def power_off(self) -> bytes:
        """Power off the device."""
        return self._run_command("power_off")

    def reset(self) -> bytes:
        """Reset the device."""
        return self._run_command("reset")

    def configure(self) -> bytes:
        """Initialize and configure the device."""
        return self._run_command("configure")

    def daq_start(self) -> bytes:
        """Start data aquisition for the device."""
        return self._run_command("daq_start")

    def daq_stop(self) -> bytes:
        """Stop data aquisition for the device."""
        return self._run_command("daq_stop")

    def list_registers(self) -> list[str]:
        """List all available registers by name."""
        return self._run_command("list_registers").decode("utf-8").split()

    def get_register(self, name: str) -> int:
        """Get the value of a named register."""
        return int(self._run_getter("get_register", name))

    def set_register(self, name: str, value: int) -> bytes:
        """Set the value of a named register."""
        return self._run_setter("set_register", name, str(value))

    def get_memory(self, name: str) -> int:
        """Get the value of a named memory."""
        return int(self._run_getter("get_memory", name))

    def set_memory(self, name: str, value: int) -> bytes:
        """Set the value of a named memory."""
        return self._run_setter("set_memory", name, str(value))

    def get_current(self, name: str) -> float:
        """Get the measured current of a named periphery port."""
        return float(self._run_getter("get_current", name))

    def set_current(self, name: str, value: float) -> bytes:
        """Set the current of a named periphery port."""
        return self._run_setter("set_current", name, str(value))

    def get_voltage(self, name: str) -> float:
        """Get the measured voltage of a named periphery port."""
        return float(self._run_getter("get_voltage", name))

    def set_voltage(self, name: str, value: float) -> bytes:
        """Set the voltage of a named periphery port."""
        return self._run_setter("set_voltage", name, str(value))

    def switch_on(self, name: str) -> bytes:
        """Switch on a periphery port."""
        return self._run_command("switch_on", name)

    def switch_off(self, name: str) -> bytes:
        """Switch off a periphery port."""
        return self._run_command("switch_off", name)

    # unknown attributes are interpreted as dynamic functions
    # and are forwarded as-is to the pearyd instance
    # sss def __getattr__(self, name: str) -> bytes:
    # sss    func = functools.partial(self._request, name)
    # sss    self.__dict__[name] = func
    # sss    return func
