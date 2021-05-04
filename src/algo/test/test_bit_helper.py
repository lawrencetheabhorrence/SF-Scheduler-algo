from .. bit_helper import locate_bit
from .. bit_helper import is_set


def test_is_set():
    assert is_set(3, 111001)


def test_locate_Bit():
    cats_per_game = {'A': 3, 'B': 3, 'C': 3}
    game = 'B'
    cat, slot, total_slots = 1, 2, 5
    assert locate_bit(cats_per_game, game, cat, slot, total_slots) == 17
