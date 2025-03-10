from __future__ import annotations

from caribou.current_bias import CurrentBias


class MockDevice:

    def set_current(self, name, value):
        return (name, value)

    def get_current(self, name):
        return name

    def switch_on(self, name):
        return name

    def switch_off(self, name):
        return name


def test_current_bias_name():
    assert CurrentBias("alpha", None).name == "alpha"
    assert CurrentBias("beta", None).name == "beta"


def test_current_bias_device():
    assert CurrentBias(None, "alpha").device == "alpha"
    assert CurrentBias(None, "beta").device == "beta"


def test_current_bias_set_current():
    assert CurrentBias("alpha", MockDevice()).set_current(1) == ("alpha", 1)
    assert CurrentBias("beta", MockDevice()).set_current(2) == ("beta", 2)


def test_current_bias_get_current():
    assert CurrentBias("alpha", MockDevice()).get_current() == "alpha"
    assert CurrentBias("beta", MockDevice()).get_current() == "beta"


def test_current_bias_switch_on():
    assert CurrentBias("alpha", MockDevice()).switch_on() == "alpha"
    assert CurrentBias("beta", MockDevice()).switch_on() == "beta"


def test_current_bias_switch_off():
    assert CurrentBias("alpha", MockDevice()).switch_off() == "alpha"
    assert CurrentBias("beta", MockDevice()).switch_off() == "beta"
