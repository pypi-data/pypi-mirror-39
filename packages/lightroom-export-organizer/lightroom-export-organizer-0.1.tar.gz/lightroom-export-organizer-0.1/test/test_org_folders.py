import os
import shutil
import pytest
import tempfile
from os import path
from collections import defaultdict
from tempfile import NamedTemporaryFile

from lightroom_export_organizer.org_folders import (
    do,
    do2,
    undo,
    validate_file_pairs,
    read_keyword,
    make_file_list,
    file_parts,
    parse_file_pairs,
    lower_extensions,
    lower_extension
)


@pytest.fixture(scope='session')
def fixture_dir():
    return path.join(path.dirname(__file__), 'fixtures')


@pytest.fixture(scope="function")
def fail_case_file_list(fixture_dir):
    with open(fixture_dir, 'r') as fp:
        lines = [line for line in fp.readlines()]
    return lines


@pytest.fixture(scope="function")
def test_fn():
    with tempfile.NamedTemporaryFile('w', delete=False) as fp:
        fp.write("beeb: dest1\n")
    yield fp.name

    if path.isfile(fp.name):
        os.remove(fp.name)


@pytest.fixture(scope="function")
def test_info(tmpdir_factory):

    def touch(fn, keyword):
        with open(fn, 'a') as fp:
            fp.write("beeb: {}\n".format(keyword))

    def make_pair(base_fn, keyword, bad=False):
        touch(base_fn + ".jpg", keyword)
        if not bad:
            touch(base_fn + ".txt", keyword)

    dir_base = str(tmpdir_factory.mktemp("test_dir_base"))
    tmpdir_maker = defaultdict(lambda: path.join(dir_base, str(tmpdir_factory.mktemp("test_dirs"))))

    make_pair(path.join(dir_base, "b1"), "dest1")
    make_pair(path.join(dir_base, "b2"), "dest2")
    make_pair(path.join(dir_base, "b3"), "dest3", bad=True)

    d1 = path.join(dir_base, "d1")
    os.mkdir(d1)
    make_pair(path.join(d1, "f1"), "dest1")
    make_pair(path.join(d1, "f2"), "dest2")
    make_pair(path.join(d1, "f3"), "dest1", bad=True)

    d2 = path.join(dir_base, "d2")
    os.mkdir(d2)
    make_pair(path.join(d2, "f4"), "dest3")
    make_pair(path.join(d2, "f5"), "dest2", bad=True)

    validity_map = {
        "valid": {
            'b1': (path.join(dir_base, 'b1'), 'dest1'),
            'b2': (path.join(dir_base, 'b2'), 'dest2'),
            'f1': (path.join(d1, "f1"), "dest1"),
            'f2': (path.join(d1, "f2"), "dest2"),
            'f4': (path.join(d1, "f4"), "dest3")
        },
        "invalid": {
            'b3': (path.join(dir_base, 'b3'), 'dest3'),
            'f3': (path.join(d1, "f3"), "dest1"),
            'f5': (path.join(d1, "f5"), "dest2")
        }
    }

    file_list = [
        path.join(dir_base, 'b1.txt'),
        path.join(dir_base, 'b1.jpg'),
        path.join(dir_base, 'b2.txt'),
        path.join(dir_base, 'b2.jpg'),
        path.join(dir_base, 'b3.jpg'),  # .txt missing because bad
        path.join(d1, 'f1.txt'),
        path.join(d1, 'f1.jpg'),
        path.join(d1, 'f2.txt'),
        path.join(d1, 'f2.jpg'),
        path.join(d1, 'f3.jpg'),  # .txt missing because bad
        path.join(d2, 'f4.txt'),
        path.join(d2, 'f4.jpg'),
        path.join(d2, 'f5.jpg')  # .txt missing because bad
    ]

    yield dir_base, validity_map, file_list

    if path.isdir(dir_base):
        shutil.rmtree(dir_base)
    for dir_name in tmpdir_maker.values():
        if path.isdir(dir_name):
            shutil.rmtree(dir_name)


def test_do(test_info, tmpdir_factory):
    dir_base, validity_map, expected_file_list = test_info

    do(dir_base)

    for base_name, (old_path, keyword) in validity_map['valid'].items():
        assert path.isdir(path.join(dir_base, keyword))
        assert path.isfile(path.join(dir_base, keyword, base_name) + ".jpg")
        # assert not path.isfile(path.join(dir_base, keyword, base_name) + ".txt")

    for base_name, (old_path, keyword) in validity_map['invalid'].items():
        assert path.isdir(path.join(dir_base, 'unknown'))
        assert path.isfile(path.join(dir_base, 'unknown', base_name) + ".jpg")


