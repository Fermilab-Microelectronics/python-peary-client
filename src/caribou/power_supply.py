from caribou.supply import Supply


class PowerSupply(Supply):
    """A power supply."""

    def set_voltage(self, value: float) -> bytes:
        """Set the voltage of the power supply."""
        return self.device.set_voltage(self.name, value)

    def get_voltage(self) -> float:
        """Measure the voltage of the power supply."""
        return self.device.get_voltage(self.name)

    def switch_on(self) -> bytes:
        """Switch on the power supply."""
        return self.device.switch_on(self.name)

    def switch_off(self) -> bytes:
        """Switch off the power supply."""
        return self.device.switch_off(self.name)
