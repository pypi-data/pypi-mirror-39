import os
from FileTransforms.Result import BaseOutputFile, BaseResult
from FileTransforms.FileType import FileType


def test_constructors():
    assert BaseOutputFile() is not None
    assert BaseResult() is not None


def test_add_row():
    f = BaseOutputFile('test.csv')
    assert [] == f.data
    f.add_row([1, 2])
    assert [[1, 2]] == f.data


def test_write_to_file():
    f = BaseOutputFile('test.csv')
    f.add_row([1, 2])
    f.write_to_file()
    with open(f.file_path, 'r') as tf:
        assert '1,2\n' == tf.read()

    f.headers = ['First', 'Second']
    assert f.write_to_file()

    with open(f.file_path, 'r') as tf:
        assert '"First","Second"\n1,2\n' == tf.read()

    os.remove(f.file_path)


def test_write_to_file2():
    f = BaseOutputFile('test.txt', file_type=FileType.TEXT)
    f.add_row('12')
    f.write_to_file()
    with open(f.file_path, 'r') as tf:
        assert '12\n' == tf.read()

    f.headers = ['These headers will be skipped for FileType.TEXT']
    assert f.write_to_file()

    with open(f.file_path, 'r') as tf:
        assert '12\n' == tf.read()

    os.remove(f.file_path)


def test_write_to_file3():
    f = BaseOutputFile('test.csv')
    assert not f.write_to_file()  # Don't write anything if there is nothing to write
    assert not os.path.exists(f.file_path)


def test_write_to_file4():
    f = BaseOutputFile('test.csv')
    f.file_type = 'This is not a file type'
    f.data = [1, 2]
    assert not f.write_to_file()
    assert not os.path.exists(f.file_path)


def test_get_item():
    f = BaseOutputFile()
    f.headers = ['A', 'B']
    f.add_row([1, 2])
    f.add_row([3, 4])
    assert 1 == f[0, 'A']
    assert 4 == f[1, 1]
    assert f[0, 'Non-existent header'] is None
    assert [1, 2] == f[0]


def test_add_file1():
    result = BaseResult()
    f = result.add_file()
    assert isinstance(f, BaseOutputFile)
    assert FileType.CSV == f.file_type


def test_add_file2():
    result = BaseResult()
    result.add_file('test.csv', common_name='test')
    f = result.get_file('test')
    assert isinstance(f, BaseOutputFile)


def test_add_text_file():
    result = BaseResult()
    f = result.add_text_file('test.txt')
    assert isinstance(f, BaseOutputFile)
    assert FileType.TEXT == f.file_type


def test_write_all():
    result = BaseResult()
    file_names = ['test1.csv', 'test2.csv']
    for filename in file_names:
        f = result.add_file(filename)
        f.add_row([1, 2])

    result.write_all()

    for filename in file_names:
        path = result.get_file(filename).file_path
        assert os.path.exists(path)
        os.remove(path)
