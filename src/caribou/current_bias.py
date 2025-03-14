from caribou.supply import Supply


class CurrentBias(Supply):
    """A current bias."""

    def set_current(self, value: float) -> bytes:
        """Set the current of the current bias."""
        return self.device.set_current(self.name, value)

    def get_current(self) -> float:
        """Measure the current of the current bias."""
        return self.device.get_current(self.name)

    def switch_on(self) -> bytes:
        """Switch on the current bias."""
        return self.device.switch_on(self.name)

    def switch_off(self) -> bytes:
        """Switch off the current bias."""
        return self.device.switch_off(self.name)
