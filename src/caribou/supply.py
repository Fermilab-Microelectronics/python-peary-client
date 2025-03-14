from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from peary.peary_device import PearyDevice


class Supply:
    """Base defintions for a supply."""

    def __init__(self, name: str, device: PearyDevice) -> None:
        """Initializes a new supply.

        Args:
            name: Name of supply.
            device: Parent device handle of supply.

        """
        self._name = name
        self._device: PearyDevice = device

    @property
    def name(self) -> str:
        """Returns the supply name."""
        return self._name

    @property
    def device(self) -> PearyDevice:
        """Returns the supply parent device."""
        return self._device
