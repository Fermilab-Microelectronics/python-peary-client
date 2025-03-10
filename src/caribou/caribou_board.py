from __future__ import annotations

from enum import Enum
from typing import TYPE_CHECKING

from caribou.current_bias import CurrentBias
from caribou.power_supply import PowerSupply
from caribou.voltage_bias import VoltageBias
from peary.peary_device import PearyDevice
from peary.peary_protocol import PearyProtocol

if TYPE_CHECKING:
    from socket import socket as socket_type

    from peary.peary_protocol_interface import PearyProtocolInterface


class CaribouBoard(PearyDevice):
    """A Caribou Board interface for use with Peary.

    Example of usage:

        func test_setup(vdda=1.2, vddd=1.0, vddio=1.8. vbias=0.4, ibias=0.001):
            device_carboard = client.add_device("SpacelyCaribouBasic", CaribouBoard)

            supply_vdda = device_carboard.power_supply(CaribouBoard.PWR_OUT_1)
            supply_vddd = device_carboard.power_supply(CaribouBoard.PWR_OUT_2)
            supply_vddio = device_carboard.power_supply(CaribouBoard.PWR_OUT_3)
            supply_vbias = device_carboard.voltage_bias(CaribouBoard.VBIAS_1))
            supply_ibias = device_carboard.current_bias(CaribouBoard.IBIAS_1))

            device_carboard.set_logic_level(vddio)
            supply_vdda.set_voltage(vdda)
            supply_vdda.set_voltage(vddd)
            supply_vdda.set_voltage(vddio)
            supply_vdda.set_voltage(vbias)
            supply_vdda.set_voltage(ibias)

            supply_vdda.switch_on()
            supply_vdda.switch_on()
            supply_vdda.switch_on()
            supply_vdda.switch_on()
            supply_vdda.switch_on()

    """

    class PowerSupplyName(Enum):
        """Available caribout board power supply outputs."""

        PWR_OUT_1 = "PWR_OUT_1"
        PWR_OUT_2 = "PWR_OUT_2"
        PWR_OUT_3 = "PWR_OUT_3"
        PWR_OUT_4 = "PWR_OUT_4"
        PWR_OUT_5 = "PWR_OUT_5"
        PWR_OUT_6 = "PWR_OUT_6"
        PWR_OUT_7 = "PWR_OUT_7"
        PWR_OUT_8 = "PWR_OUT_8"

    # TODO(Jeff): Update the Caribou Device to provide access to all 32 biases.
    class VoltageBiasName(Enum):
        """Available caribout board voltage bias outputs."""

        BIAS_1 = "BIAS_1"
        BIAS_2 = "BIAS_2"
        BIAS_3 = "BIAS_3"
        BIAS_4 = "BIAS_4"
        BIAS_5 = "BIAS_5"

    class CurrentBiasName(Enum):
        """Available caribout board current bias outputs."""

        CUR_1 = "CUR_1"
        CUR_2 = "CUR_2"
        CUR_3 = "CUR_3"
        CUR_4 = "CUR_4"
        CUR_5 = "CUR_5"
        CUR_6 = "CUR_6"
        CUR_7 = "CUR_7"
        CUR_8 = "CUR_8"

    class BusI2C(Enum):
        """Available I2C buses."""

        BUS_0 = 0
        BUS_1 = 1
        BUS_2 = 2
        BUS_3 = 3

    PWR_OUT_1 = PowerSupplyName.PWR_OUT_1
    PWR_OUT_2 = PowerSupplyName.PWR_OUT_2
    PWR_OUT_3 = PowerSupplyName.PWR_OUT_3
    PWR_OUT_4 = PowerSupplyName.PWR_OUT_4
    PWR_OUT_5 = PowerSupplyName.PWR_OUT_5
    PWR_OUT_6 = PowerSupplyName.PWR_OUT_6
    PWR_OUT_7 = PowerSupplyName.PWR_OUT_7
    PWR_OUT_8 = PowerSupplyName.PWR_OUT_8

    VBIAS_1 = VoltageBiasName.BIAS_1
    VBIAS_2 = VoltageBiasName.BIAS_2
    VBIAS_3 = VoltageBiasName.BIAS_3
    VBIAS_4 = VoltageBiasName.BIAS_4
    VBIAS_5 = VoltageBiasName.BIAS_5

    IBIAS_1 = CurrentBiasName.CUR_1
    IBIAS_2 = CurrentBiasName.CUR_2
    IBIAS_3 = CurrentBiasName.CUR_3
    IBIAS_4 = CurrentBiasName.CUR_4
    IBIAS_5 = CurrentBiasName.CUR_5
    IBIAS_6 = CurrentBiasName.CUR_6
    IBIAS_7 = CurrentBiasName.CUR_7
    IBIAS_8 = CurrentBiasName.CUR_8

    def __init__(
        self,
        index: int,
        socket: socket_type,
        protocol_class: type[PearyProtocolInterface] = PearyProtocol,
    ) -> None:
        """Initializes a caribou board as a remote peary device.

        Args:
            socket: Socket connected to the remote peary server.
            protocol_class: Protocol used during communication with the peary server.
            index: Numerical identifier for the device.

        """
        super().__init__(index, socket, protocol_class)
        self._power_supply_collection = {
            s: PowerSupply(s.value, self) for s in CaribouBoard.PowerSupplyName
        }
        self._voltage_bias_collection = {
            s: VoltageBias(s.value, self) for s in CaribouBoard.VoltageBiasName
        }

        self._current_bias_collection = {
            s: CurrentBias(s.value, self) for s in CaribouBoard.CurrentBiasName
        }

        # Configure PCA9539 at address 0x76, 6 to generate output enable signals for
        # the power supply compenents, and configure address 0x76, 7 to enable the
        # power supplies.
        self.write_i2c(CaribouBoard.BusI2C.BUS_0, 0x76, 6, 0)
        self.write_i2c(CaribouBoard.BusI2C.BUS_0, 0x76, 7, 0)

    def power_supply(self, name: PowerSupplyName) -> PowerSupply:
        """Returns an available power supply.

        Args:
            name: name of the power supply

        Returns:
            PowerSupply

        """
        return self._power_supply_collection[name]

    def voltage_bias(self, name: VoltageBiasName) -> VoltageBias:
        """Returns an available voltage bias.

        Args:
            name: name of the voltage bias

        Returns:
            VoltageBias

        """
        return self._voltage_bias_collection[name]

    def current_bias(self, name: CurrentBiasName) -> CurrentBias:
        """Returns an available current bias.

        Args:
            name: name of the current bias.

        Returns:
            CurrentBias

        """
        return self._current_bias_collection[name]

    def set_logic_level(self, value: float) -> None:
        """Set the logic level voltages.

        Args:
            value: logic level voltages.

        Returns:
            bytes: return value.
        """
        self._request("setInputCMOSLevel", str(value))
        self._request("setOutputCMOSLevel", str(value))

    def write_i2c(self, bus: BusI2C, comp: int, addr: int, data: int) -> bytes:
        """Writes to the Caribou board I2C inerface.

        Args:
            bus: I2C bus to connect.
            comp: Component address for the connected I2C component.
            addr: Memory address within the connected I2C component.
            data: Data to write to the component memory address.

        Returns:
            bytes: return value.

        """
        return self._request("car_i2c_write", str(bus), str(comp), str(addr), str(data))

    def read_i2c(self, bus: BusI2C, comp: int, addr: int, length: int) -> bytes:
        """Reads from the Caribou board I2C inerface.

        Args:
            bus: I2C bus to connect.
            comp: Component address for the connected I2C component.
            addr: Memory address within the connected I2C component.
            length: Lenght of data to read from the component memory address.

        Returns:
            bytes: return value.
        """
        return self._request(
            "car_i2c_read", str(bus), str(comp), str(addr), str(length)
        )
