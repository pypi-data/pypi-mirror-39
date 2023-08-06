from datahelper.private.base_set import base_set


def test_base_set():
    dummy = {'a': 1}
    result = base_set(dummy, 'c', 10)
    assert result == {'a': 1, 'c': 10}


def test_base_set_empty():
    dummy = {}
    result = base_set(dummy, 'c', 10)
    assert result == {'c': 10}


def test_base_set_list():
    dummy = [1, 2, 3, 4]
    result = base_set(dummy, '4', 10)
    assert result == [1, 2, 3, 4, 10]


def test_base_set_empty_list():
    dummy = []
    result = base_set(dummy, '4', 10)
    assert result == [10]


def test_base_set_list_but_path_is_string():
    dummy = []
    result = base_set(dummy, 'a', 1)
    assert result == {'a': 1}


def test_base_set_dict_but_path_is_int():
    dummy = {}
    result = base_set(dummy, '1', 1)
    assert result == [1]
