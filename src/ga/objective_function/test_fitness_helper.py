import ga.objective_function.fitness_helper as fh


def test_if_simultaneous():
    has_simultaneous = fh.if_simultaneous(0b10011001, 4, 1, 1)
    no_simultaneous = not fh.if_simultaneous(0b11110000, 4, 1, 1)
    assert has_simultaneous and no_simultaneous


def test_split_chromosome_per_game():
    c = 0b1111000101111000101010111000
    cats_per_game = {'A': 3, 'B': 2, 'C': 4}
    slots = 3
    result = {
        'A': [0b111, 0b000, 0b101],
        'B': [0b111, 0b000],
        'C': [0b101, 0b010, 0b111, 0b000]
    }
    assert fh.split_chromosome_per_game(c, cats_per_game,
                                     slots) == result

def test_enough_consec_slots():
    c = 0b111011100111111
    assert fh.enough_consec_slots(c, 3) and not \
        fh.enough_consec_slots(c, 2)


def test_enough_rounds():
    c = 0b111011100111111
    assert fh.enough_rounds(c, 3) and not fh.enough_rounds(c, 5)