def test_do2(test_info, tmpdir_factory):
    dir_base, validity_map, expected_file_list = test_info

    do2(dir_base)

    for base_name, (old_path, keyword) in validity_map['valid'].items():
        assert path.isdir(path.join(dir_base, keyword))
        assert path.isfile(path.join(dir_base, keyword, base_name) + ".jpg")
        # assert not path.isfile(path.join(dir_base, keyword, base_name) + ".txt")

    for base_name, (old_path, keyword) in validity_map['invalid'].items():
        assert path.isdir(path.join(dir_base, 'unknown'))
        assert path.isfile(path.join(dir_base, 'unknown', base_name) + ".jpg")


def test_read_keyword(test_fn):
    assert "dest1" == read_keyword(test_fn)

    with NamedTemporaryFile(delete=False) as fp:
        fn = fp.name
    keyword = read_keyword(fn)
    os.remove(fn)
    assert keyword is None


def test_validate_file_pairs(test_info):
    test_directory, validity_map, expected_file_list = test_info
    valid, invalid = validate_file_pairs(test_directory)

    def get_base_fn(fn):
        return path.splitext(path.basename(fn))[0]

    valid = list(map(get_base_fn, valid))
    invalid = list(map(get_base_fn, invalid))

    for item_valid in validity_map['valid'].keys():
        assert item_valid in valid
        assert item_valid not in invalid

    for item_invalid in validity_map['invalid'].keys():
        assert item_invalid in invalid
        assert item_invalid not in valid


@pytest.mark.parametrize("in_fn,expected", [
    ("/path/To/a.txt", "/path/To/a.txt"),
    ("/path/To/a.TXT", "/path/To/a.txt"),
])
def test_lower_extension(in_fn, expected):
    assert expected == lower_extension(in_fn)


@pytest.fixture(scope='function')
def extension_test_dir(tmpdir_factory):
    dir_base = str(tmpdir_factory.mktemp("test_extensions"))

    def touch(fn):
        with open(fn, 'w') as fp:
            fp.write('hello\n')

    before = [
        path.join(dir_base, "a.txt"),
        path.join(dir_base, "a.jpg"),
        path.join(dir_base, "a.TXT"),
        path.join(dir_base, "a.JPG"),
        path.join(dir_base, "a.MP3")
    ]

    after = [
        path.join(dir_base, "a.txt"),
        path.join(dir_base, "a.jpg"),
        path.join(dir_base, "a.txt"),
        path.join(dir_base, "a.jpg"),
        path.join(dir_base, "a.mp3")
    ]

    # create all the files
    map(touch, before)

    yield dir_base, before, after

    # clean up
    if path.isdir(dir_base):
        shutil.rmtree(dir_base)


def test_lower_extensions(extension_test_dir):
    dir_name, before, after = extension_test_dir
    lower_extensions(dir_name)
    assert all(map(os.path.isfile, after))


def test_make_file_list(test_info):
    dir_base, _, expected_file_list = test_info

    actual_file_list = make_file_list(dir_base)
    for a, b in zip(sorted(expected_file_list), sorted(actual_file_list)):
        assert a == b
    assert len(set(expected_file_list) & set(actual_file_list)) == len(expected_file_list)


def test_parse_file_pairs():
    file_list = [
        "/path/to/a.txt",
        "/path/to/a.jpg",
        "path/to/a.txt",
        "path/to/a.jpg",
        "/path/to/b.txt",
        "/path/to/b.jpg",
        "/path/to/b.mp3"
    ]

    expected_pairs = {
        "/path/to/a": {".jpg": True, ".txt": True},
        "path/to/a": {".jpg": True, ".txt": True},
        "/path/to/b": {".jpg": True, ".txt": True, ".mp3": True}
    }

    assert expected_pairs == parse_file_pairs(file_list)


@pytest.mark.parametrize("fn_input,expected", [
    ("/path/to/file.txt", ("/path/to", "file", ".txt")),
    ("file.txt", ("", "file", ".txt")),
])
def test_file_parts(fn_input, expected):
    base_dir, base_fn, ext = file_parts(fn_input)
    exp_base_dir, exp_base_fn, exp_ext = expected
    assert base_dir == exp_base_dir
    assert base_fn == exp_base_fn
    assert ext == exp_ext


def test_previous_fail_case_do(fail_case_file_list):
