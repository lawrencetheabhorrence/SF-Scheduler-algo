from .. objective_helper import if_simultaneous, \
        enough_consec_slots, split_chromosome


def test_if_simultaneous():
    has_simultaneous = if_simultaneous(0b10011001, 4, 1, 1)
    no_simultaneous = not if_simultaneous(0b11110000, 4, 1, 1)
    assert has_simultaneous and no_simultaneous

def test_split_chromosome():
    c = 0b1111000101111000101010111000
    cats_per_game = {'A': 3, 'B': 2, 'C': 4}
    slots = 3
    result = {
        'A': ['111', '000', '101'],
        'B': ['111', '000'],
        'C': ['101', '010', '111', '000']
    }
    assert split_chromosome(c, cats_per_game, slots) == result

def test_enough_consec_slots():
    c = '111011100111111'
    assert enough_consec_slots(c, 3) and not \
        enough_consec_slots(c, 2)
