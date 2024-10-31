from peary.peary_protocol import PearyProtocol


def test_peary_protocol_encode_payload():
    assert (
        PearyProtocol.encode(b"alpha", 0, 0) == b"\x00\x00\x00\x09\x00\x00\x00\x00alpha"
    )
    assert (
        PearyProtocol.encode(b"beta", 0, 0) == b"\x00\x00\x00\x08\x00\x00\x00\x00beta"
    )


def test_peary_protocol_encode_header_id():
    assert PearyProtocol.encode(b"", 0, 0) == b"\x00\x00\x00\x04\x00\x00\x00\x00"
    assert PearyProtocol.encode(b"", 1, 0) == b"\x00\x00\x00\x04\x00\x01\x00\x00"


def test_peary_protocol_encode_header_status():
    assert PearyProtocol.encode(b"", 0, 0) == b"\x00\x00\x00\x04\x00\x00\x00\x00"
    assert PearyProtocol.encode(b"", 0, 1) == b"\x00\x00\x00\x04\x00\x00\x00\x01"


def test_peary_protocol_encode_length():
    assert PearyProtocol.encode(b"", 0, 0) == b"\x00\x00\x00\x04\x00\x00\x00\x00"
    assert PearyProtocol.encode(b"1", 0, 0) == b"\x00\x00\x00\x05\x00\x00\x00\x001"
    assert PearyProtocol.encode(b"12", 0, 0) == b"\x00\x00\x00\x06\x00\x00\x00\x0012"
    assert PearyProtocol.encode(b"123", 0, 0) == b"\x00\x00\x00\x07\x00\x00\x00\x00123"
