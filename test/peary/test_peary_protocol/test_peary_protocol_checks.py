from peary.peary_protocol import PearyProtocol


def test_peary_protocol_class_constants_checks() -> None:
    assert PearyProtocol.Checks.CHECK_VERSION not in PearyProtocol.Checks.CHECK_NONE
