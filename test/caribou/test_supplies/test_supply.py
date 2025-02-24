from caribou.supply import Supply


def test_supply_name():
    assert Supply("alpha", None).name == "alpha"
    assert Supply("beta", None).name == "beta"


def test_supply_device():
    assert Supply("", "alpha").device == "alpha"
    assert Supply("", "beta").device == "beta"
