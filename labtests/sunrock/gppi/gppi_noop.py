"""Mock tests for the GPPI."""

import labtest

import peary


@labtest.register
def gppi_mock() -> None:
    """Mock function for testing the GPPI."""
    with peary.PearyClient("192.168.1.49", port=12345) as client:
        client.keep_alive()
