from struct import pack
from unittest import mock
import pytest

from .recordgeneration import create_record_struct, calculate_crc, create_structs_from_bytes, delta_t_valid
from .test_data.gen_test_data import gen_test_data


def test_record_generation_naive():

    # with open("osensaplantiga/test_data/record.bin", "rb") as f:
    record_bytes, _, _ = gen_test_data(ts=1540000001.0)
    record_struct = create_record_struct(record_bytes)

    record_1 = next(record_struct)
    assert record_1['gx'] == 0.0
    assert record_1['gy'] == 1.0
    assert record_1['gz'] == 2.0
    assert record_1['ax'] == 3.0
    assert record_1['ay'] == 4.0
    assert record_1['az'] == 5.0
    assert record_1['time'] == 1540000001 * 1e6

    record_2 = next(record_struct)
    assert record_2['gx'] == 100.0
    assert record_2['gy'] == 101.0
    assert record_2['gz'] == 102.0
    assert record_2['ax'] == 103.0
    assert record_2['ay'] == 104.0
    assert record_2['az'] == 105.0
    assert record_2['time'] == (1540000001 * 1e6) + (1e6 // 416)

    delta = record_2['time'] - record_1['time']
    assert delta == 1e6 // 416


def test_record_generation_time():

    with open("osensaplantiga/test_data/multi_records.bin", "rb") as f:
        record_bytes = f.read()
    structs = list(create_structs_from_bytes(record_bytes))
    entries_per_record = 40
    record_1_pt_1 = structs[0]
    assert record_1_pt_1['time'] == 1535138861446991
    record_1_pt_2 = structs[1]
    assert record_1_pt_2['time'] == 1535138861448189
    record_2_pt_1 = structs[entries_per_record]

    delta_expected = (record_2_pt_1['time'] - record_1_pt_1['time']) // entries_per_record
    delta_t = (record_1_pt_2['time'] - record_1_pt_1['time'])
    assert delta_expected == delta_t


@mock.patch('osensaplantiga.recordgeneration.calculate_crc')
@mock.patch('osensaplantiga.recordgeneration.delta_t_valid')
def test_record_generation_new_rate(delta_t_valid, calculate_crc):
    calculate_crc.return_value = 0
    delta_t_valid.return_value = True
    with open("osensaplantiga/test_data/record.bin", "rb") as f:
        record_bytes = f.read()
    initial_time = 0
    # Double record time diff
    next_time = initial_time + 40.000000
    next_time_packed = pack('d', next_time)
    initial_time_packed = pack('d', initial_time)

    record_bytes_later = record_bytes[0:22] + next_time_packed + record_bytes[30:512]
    record_bytes = record_bytes[0:22] + initial_time_packed + record_bytes[30:512]
    all_bytes = record_bytes + record_bytes_later
    structs = list(create_structs_from_bytes(all_bytes))
    assert len(structs) == 80
    record_1_pt_1 = structs[0]
    assert record_1_pt_1['time'] == 0
    record_1_pt_2 = structs[1]
    # First record's entries should use custom rate
    assert record_1_pt_2['time'] == 1e6
    delta_records = record_1_pt_2['time'] - record_1_pt_1['time']
    assert delta_records == 1e6
    record_2_pt_1 = structs[40]
    expected_time = 40e6
    assert record_2_pt_1['time'] == expected_time
    record_2_pt_2 = structs[41]
    expected_time = 40e6 + 1200
    # Last record's entries should use naive method
    assert record_2_pt_2['time'] == expected_time
    delta_records = record_2_pt_2['time'] - record_2_pt_1['time']
    assert delta_records == 1e6 // 833


@pytest.mark.parametrize("new_delta_t, expected_delta_t, answer, message", [
    (1 / 200, 1 / 800, False, "Min naive should be 1/400"),
    (1 / 1600, 1 / 800, True, "1/1600 should be valid for 1/800 naive"),
    (100, 1 / 800, False, "Min naive should be 1/400"),
    (1 / 1000000, 1 / 800, False, "Max naive should be 1/1600"),
    (1 / 200, 1 / 400, True, "1/200 should be valid for 1/400 naive"),
    (1 / 1600, 1 / 400, False, "Max naive should be 1/800"),
    (100, 1 / 400, False, "Min naive should be 1/200"),
    (1 / 1000000, 1 / 400, False, "Max naive should be 1/800")
])
def test_delta_t_valid(new_delta_t, expected_delta_t, answer, message):
    assert delta_t_valid(new_delta_t, expected_delta_t) == answer, message


def test_invalid_crc():
    with open("osensaplantiga/test_data/record.bin", "rb") as f:
        record_bytes = f.read()
    record_bytes_bad = record_bytes[0:22] + b'FFAA0066' + record_bytes[30:512]

    _crccheck = 0xFFFF
    for b in record_bytes:
        _crccheck = calculate_crc(_crccheck, b)
    isvalid = (_crccheck == 0)
    assert (isvalid is True)

    _crccheck = 0xFFFF
    for b in record_bytes_bad:
        _crccheck = calculate_crc(_crccheck, b)
    isvalid = (_crccheck == 0)
    assert (isvalid is False)


def test_record_struct_has_no_nones():
    with open("osensaplantiga/test_data/record.bin", "rb") as f:
        record_bytes = f.read()
    record_bytes_bad = record_bytes[0:22] + b'FFAA0066' + record_bytes[30:512]
    all_bytes = record_bytes + record_bytes_bad

    structs = list(create_structs_from_bytes(record_bytes))
    assert len(structs) == 40
    struct_bad = list(create_structs_from_bytes(record_bytes_bad))
    assert len(struct_bad) == 0
    struct_s_both = list(create_structs_from_bytes(all_bytes))
    assert len(struct_s_both) == 40
