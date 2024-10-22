import peary


class PearyDevice:
    """A Peary device.

    This object acts as a proxy that forwards all function calls to the
    device specified by the device index using the client object.
    """

    def __init__(self, client: peary.peary_client.PearyClient, index: int) -> None:
        """Initializes a remote peary device.

        Args:
            client: Peary client used to connect to the remote peary server.
            index: Numerical identifier for the device.

        """
        self._client = client
        self.index = index
        # internal name is actualy <name>Device, but we only use <name>
        # to generate it. remove the suffix for consistency
        self.device_type = self._request("name").decode("utf-8")
        if self.device_type.endswith("Device"):
            self.device_type = self.device_type[:-6]

    def __repr__(self) -> str:
        """Returns a string representation for the device.

        Returns:
            String: The string representation of the device instance.

        """
        return f"{self.device_type}Device(index={self.index})"

    def _request(self, cmd: str, *args: str) -> bytes:
        """Send a per-device command to the host and return the reply payload."""
        return self._client.request(f"device.{cmd}", self.index, *args)

    # fixed device functionality is added explicitely with
    # additional return value decoding where appropriate

    def power_on(self) -> bytes:
        """Power on the device."""
        self._request("power_on")

    def power_off(self) -> bytes:
        """Power off the device."""
        self._request("power_off")

    def reset(self) -> bytes:
        """Reset the device."""
        self._request("reset")

    def configure(self) -> bytes:
        """Initialize and configure the device."""
        self._request("configure")

    def daq_start(self) -> bytes:
        """Start data aquisition for the device."""
        self._request("daq_start")

    def daq_stop(self) -> bytes:
        """Stop data aquisition for the device."""
        self._request("daq_stop")

    def list_registers(self) -> bytes:
        """List all available registers by name."""
        return self._request("list_registers").decode("utf-8").split()

    def get_register(self, name: str) -> bytes:
        """Get the value of a named register."""
        return int(self._request("get_register", name))

    def set_register(self, name: str, value: float) -> bytes:
        """Set the value of a named register."""
        self._request("set_register", name, value)

    def get_memory(self, name: str) -> bytes:
        """Get the value of a named memory."""
        return int(self._request("get_memory", name))

    def set_memory(self, name: str, value: float) -> bytes:
        """Set the value of a named memory."""
        self._request("set_memory", name, value)

    def get_current(self, name: str) -> bytes:
        """Get the measured current of a named periphery port."""
        return float(self._request("get_current", name))

    def set_current(self, name: str, value: float) -> bytes:
        """Set the current of a named periphery port."""
        self._request("set_current", name, value)

    def get_voltage(self, name: str) -> bytes:
        """Get the measured voltage of a named periphery port."""
        return float(self._request("get_voltage", name))

    def set_voltage(self, name: str, value: float) -> bytes:
        """Set the voltage of a named periphery port."""
        self._request("set_voltage", name, value)

    def switch_on(self, name: str) -> bytes:
        """Switch on a periphery port."""
        self._request("switch_on", name)

    def switch_off(self, name: str) -> bytes:
        """Switch off a periphery port."""
        self._request("switch_off", name)

    # unknown attributes are interpreted as dynamic functions
    # and are forwarded as-is to the pearyd instance
    # sss def __getattr__(self, name: str) -> bytes:
    # sss    func = functools.partial(self._request, name)
    # sss    self.__dict__[name] = func
    # sss    return func
