import os
import json
import pytest
from FileTransforms.header_utils import enumerate_headers, generate_header_lookup_dict, load_headers
from FileTransforms.csv_utils import read_csv, write_csv


@pytest.fixture(scope="module")
def generated_test_csv():
    path = 'test.csv'
    with open(path, 'w') as f:
        f.write('File,Transforms\n1,2')

    yield path
    os.remove(path)


@pytest.fixture(scope="module")
def generated_headers_file():
    path = 'headers.json'
    with open(path, 'w') as f:
        json.dump({
            'key1': 'value1',
            'key2': ['value2', 'value3']
        }, f)

    yield path
    os.remove(path)


def test_enumerate_headers1():
    assert ['THING 1'] == enumerate_headers(['THING '], ['THING '])
    assert ['THING 1', 'CAT', ''] == enumerate_headers(['THING ', 'CAT', ''], ['THING '])
    assert ['THING 1', 'THING 2'] == enumerate_headers(['THING ', 'THING 2'], ['THING '])


def test_enumerate_headers2():
    assert ['THING 10'] == enumerate_headers(['THING '], ['THING '], start_idx=10)
    assert ['THING 10', 'CAT'] == enumerate_headers(['THING ', 'CAT'], ['THING '], start_idx=10)


def test_enumerate_headers3():
    assert ['THING 1', 'NOTES_1'] == enumerate_headers(['THING ', 'NOTES_'], ['THING ', 'NOTES_'])
    assert ['THING 10', 'NOTES_10'] == enumerate_headers(['THING ', 'NOTES_'], ['THING ', 'NOTES_'], start_idx=10)


def test_generate_header_lookup_dict1():
    lookup = generate_header_lookup_dict({'key': 'value'})
    assert 'key' not in lookup
    assert lookup['value'] == 'key'


def test_generate_header_lookup_dict2():
    lookup = generate_header_lookup_dict({'key': ['value1', 'value2']})
    assert 'key' not in lookup
    assert lookup['value1'] == 'key'
    assert lookup['value2'] == 'key'


def test_read_csv(generated_test_csv):
    data = read_csv(generated_test_csv)
    assert ['File', 'Transforms'] == data[0]
    assert ['1', '2'] == data[1]


def test_write_csv():
    path = 'write.test.csv'
    write_csv(path, [['File', 'Transforms'], ['1', '2']])
    with open(path, 'r') as f:
        data = f.read()

    assert 'File,Transforms\n1,2\n' == data
    os.remove(path)


def test_load_headers(generated_headers_file):
    header_map = load_headers(generated_headers_file)
    assert header_map['key1'] == 'value1'
    assert header_map['key2'] == ['value2', 'value3']


def test_load_headers2():
    assert load_headers('path does not exist') is None
