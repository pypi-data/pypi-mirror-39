from datahelper.private.create import create


def test_create_int_path_create_list():
    assert create(1) == []


def test_create_str_path_create_dict():
    assert create('test_path') == {}


def test_create_int_like_path_create_dict():
    assert create('1') == []
