from .. objective_function import hc4, hc3


def test_hc3():
    c = 0b1111000101111000101010111000
    cats_per_game = {'A': 3, 'B': 2, 'C': 4}
    slots = 3
    min_slots_per_game = {'A': 3, 'B': 3, 'C': 3}
    assert not hc3(c, min_slots_per_game, cats_per_game, slots)


def test_hc4():
    priority_per_game = {'A': 'Major', 'B': 'Junior', 'C': 'Minor'}
    cats_per_game = {'A': 3, 'B': 2, 'C': 3}
    slots = 3
    c = 0b1111010001001001110001010
    assert hc4(c, cats_per_game, priority_per_game, slots) == 1
