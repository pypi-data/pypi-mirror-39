from struct import unpack, calcsize
from .crc import calculate_crc
import logging

logger = logging.getLogger(__name__)

record_format = 'eeeeee'
bytes_per_record = calcsize(record_format)  # 12

MAX_RELATIVE_TIME_SHIFT = 2


def create_record_struct(raw_bytes, next_bytes=None):
    "Takes a pod's 512 bytes and parses returns it parsed into anonymous record struct"
    assert len(raw_bytes) == 512
    raw_data = raw_bytes[30: 510]

    dataRate = raw_bytes[4:6]
    unixtime = raw_bytes[22:30]
    # Check if CRC is valid
    _crccheck = 0xFFFF
    for b in raw_bytes:
        _crccheck = calculate_crc(_crccheck, b)
    isvalid = (_crccheck == 0)
    if (isvalid is False):
        logger.warn("crc check is invalid")
        return None

    unixtime = unpack('d', unixtime)[0]
    dataRate = unpack('h', dataRate)[0]

    isvalid_next = False
    if (next_bytes is not None):
        _crccheck = 0xFFFF
        for b in next_bytes:
            _crccheck = calculate_crc(_crccheck, b)
        isvalid_next = (_crccheck == 0)

    delta_t = 1 / dataRate
    num_entries = 40

    # Calculate time based on time from current record to next if possible. Else use naive method
    # If time difference is too large pod was probably asleep -> use naive
    # If time difference is tiny, something probably went wrong -> use naive
    if isvalid_next:
        unixtime_next = next_bytes[22:30]
        unixtime_next = unpack('d', unixtime_next)[0]
        if delta_t_valid((unixtime_next - unixtime) / num_entries, delta_t):
            delta_t = (unixtime_next - unixtime) / num_entries

    for i, idx in enumerate(range(0, 480, bytes_per_record)):
        gx, gy, gz, ax, ay, az = unpack(record_format, raw_data[idx: idx + bytes_per_record])
        time = int((unixtime + i * delta_t) * 1e6)
        yield {"ax": ax, "ay": ay, "az": az, "gx": gx, "gy": gy, "gz": gz, 'time': time}


def delta_t_valid(new_delta_t, expected_delta_t):
    return new_delta_t / MAX_RELATIVE_TIME_SHIFT <= expected_delta_t <= new_delta_t * MAX_RELATIVE_TIME_SHIFT


def create_structs_from_pod_data(pod, page_start, npages):
    """Reads npages number of pages, returns list of anonymous
    record objects with size npages"""
    if npages < 1:
        raise AttributeError('Number of pages cannot be less than 0')
    if npages > 15:
        raise AttributeError('Number of pages cannot exceed 16 (8192 bytes)')
    page_size = 512
    adr = page_start * page_size
    nbytes = npages * page_size
    response = pod.read_flash(adr, nbytes)
    response = response[4:-2]
    # Convert to byte array
    datab = response.encode()
    # Split response into pages
    yield from create_structs_from_bytes(datab)


def create_structs_from_bytes(raw_bytes):
    "Reads bytes, creates anonymous record objects with size npages"
    page_size = 512
    i = 0
    # Split response into pages
    while (i * page_size < len(raw_bytes)):
        start = i * page_size
        end = start + page_size
        end_next = end + page_size
        if (end_next <= len(raw_bytes)):
            next_struct = create_record_struct(raw_bytes[start:end], raw_bytes[end:end_next])
        else:
            next_struct = create_record_struct(raw_bytes[start:end])
        yield from next_struct
        i = i + 1


def read_pod_raw(pod, page_start, npages, raw_bytes):
    """Reads npages number of pages from pod, returns
    initial raw bytes combined with bytes read"""
    if npages < 1:
        raise AttributeError('Number of pages cannot be less than 0')
    if npages > 15:
        raise AttributeError('Number of pages cannot exceed 16 (8192 bytes)')
    page_size = 512
    adr = page_start * page_size
    nbytes = npages * page_size
    response = pod.read_flash(adr, nbytes)
    response = response[4:-2]
    # Convert to byte array
    datab = response.encode()
    # Split response into pages
    for i in range(npages):
        start = i * page_size
        end = start + page_size
        raw_bytes = raw_bytes + datab[start:end]
    return raw_bytes


def read_flash_structs(pod, page_start, npages, pages_per_read=15):
    "Reads npages number of pages from pod, returns list of anonymous record objects with size npages"
    count = 0
    while count < npages:
        read_pages = pages_per_read if (npages - count) > pages_per_read else (npages - count)
        yield from create_structs_from_pod_data(pod, page_start + count, read_pages)
        count += read_pages


def read_flash_raw(pod, page_start, npages, pages_per_read=15):
    "Reads npages number of pages from pod, returns pages as raw bytes"
    raw_bytes = b''
    count = 0
    while count < npages:
        read_pages = pages_per_read if (npages - count) > pages_per_read else (npages - count)
        raw_bytes = read_pod_raw(pod, page_start + count, read_pages, raw_bytes)
        count += read_pages
    return raw_bytes
