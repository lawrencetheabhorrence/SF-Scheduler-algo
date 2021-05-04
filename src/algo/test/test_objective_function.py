from .. objective_function import if_simultaneous
from .. objective_function import hc4


def test_if_simultaneous():
    has_simultaneous = if_simultaneous(0b10011001, 4, 1, 1)
    no_simultaneous = not if_simultaneous(0b11110000, 4, 1, 1)
    assert has_simultaneous and no_simultaneous


def test_hc4():
    priority_per_game = {'A': 'Major', 'B': 'Junior', 'C': 'Minor'}
    cats_per_game = {'A': 3, 'B': 2, 'C': 3}
    slots = 3
    c = 0b1111010001001001110001010
    assert hc4(c, cats_per_game, priority_per_game, slots) == 1
