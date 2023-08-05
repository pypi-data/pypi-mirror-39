GLOBAL_CRC = None


def calculate_crc_on_bytes(raw_bytes):
    "check if crc is valid for a set of bytes"
    _crccheck = 0xFFFF
    for b in raw_bytes:
        _crccheck = calculate_crc(_crccheck, b)
    return _crccheck == 0


def get_crc_table():
    "Initialize crc_table"
    global GLOBAL_CRC
    if GLOBAL_CRC is None:
        GLOBAL_CRC = list(range(256))
        for i in range(0, 256):
            crc = 0
            c = i
            for j in range(0, 8):
                if ((crc ^ c) & 0x0001):
                    crc = (crc >> 1) ^ 0xA001
                else:
                    crc = crc >> 1
                c = c >> 1
            GLOBAL_CRC[i] = crc
    return GLOBAL_CRC


def calculate_crc(crc, c):
    "Calculate CRC value"
    table = get_crc_table()
    int_c = 0x00ff & c

    tmp = crc ^ int_c
    crc = (crc >> 8) ^ table[tmp & 0xff]
    return crc


def is_record_valid(record):
    "Check that record CRC is valid"
    _crccheck = 0xFFFF
    isvalid = False
    for b in record.databytes:
        _crccheck = calculate_crc(_crccheck, b)
        isvalid = (_crccheck == 0)
    return isvalid
