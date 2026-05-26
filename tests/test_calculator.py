
from tmp.calculator import add, subtract

def test_add():
    assert add(5,5) == 10


def test_subtract():
    assert subtract(10, 9) == 1
    