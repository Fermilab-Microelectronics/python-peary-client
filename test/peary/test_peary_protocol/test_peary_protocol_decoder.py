import pytest

from peary.peary_protocol import PearyProtocol


def test_peary_protocol_decode_payload() -> None:
    assert (
        PearyProtocol.decode(b"\x00\x00\x00\x09\x00\x00\x00\x00alpha").payload
        == b"alpha"
    )
    assert (
        PearyProtocol.decode(b"\x00\x00\x00\x08\x00\x00\x00\x00beta").payload == b"beta"
    )


def test_peary_protocol_decode_tag() -> None:
    assert PearyProtocol.decode(b"\x00\x00\x00\x04\x00\x00\x00\x00").tag == 0
    assert PearyProtocol.decode(b"\x00\x00\x00\x04\x00\x01\x00\x00").tag == 1


def test_peary_protocol_decode_status() -> None:
    assert PearyProtocol.decode(b"\x00\x00\x00\x04\x00\x00\x00\x00").status == 0
    assert PearyProtocol.decode(b"\x00\x00\x00\x04\x00\x00\x00\x01").status == 1


def test_peary_protocol_decode_insufficient_number_number_of_bytes() -> None:
    with pytest.raises(
        PearyProtocol.DecodeError, match="Insufficent number of bytes: 0"
    ):
        PearyProtocol.decode(b"")
    with pytest.raises(
        PearyProtocol.DecodeError, match="Insufficent number of bytes: 1"
    ):
        PearyProtocol.decode(b".")
    with pytest.raises(
        PearyProtocol.DecodeError, match="Insufficent number of bytes: 2"
    ):
        PearyProtocol.decode(b"..")
    with pytest.raises(
        PearyProtocol.DecodeError, match="Insufficent number of bytes: 3"
    ):
        PearyProtocol.decode(b"...")


def test_peary_protocol_decode_insufficient_number_number_of_bytes_sweep() -> None:
    for ii in range(PearyProtocol.STRUCT_LENGTH.size):
        with pytest.raises(
            PearyProtocol.DecodeError, match=f"Insufficent number of bytes: {ii}"
        ):
            PearyProtocol.decode(bytes(ii))


def test_peary_protocol_decode_incorrect_number_of_bytes() -> None:
    with pytest.raises(PearyProtocol.DecodeError, match="Incorrect number of bytes"):
        PearyProtocol.decode(b"\x00\x00\x00\x03\x00\x00\x00\x00")
    with pytest.raises(PearyProtocol.DecodeError, match="Incorrect number of bytes"):
        PearyProtocol.decode(b"\x00\x00\x00\x05\x00\x00\x00\x00")
