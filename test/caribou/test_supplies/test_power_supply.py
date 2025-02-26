from caribou.power_supply import PowerSupply


class MockDevice:

    def set_voltage(self, name, value):
        return (name, value)

    def get_voltage(self, name):
        return name

    def switch_on(self, name):
        return name

    def switch_off(self, name):
        return name


def test_power_supply_name():
    assert PowerSupply("alpha", None).name == "alpha"
    assert PowerSupply("beta", None).name == "beta"


def test_power_supply_device():
    assert PowerSupply(None, "alpha").device == "alpha"
    assert PowerSupply(None, "beta").device == "beta"


def test_power_supply_set_voltage():
    assert PowerSupply("alpha", MockDevice()).set_voltage(1) == ("alpha", 1)
    assert PowerSupply("beta", MockDevice()).set_voltage(2) == ("beta", 2)


def test_power_supply_get_voltage():
    assert PowerSupply("alpha", MockDevice()).get_voltage() == "alpha"
    assert PowerSupply("beta", MockDevice()).get_voltage() == "beta"


def test_power_supply_switch_on():
    assert PowerSupply("alpha", MockDevice()).switch_on() == "alpha"
    assert PowerSupply("beta", MockDevice()).switch_on() == "beta"


def test_power_supply_switch_off():
    assert PowerSupply("alpha", MockDevice()).switch_off() == "alpha"
    assert PowerSupply("beta", MockDevice()).switch_off() == "beta"
