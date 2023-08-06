import os
import pytest
import json
from FileTransforms.Transform import BaseTransform, FixedWidthTransform, SingleLineFixedWidthTransform
from FileTransforms.Result import BaseResult
from FileTransforms.ColumnMod import ColumnMod
from FileTransforms.Exceptions import ProcessingFunctionReturnError


def write_file(path, data):
    with open(path, 'w') as f:
        f.write(data)
    return path


@pytest.fixture(scope="module")
def generated_input_csv() -> str:
    path = 'test.csv'
    yield write_file(path, 'A,B\nJohn,Doe')
    os.remove(path)


@pytest.fixture(scope="module")
def generated_input_csv2() -> str:
    path = 'test2.csv'
    yield write_file(path, 'A,B\nJohn,Doe\n')
    os.remove(path)


@pytest.fixture(scope="module")
def generated_input_fixed_width() -> str:
    path = 'fixed.width.txt'
    yield write_file(path, 'A    B    \nJohn Doe  ')
    os.remove(path)


@pytest.fixture(scope="module")
def generated_input_single_line_fixed_width() -> str:
    path = 'single.line.fixed.width.txt'
    yield write_file(path, 'A    B    John Doe  \n')
    os.remove(path)


@pytest.fixture(scope="module")
def generated_headers_map() -> str:
    path = 'test.json'
    with open(path, 'w') as f:
        json.dump({
            'FIRST NAME': 'A',
            'LAST NAME': 'B',
            'ADDRESS': 'C',
        }, f)

    yield path
    os.remove(path)


@pytest.fixture
def basic_transform(generated_headers_map):
    t = BaseTransform()
    t.has_headers = True
    t.headers_file_path = generated_headers_map
    return t


@pytest.fixture
def basic_transform2(basic_transform):
    def modify_data(data):
        for r in data:
            r[0] = len(data)

        return data

    basic_transform.processing_funcs.append(modify_data)
    return basic_transform


def test_constructors():
    assert BaseTransform() is not None
    assert ColumnMod() is not None
    assert FixedWidthTransform((1,)) is not None
    assert SingleLineFixedWidthTransform((1,)) is not None

    result = BaseResult()
    t = BaseTransform(result)
    assert result == t.result


def test_contains_headers():
    t = BaseTransform()
    t.headers = ['A', 'B']
    assert t.contains_headers(['A'])
    assert t.contains_headers(['B', 'A'])
    assert not t.contains_headers(['B', 'C'])


def test_get_header_idx():
    t = BaseTransform()
    t.headers = ['A', 'B']
    assert 0 == t.get_header_idx('A')
    assert 1 == t.get_header_idx('B')
    assert -1 == t.get_header_idx('C')


def test_get_header_indices():
    t = BaseTransform()
    t.headers = ['A', 'B']
    idx = t.get_header_indices(['A', 'B', 'C'])
    assert 0 == idx['A']
    assert 1 == idx['B']
    assert idx['C'] is None


def test_get_output_file_path():
    t = BaseTransform()
    t.output_name = 'output.csv'
    assert os.path.join('/test/path', 'output.csv') == t.get_output_file_path('/test/path/input.csv')
    assert os.path.join('~/Desktop', 'output.csv') == t.get_output_file_path()


def test_remove_token_from_headers_map():
    t = BaseTransform()
    header_map = {'A': '1'}
    t.remove_token_from_headers_map(header_map, '1')
    assert 'A' not in header_map


def test_remove_token_from_headers_map2():
    t = BaseTransform()
    t.enumerable_headers.append('ENUM_')
    header_map = {'A': 'ENUM_'}
    t.remove_token_from_headers_map(header_map, 'ENUM_')
    assert 'A' in header_map


def test_parse_headers():
    t = BaseTransform()
    t.header_map = {'A': 'NAME', 'B': 'ADDRESS'}
    t.headers = ['A', 'B']
    assert ['NAME', 'ADDRESS'] == t.parse_headers()


def test_parse_headers2():
    t = BaseTransform()
    t.headers = ['A', 'B']
    assert ['A', 'B'] == t.parse_headers()


def test_parse_headers3():
    t = BaseTransform()
    t.header_map = {'A': 'NAME', 'B': 'ADDRESS'}
    assert t.parse_headers() is None


def test_parse_headers4():
    t = BaseTransform()
    t.header_map = {'A': 'NAME', 'B': 'ADDRESS'}
    t.headers = [None, 'B']
    assert ['', 'ADDRESS'] == t.parse_headers()


def test_parse_headers5():
    t = BaseTransform()
    t.header_map = {'A': 'FIRST NAME', 'B': 'LAST NAME'}
    t.headers = ['A', 'B', 'ADDRESS']
    t.valid_headers = ['FIRST NAME', 'LAST NAME', 'ADDRESS']
    assert ['FIRST NAME', 'LAST NAME', 'ADDRESS'] == t.parse_headers()


