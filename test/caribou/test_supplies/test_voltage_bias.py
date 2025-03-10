from __future__ import annotations

from caribou.voltage_bias import VoltageBias


class MockDevice:

    def set_voltage(self, name, value):
        return (name, value)

    def get_voltage(self, name):
        return name

    def switch_on(self, name):
        return name

    def switch_off(self, name):
        return name


def test_voltage_bias_name():
    assert VoltageBias("alpha", None).name == "alpha"
    assert VoltageBias("beta", None).name == "beta"


def test_voltage_bias_device():
    assert VoltageBias(None, "alpha").device == "alpha"
    assert VoltageBias(None, "beta").device == "beta"


def test_voltage_bias_set_voltage():
    assert VoltageBias("alpha", MockDevice()).set_voltage(1) == ("alpha", 1)
    assert VoltageBias("beta", MockDevice()).set_voltage(2) == ("beta", 2)


def test_voltage_bias_get_voltage():
    assert VoltageBias("alpha", MockDevice()).get_voltage() == "alpha"
    assert VoltageBias("beta", MockDevice()).get_voltage() == "beta"


def test_voltage_bias_switch_on():
    assert VoltageBias("alpha", MockDevice()).switch_on() == "alpha"
    assert VoltageBias("beta", MockDevice()).switch_on() == "beta"


def test_voltage_bias_switch_off():
    assert VoltageBias("alpha", MockDevice()).switch_off() == "alpha"
    assert VoltageBias("beta", MockDevice()).switch_off() == "beta"
