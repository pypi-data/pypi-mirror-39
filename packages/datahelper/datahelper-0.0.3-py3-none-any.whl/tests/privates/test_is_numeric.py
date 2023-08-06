from datahelper.private.is_numeric import is_numeric


def test_is_numeric():
    assert is_numeric(1) is True
    assert is_numeric('TEST') is False