def test_parse_headers6():
    t = BaseTransform()
    t.header_map = {'A': 'FIRST NAME', 'B': 'LAST NAME'}
    t.headers = ['A', 'B', 'ADDRESS']
    t.valid_headers = ['FIRST NAME', 'LAST NAME', 'SKIP']
    t.default_not_found = 'SKIP'
    assert ['FIRST NAME', 'LAST NAME', 'SKIP'] == t.parse_headers()


def test_parse_headers7():
    t = BaseTransform()
    t.header_map = {'A': 'FIRST NAME', 'Column B': 'LAST NAME', 'C': 'NOTES'}
    t.headers = ['A', 'Column  B', 'C']
    t.valid_headers = ['FIRST NAME', 'LAST NAME', 'NOTES']
    t.prefixable_headers.append('NOTES')
    assert ['FIRST NAME', 'LAST NAME', 'NOTES'] == t.parse_headers()
    assert t.column_mods[2].prefix == 'C: '


def test_parse_headers8(basic_transform):
    basic_transform.header_map = {'C': 'NOTES'}
    basic_transform.headers = ['A', 'B', 'C']
    basic_transform.valid_headers = ['FIRST NAME', 'LAST NAME', 'NOTES']
    basic_transform.prefixable_headers.append('NOTES')
    assert ['FIRST NAME', 'LAST NAME', 'NOTES'] == basic_transform.parse_headers()


def test_try_header_variations1():
    t = BaseTransform()
    t.header_map = {'0123456789': 'NAME'}
    assert (False, 'A') == t.try_header_variations('A', t.header_map, ['NAME'])
    assert (True, 'NAME') == t.try_header_variations('1123456789', t.header_map, ['NAME'])


def test_try_header_variations2():
    t = BaseTransform()
    header_map = {'A': 'NAME'}
    assert (True, 'NAME') == t.try_header_variations('name', header_map, ['NAME'])


def test_try_header_variations3():
    t = BaseTransform()
    t.header_map = {'COLUMN A': 'NAME'}
    t._generate_variations = lambda s: [s, 'COLUMN ' + s]
    assert (True, 'NAME') == t.try_header_variations('a', t.header_map, ['NAME'])


def test_try_header_variations4():
    t = BaseTransform()
    t.header_map = {'NAME': 'FULL_NAME', 'AME': 'OTHER'}
    assert (True, 'FULL_NAME') == t.try_header_variations('Full Name', t.header_map, ['FULL_NAME'])


def test_process_input_data():
    t = BaseTransform()
    t.input_validate_func = lambda i, r: (i % 2 == 0, r)
    data = t._process_input_data([
        ['A', 'B'],
        [1, 2],
        [3, 4],
        [5, 6],
        [7, 8],
    ])
    assert [['A', 'B'], [3, 4], [7, 8]] == data


def test_apply_column_mods():
    t = BaseTransform()
    assert [['1', '2', '3']] == t._apply_column_mods([['1', '2', '3']])
    t.column_mods[0] = ColumnMod(prefix='A: ')
    t.column_mods[1] = ColumnMod(suffix=' (B)')
    t.column_mods[2] = ColumnMod(func=lambda s: s * 3)
    t.column_mods[3] = ColumnMod(prefix='Extra: ')
    assert [['A: 1', '2 (B)', '333']] == t._apply_column_mods([['1', '2', '3']])


def test_run_processing_funcs1(basic_transform):
    assert [] == basic_transform.run_processing_funcs(None)

    def drop_data(_):
        return None

    # noinspection PyTypeChecker
    basic_transform.processing_funcs.extend((drop_data, drop_data))
    with pytest.raises(ProcessingFunctionReturnError):
        basic_transform.run_processing_funcs([[1, 2], [3, 4]])


def test_run_processing_funcs2(basic_transform):
    def reverse_rows(data):
        return data[::-1]

    basic_transform.processing_funcs.append(reverse_rows)
    assert [[3, 4], [1, 2]] == basic_transform.run_processing_funcs([[1, 2], [3, 4]])


def test_run_with_nothing(basic_transform):
    result = basic_transform.run(write_output=False)
    assert 0 == len(result.output_files)


def test_run_with_data1(basic_transform):
    data = [
        ['A', 'B'],
        ['John', 'Doe']
    ]
    result = basic_transform.run(data=data, write_output=False)
    f = result.get_file(basic_transform.output_name)
    assert ['FIRST NAME', 'LAST NAME'] == f.headers
    assert ['John', 'Doe'] == f[0]
    assert 1 == len(f.data)


def test_run_with_data2(basic_transform):
    data = [
        ['A', 'B'],
        ['John', 'Doe']
    ]
    basic_transform.run(data=data, write_output=False)
    result = basic_transform.run(data=[], write_output=False)
    f = result.get_file(basic_transform.output_name)
    assert ['FIRST NAME', 'LAST NAME'] == f.headers
    assert ['John', 'Doe'] == f[0]
    assert 1 == len(f.data)


