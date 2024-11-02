from socket import socket as socket_type

import peary
from peary.peary_protocol_interface import PearyProtocolInterface
from peary.peary_proxy import PearyProxy


# pylint: disable=missing-param-doc
class MockProtocol(PearyProtocolInterface):
    def __init__(self, socket: socket_type, timeout: int = 10):
        """Mock __init__"""

    def request(self, msg: str, *args: str, buffer_size: int = 4096):
        """Mock request"""


def test_peary_proxy_keep_alive(monkeypatch, mock_socket):
    def mock_request_name(_):
        pass

    monkeypatch.setattr(
        peary.peary_device.PearyDevice, "_request_name", mock_request_name
    )

    def mock_request(encoded_request, return_value):
        def _mock_request(_, *args):
            nonlocal encoded_request
            nonlocal return_value
            assert " ".join(args).encode("utf-8") == encoded_request
            return return_value

        return _mock_request

    monkeypatch.setattr(MockProtocol, "request", mock_request(b"", b""))
    assert PearyProxy(mock_socket("", ""), MockProtocol).keep_alive() == b""
