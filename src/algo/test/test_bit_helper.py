from .. bit_helper import locate_bit
from .. bit_helper import is_set
from .. bit_helper import bit_slice
from .. bit_helper import all_set


def test_is_set():
    assert is_set(3, 111001)


def test_locate_Bit():
    cats_per_game = {'A': 3, 'B': 3, 'C': 3}
    game = 'B'
    cat, slot, total_slots = 1, 2, 5
    assert locate_bit(cats_per_game, game, cat, slot, total_slots) == 17


def test_bit_slice():
    bits = 0b11101101
    assert bit_slice(3, 5, bits) == 0b101


def all_set():
    assert all_set(0b1111)