def test_run_with_data3(basic_transform):
    data = [['John', 'Doe']]
    basic_transform.headers = ['FIRST NAME', 'LAST NAME']
    basic_transform.has_headers = False
    basic_transform.run(data=data, write_output=False)
    result = basic_transform.run(data=[], write_output=False)
    f = result.get_file(basic_transform.output_name)
    assert ['FIRST NAME', 'LAST NAME'] == f.headers
    assert ['John', 'Doe'] == f[0]
    assert 1 == len(f.data)


def test_run_with_file1(basic_transform, generated_input_csv):
    result = basic_transform.run(generated_input_csv, write_output=False)
    f = result.get_file(basic_transform.output_name)
    assert ['FIRST NAME', 'LAST NAME'] == f.headers
    assert ['John', 'Doe'] == f[0]
    assert 1 == len(f.data)


def test_run_with_file2(basic_transform, generated_input_csv):
    result = basic_transform.run(file_paths=[generated_input_csv], write_output=False)
    f = result.get_file(basic_transform.output_name)
    assert ['FIRST NAME', 'LAST NAME'] == f.headers
    assert ['John', 'Doe'] == f[0]
    assert 1 == len(f.data)


def test_run_with_file3(basic_transform, generated_input_csv):
    """
    Verify that a file is only read once regardless of how many times the path is included as an argument

    :param basic_transform: pytest fixture - instance of BaseTransform
    :param generated_input_csv: pytest fixture - test input file path
    """
    result = basic_transform.run(generated_input_csv, [generated_input_csv, generated_input_csv], write_output=False)
    f = result.get_file(basic_transform.output_name)
    assert ['FIRST NAME', 'LAST NAME'] == f.headers
    assert ['John', 'Doe'] == f[0]
    assert 1 == len(f.data)


def test_run_with_file4(basic_transform2, generated_input_csv, generated_input_csv2):
    """
    Read from two separate files and process them separately before combining them.

    :param basic_transform2: pytest fixture - instance of BaseTransform with a processing function
    :param generated_input_csv: pytest fixture - test input file path
    """

    result = basic_transform2.run(file_paths=[generated_input_csv, generated_input_csv2], write_output=False)
    f = result.get_file(basic_transform2.output_name)
    assert ['FIRST NAME', 'LAST NAME'] == f.headers
    assert [1, 'Doe'] == f[0]
    assert [1, 'Doe'] == f[1]
    assert 2 == len(f.data)


def test_run_with_file5(basic_transform2, generated_input_csv, generated_input_csv2):
    """
    Read from two separate files and process them separately before combining them.

    :param basic_transform2: pytest fixture - instance of BaseTransform with a processing function
    :param generated_input_csv: pytest fixture - test input file path
    """
    basic_transform2.combine_inputs = True

    result = basic_transform2.run(file_paths=[generated_input_csv, generated_input_csv2], write_output=False)
    f = result.get_file(basic_transform2.output_name)
    assert ['FIRST NAME', 'LAST NAME'] == f.headers
    assert [2, 'Doe'] == f[0]
    assert [2, 'Doe'] == f[1]
    assert 2 == len(f.data)


def test_run_write_output(basic_transform, generated_input_csv):
    result = basic_transform.run(generated_input_csv)
    file_path = result.get_file(basic_transform.output_name).file_path
    assert os.path.exists(file_path)
    assert os.path.dirname(generated_input_csv) == os.path.dirname(file_path)
    os.remove(file_path)


def test_fixed_width(generated_input_fixed_width):
    t = FixedWidthTransform(field_widths=(5, 5))
    f = t.run(generated_input_fixed_width, write_output=False).get_file(t.output_name)
    assert not t.has_headers
    assert ['A', 'B'] == f[0]
    assert ['John', 'Doe'] == f[1]


def test_single_line_fixed_width(generated_input_single_line_fixed_width):
    t = SingleLineFixedWidthTransform(field_widths=(5, 5))
    t.line_length = 10
    f = t.run(generated_input_single_line_fixed_width, write_output=False).get_file(t.output_name)
    assert not t.has_headers
    assert ['A', 'B'] == f[0]
    assert ['John', 'Doe'] == f[1]
    assert 2 == len(f.data)


def test_column_apply():
    m = ColumnMod(prefix='Prefix: ')
    assert 'Prefix: value' == m.apply('value')
    m = ColumnMod(suffix=' (Suffix)')
    assert 'value (Suffix)' == m.apply('value')
    m = ColumnMod(func=lambda x: x * 5)
    assert '_____' == m.apply('_')
    m = ColumnMod(prefix='Prefix: ', suffix=' (Suffix)', func=lambda x: x * 5)
    assert 'Prefix: _____ (Suffix)' == m.apply('_')
