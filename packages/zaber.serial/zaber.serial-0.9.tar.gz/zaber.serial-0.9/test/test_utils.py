from zaber.serial.utils import isstring


def test_isstring_returns_true_for_string_and_unicode():
    assert isstring("a") is True
    assert isstring(b"a".decode()) is True


def test_isstring_returns_false_for_non_string():
    assert isstring(1) is False
    assert isstring(object()) is False
