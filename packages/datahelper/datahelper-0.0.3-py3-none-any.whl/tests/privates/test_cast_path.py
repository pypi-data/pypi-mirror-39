from datahelper.private.cast_path import cast_path


def test_cast_path_int_like_string_to_int():
    assert cast_path('1') == 1


def test_cast_path_string_to_string():
    assert cast_path('HelloWorld') == 'HelloWorld'
