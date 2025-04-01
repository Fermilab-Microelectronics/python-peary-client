from __future__ import annotations

import socket as socket_module

from peary.peary_device import PearyDevice
from peary.peary_protocol import PearyProtocol


def test_peary_device_init_index() -> None:
    protocol = PearyProtocol(
        socket_module.socket(), checks=PearyProtocol.Checks.CHECK_NONE
    )
    assert PearyDevice(0, protocol).index == 0
    assert PearyDevice(1, protocol).index == 1


def test_peary_device_init_name() -> None:
    protocol = PearyProtocol(
        socket_module.socket(), checks=PearyProtocol.Checks.CHECK_NONE
    )
    assert PearyDevice(0, protocol).protocol is protocol
