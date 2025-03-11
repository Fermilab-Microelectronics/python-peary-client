import struct

from peary.peary_protocol import PearyProtocol


def test_peary_protocol_class_constant_status_ok() -> None:
    assert PearyProtocol.STATUS_OK == 0


def test_peary_protocol_class_constant_struct_header() -> None:
    assert PearyProtocol.STRUCT_HEADER.format == struct.Struct("!HH").format


def test_peary_protocol_class_constant_struct_lenght() -> None:
    assert PearyProtocol.STRUCT_LENGTH.format == struct.Struct("!L").format


def test_peary_protocol_class_constant_version() -> None:
    assert PearyProtocol.VERSION == b"1"
