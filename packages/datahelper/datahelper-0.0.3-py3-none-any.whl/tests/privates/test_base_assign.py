from datahelper.private.base_assign import base_assign


def test_base_assign():
    dummy = {'a': 1}
    result = base_assign(dummy, 'a', 3)
    assert result == {'a': 3}


def test_base_assign_scalar_to_dict():
    dummy = {'a': 1}
    result = base_assign(dummy, 'a.b', 3)
    assert result == {'a': {'b': 3}}


def test_base_assign_scalar_to_list():
    dummy = {'a': 1}
    result = base_assign(dummy, 'a.0', 3)
    assert result == {'a': [3]}


def test_base_assign_nested_dict():
    dummy = {'a': 1, 'b': {'c': 3}}
    result = base_assign(dummy, 'a.b.c', {'d': 1})
    assert result == {'a': {'b': {'c': {'d': 1}}}, 'b': {'c': 3}}


def test_base_assign_nested_dict_detail():
    dummy = {'a': 1, 'b': {'c': 3}}
    result = base_assign(dummy, 'b.c', {'d': 1})
    assert result == {'a': 1, 'b': {'c': {'d': 1}}}


def test_base_assign_nested_dict_and_list():
    dummy = {'a': 1}
    result = base_assign(dummy, 'b.0.c', {'d': 1})
    assert result == {'a': 1, 'b': [{'c': {'d': 1}}]}


def test_base_assign_nested_dict_and_list_detail():
    dummy = {'a': 1}
    result = base_assign(dummy, 'b.0.c.4', {'d': 1})
    assert result == {'a': 1, 'b': [{'c': [{'d': 1}]}]}
