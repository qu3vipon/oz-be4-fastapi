import pytest

def divide(a, b):
    return a / b


def test_divide():
    assert divide(1, 2) == 1 / 2
    assert divide(3, 7) == 3 / 7

    with pytest.raises(ZeroDivisionError):
        assert divide(3, 0)
