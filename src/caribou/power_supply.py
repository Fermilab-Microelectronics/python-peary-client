from caribou.supply import Supply


class PowerSupply(Supply):
    """A power supply."""

    def set_voltage(self, value: float) -> bytes:
        """Set the voltage for the power supply."""
        return self.device.set_voltage(self.name, value)

    def get_voltage(self) -> float:
        """Get the measured voltage of a named periphery port."""
        return self.device.get_voltage(self.name)
