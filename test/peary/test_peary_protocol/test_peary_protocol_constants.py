import struct

from peary.peary_protocol import PearyProtocol


def test_peary_protocol_class_constant_status_ok():
    assert PearyProtocol.STATUS_OK == 0


def test_peary_protocol_class_constant_struct_header():
    assert type(PearyProtocol.STRUCT_HEADER) is type(struct.Struct("!HH"))


def test_peary_protocol_class_constant_struct_lenght():
    assert type(PearyProtocol.STRUCT_LENGTH) is type(struct.Struct("!L"))


def test_peary_protocol_class_constant_version():
    assert PearyProtocol.VERSION == b"1"
