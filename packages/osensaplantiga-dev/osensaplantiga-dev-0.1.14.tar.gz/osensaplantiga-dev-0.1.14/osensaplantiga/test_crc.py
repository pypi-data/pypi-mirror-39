import os
from .crc import calculate_crc

TEST_BIN_PATH = os.path.abspath(os.path.join(__file__, "..", "test_data", "record.bin"))


def test_expected_crc():

    with open(TEST_BIN_PATH, "rb") as fd:
        record_bytes = fd.read()

    _crccheck = 0xFFFF
    isvalid = False
    for b in record_bytes:
        _crccheck = calculate_crc(_crccheck, b)
        isvalid = (_crccheck == 0)

    assert isvalid, "CRC check failed for test data"
