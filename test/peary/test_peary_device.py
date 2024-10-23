from peary.peary_device import PearyDevice


class MockClient:  # pylint: disable=too-few-public-methods
    def request(self, *args):
        """concatenates the arguments into a string"""
        return bytes(" ".join(args).encode("utf-8"))


# TODO(Jeff): Float tests using this mock are very flakey. Minor changes in the
#       strings are not detected.
class MockClientGetInt:  # pylint: disable=too-few-public-methods
    def request(self, *args):
        """concatenates the arguments into a string"""
        return int.from_bytes(" ".join(args).encode("utf-8"), "big")


class MockDevice(PearyDevice):  # pylint: disable=too-few-public-methods
    def _run_command(self, cmd, *args):  # noqa: ARG002
        """Request a nullary operation from the device."""
        return b""


def test_peary_device_init_index():
    assert PearyDevice(MockClient(), 0).index == 0
    assert PearyDevice(MockClient(), 1).index == 1


def test_peary_device_init_device_type():
    assert PearyDevice(MockClient(), 0).device_type == "device.name 0"
    assert PearyDevice(MockClient(), 1).device_type == "device.name 1"


def test_peary_device_repr():
    assert str(PearyDevice(MockClient(), 0)) == "device.name 0_Device(0)"
    assert str(PearyDevice(MockClient(), 1)) == "device.name 1_Device(1)"


def test_peary_device_power_on():
    assert PearyDevice(MockClient(), 0).power_on() == b"device.power_on 0"


def test_peary_device_power_off():
    assert PearyDevice(MockClient(), 0).power_off() == b"device.power_off 0"


def test_peary_device_reset():
    assert PearyDevice(MockClient(), 0).reset() == b"device.reset 0"


def test_peary_device_configure():
    assert PearyDevice(MockClient(), 0).configure() == b"device.configure 0"


def test_peary_device_daq_start():
    assert PearyDevice(MockClient(), 0).daq_start() == b"device.daq_start 0"


def test_peary_device_daq_stop():
    assert PearyDevice(MockClient(), 0).daq_stop() == b"device.daq_stop 0"


def test_peary_device_list_registers():
    assert PearyDevice(MockClient(), 0).list_registers() == [
        "device.list_registers",
        "0",
    ]


def test_peary_device_get_register():
    assert (MockDevice(MockClientGetInt(), 0).get_register("alpha")).to_bytes(
        27, "big"
    ) == b"device.get_register 0 alpha"

    assert (MockDevice(MockClientGetInt(), 0).get_register("beta")).to_bytes(
        26, "big"
    ) == b"device.get_register 0 beta"


def test_peary_device_set_register():
    assert (
        PearyDevice(MockClient(), 0).set_register("alpha", 0)
        == b"device.set_register 0 alpha 0"
    )
    assert (
        PearyDevice(MockClient(), 0).set_register("beta", 1)
        == b"device.set_register 0 beta 1"
    )


def test_peary_device_get_memory():
    assert (MockDevice(MockClientGetInt(), 0).get_memory("alpha")).to_bytes(
        25, "big"
    ) == b"device.get_memory 0 alpha"

    assert (MockDevice(MockClientGetInt(), 1).get_memory("beta")).to_bytes(
        24, "big"
    ) == b"device.get_memory 1 beta"


def test_peary_device_set_memory():
    assert (
        PearyDevice(MockClient(), 0).set_memory("alpha", 0)
        == b"device.set_memory 0 alpha 0"
    )
    assert (
        PearyDevice(MockClient(), 0).set_memory("beta", 1)
        == b"device.set_memory 0 beta 1"
    )


def test_peary_device_get_current():
    assert MockDevice(MockClientGetInt(), 0).get_current("alpha") == float(
        int.from_bytes(b"device.get_current 0 alpha", "big")
    )
    assert MockDevice(MockClientGetInt(), 1).get_current("beta") == float(
        int.from_bytes(b"device.get_current 1 beta", "big")
    )


def test_peary_device_set_current():
    assert (
        PearyDevice(MockClient(), 0).set_current("alpha", 0)
        == b"device.set_current 0 alpha 0"
    )
    assert (
        PearyDevice(MockClient(), 0).set_current("beta", 1)
        == b"device.set_current 0 beta 1"
    )


def test_peary_device_get_voltage():
    assert MockDevice(MockClientGetInt(), 0).get_voltage("alpha") == float(
        int.from_bytes(b"device.get_voltage 0 alpha", "big")
    )
    assert MockDevice(MockClientGetInt(), 1).get_voltage("beta") == float(
        int.from_bytes(b"device.get_voltage 1 beta", "big")
    )


def test_peary_device_set_voltage():
    assert (
        PearyDevice(MockClient(), 0).set_voltage("name", 0.0)
        == b"device.set_voltage 0 name 0.0"
    )
    assert (
        PearyDevice(MockClient(), 0).set_voltage("name", 1.0)
        == b"device.set_voltage 0 name 1.0"
    )


def test_peary_device_switch_on():
    assert (
        PearyDevice(MockClient(), 0).switch_on("alpha") == b"device.switch_on 0 alpha"
    )
    assert PearyDevice(MockClient(), 0).switch_on("beta") == b"device.switch_on 0 beta"


def test_peary_device_switch_off():
    assert (
        PearyDevice(MockClient(), 0).switch_off("alpha") == b"device.switch_off 0 alpha"
    )
    assert (
        PearyDevice(MockClient(), 0).switch_off("beta") == b"device.switch_off 0 beta"
    )
