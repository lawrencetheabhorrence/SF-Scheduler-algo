from . bit_helper import locate_bit
from . bit_helper import is_set


def test_is_set():
    assert is_set(3, 111001)
