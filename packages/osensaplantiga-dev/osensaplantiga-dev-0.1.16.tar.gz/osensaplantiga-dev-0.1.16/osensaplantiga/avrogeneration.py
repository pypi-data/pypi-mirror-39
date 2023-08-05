from fastavro import writer, parse_schema
from .recordgeneration import create_structs_from_bytes
from .custom_exceptions import NoStructsFoundError, NoBytesFoundError
import io


def create_schema(metadata):

    return parse_schema({
        'name': 'plantiga_device',
        'doc': 'Plantiga Device Data',
        'namespace': 'test',
        'metadata': metadata,
        'type': 'record',
        'fields': [
            {'name': 'time', 'type': 'long'},
            {'name': 'gx', 'type': 'float'},
            {'name': 'gy', 'type': 'float'},
            {'name': 'gz', 'type': 'float'},
            {'name': 'ax', 'type': 'float'},
            {'name': 'ay', 'type': 'float'},
            {'name': 'az', 'type': 'float'},
        ],
    })


def bytes_to_avro(raw_bytes, metadata=None):
    """Takes raw pod data and transforms it into avro format, with optional metadata"""

    if len(raw_bytes) == 0:
        raise NoBytesFoundError("No bytes were found, should be integer > 0")
    record_structs = list(create_structs_from_bytes(raw_bytes))
    schema = create_schema(metadata)
    buffer = io.BytesIO()
    writer(buffer, schema, record_structs)
    if len(record_structs) < 1:
        raise NoStructsFoundError("No structs were generated, should have at least one")

    return buffer.getvalue(), record_structs[0]['time'], record_structs[-1]['time']


def raw_file_to_avro(file_path):
    """Takes a file with raw pod data and transforms it into file with avro format"""
    with open(file_path, 'rb') as f:
        raw_bytes = f.read()
    b = bytes_to_avro(raw_bytes, {})
    new_path = file_path.split('.bin')[0] + '.avro'
    with open(new_path, 'wb') as out:
        out.write(b)
