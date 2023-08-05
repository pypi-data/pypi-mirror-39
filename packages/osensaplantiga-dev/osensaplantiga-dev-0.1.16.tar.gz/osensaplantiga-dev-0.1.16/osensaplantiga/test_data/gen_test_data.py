import time
from struct import pack
from osensaplantiga.crc import calculate_crc


def row_func(i):
    'generate a record row'
    return [(i * 100 + b) for b in range(6)]


def gen_test_data(ts=None, dataRate=416, row=row_func):
    '''
    create test data for testing!

    :param ts: start time in seconds
    :param dataRate: number of samples taken in one second
    :param row: function(i: record number) => a list of six values for [gx,gy,gz,ax,ay,az]
    :return: records as a length 512 bytes
    '''
    test_data = bytearray(512)

    if ts is None:
        # time to the nearest second
        ts = time.time() // 1

    test_data[4:6] = pack('h', dataRate)
    test_data[22:30] = pack('d', ts)

    for i, idx in enumerate(range(30, 510, 12)):
        ga = row(i)
        test_data[idx:idx + 12] = pack('eeeeee', *ga)

    start_us = int(ts * 1e6)

    _crccheck = 0xFFFF
    for b in test_data[:-2]:
        _crccheck = calculate_crc(_crccheck, b)

    # Compute valid CRC check for input data
    test_data[-2] = 0x00ff & _crccheck
    _crccheck = calculate_crc(_crccheck, 0x00ff & _crccheck)
    test_data[-1] = 0x00ff & _crccheck
    _crccheck = calculate_crc(_crccheck, 0x00ff & _crccheck)

    assert _crccheck == 0

    end_us = start_us + int(39e6 // dataRate)

    return bytes(test_data), start_us, end_us
