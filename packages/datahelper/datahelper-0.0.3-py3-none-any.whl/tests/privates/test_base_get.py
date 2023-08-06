from datahelper.private.base_get import base_get


def test_base_get():
    dummy = {'a': 1}
    assert base_get(dummy, 'a') == 1


def test_base_get_return_none_if_key_does_not_exist():
    dummy = {'a': 1}
    assert base_get(dummy, 'b') is None


def test_base_get_return_none_if_list_index_is_string():
    dummy = [1, 2, 3, 4]
    assert base_get(dummy, 'b') is None


def test_base_get_list_index():
    dummy = [1, 2, 3, 4]
    assert base_get(dummy, 3) == 4


def test_base_get_list_index_out_of_range():
    dummy = [1, 2, 3, 4]
    assert base_get(dummy, 4) is None
