from .avrogeneration import bytes_to_avro
from fastavro import reader
from .custom_exceptions import NoStructsFoundError
import io
import pytest


def test_avro_generation():
    with open("osensaplantiga/test_data/record.bin", "rb") as f:
        record_bytes = f.read()
    metadata = {'firmware_version': 1.04}
    avro_data, t1_us, t2_us = bytes_to_avro(record_bytes, metadata)
    buffer = io.BytesIO(avro_data)
    avro_reader = reader(buffer)
    records = list(avro_reader)
    record_1 = records[0]
    assert avro_reader.schema['metadata'] == metadata
    assert t1_us < t2_us
    assert t1_us == 1541183746284365
    assert record_1['ax'] == 1.2392578125
    assert record_1['ay'] == -0.366455078125
    assert record_1['az'] == 0.54150390625
    assert record_1['gx'] == -98.4375
    assert record_1['gy'] == -252.875
    assert record_1['gz'] == -47.375
    assert record_1['time'] == 1541183746284365


def test_avro_generation_no_structs():
    record_bytes_bad = bytearray(512)
    metadata = {'firmware_version': 1.04}
    with pytest.raises(NoStructsFoundError) as nsfe:
        bytes_to_avro(record_bytes_bad, metadata)
    assert str(nsfe.value) == 'No structs were generated, should have at least one'
