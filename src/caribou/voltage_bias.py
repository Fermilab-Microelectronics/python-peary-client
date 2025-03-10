from caribou.supply import Supply


class VoltageBias(Supply):
    """A voltage bias."""

    def set_voltage(self, value: float) -> bytes:
        """Set the voltage of the voltage bias."""
        return self.device.set_voltage(self.name, value)

    def get_voltage(self) -> float:
        """Measure the voltage of the voltage bias."""
        return self.device.get_voltage(self.name)

    def switch_on(self) -> bytes:
        """Switch on the voltage bias."""
        return self.device.switch_on(self.name)

    def switch_off(self) -> bytes:
        """Switch off the voltage bias."""
        return self.device.switch_off(self.name)
