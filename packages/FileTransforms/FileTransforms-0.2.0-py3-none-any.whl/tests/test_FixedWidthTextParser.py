import os
import pytest
from FileTransforms.FixedWidthTextParser import FixedWidthTextParser


@pytest.fixture(scope="module")
def generated_test_file():
    path = 'test.txt'
    with open(path, 'w') as f:
        f.write('File\nTransforms')

    yield path
    os.remove(path)


def test_constructor():
    t = FixedWidthTextParser([1, 1])
    assert t is not None


def test_read_fix_width1():
    t = FixedWidthTextParser([1, 1])
    assert ['a', 'b'] == t.read_fixed_width('ab')
    assert ['a'] == t.read_fixed_width('a')


def test_read_fix_width2():
    t = FixedWidthTextParser([-3, 1])
    assert ['a'] == t.read_fixed_width('abba')


def test_read_fix_width3():
    t = FixedWidthTextParser({'a': [1, 1]})
    assert ['a', 'b'] == t.read_fixed_width('abba')
    assert [] == t.read_fixed_width('b')


def test_read_fix_width4():
    t = FixedWidthTextParser({'b': [1, 1, 12, 12]})
    assert ['b', 'b', 'a'] == t.read_fixed_width('bba')


def test_read_file1(generated_test_file):
    t = FixedWidthTextParser([-3, 1])
    assert [['e'], ['n']] == t.read_file(generated_test_file)


def test_read_file2(generated_test_file):
    t = FixedWidthTextParser({'a': [1, 1]})
    assert [[], []] == t.read_file(generated_test_file)
