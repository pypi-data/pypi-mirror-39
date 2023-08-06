import pytest

from lhub_integ.params import DataType


def test_numeric_coercion():
    assert DataType.INT.coerce("123") == 123
    assert DataType.INT.coerce("123.5") == 123
    assert DataType.NUMBER.coerce("123.5") == 123.5


def test_bool_coercion():
    assert DataType.BOOL.coerce("false") is False
    assert DataType.BOOL.coerce("true") is True

    with pytest.raises(ValueError):
        DataType.BOOL.coerce("cat")

    assert DataType.BOOL.coerce(True) is True
    assert DataType.BOOL.coerce(False) is False

    assert DataType.BOOL.coerce("True") is True
    assert DataType.BOOL.coerce("False") is False


def test_json_coercion():
    assert DataType.JSON.coerce("[1,2,3]") == [1, 2, 3]

    with pytest.raises(ValueError):
        DataType.JSON.coerce("1,2,3")
