import numpy as np
import ga.objective_function.fitness_helper as fh


def test_if_simultaneous():
    c1 = np.array([1, 0, 0, 1, 1, 0, 0, 1])
    c2 = np.array([1, 1, 1, 1, 0, 0, 0, 0])
    has_simultaneous = fh.if_simultaneous(c1,  4,  1,  1)
    no_simultaneous = not fh.if_simultaneous(c2,  4,  1,  1)
    assert has_simultaneous and no_simultaneous


def test_split_chromosome_per_game():
    c = np.array([1, 1, 1, 1, 0, 0, 0, 1, 0, 1, 1, 1, 1, 0, 0, 0, 1, 0, 1, 0, 1, 0, 1, 1, 1, 0, 0, 0])
    cats_per_game = {'A': 3,  'B': 2,  'C': 2}
    slots = 4
    correct = {
        'A': [[1, 1, 1, 1], [0, 0, 0, 1], [0, 1, 1, 1]],
        'B': [[1, 0, 0, 0], [1, 0, 1, 0]],
        'C': [[1, 0, 1, 1], [1, 0, 0, 0]]
    }

    result = fh.split_chromosome_per_game(c,  cats_per_game,  slots)

    for g in cats_per_game:
        np.testing.assert_array_equal(correct[g],  result[g])


def test_enough_consec_slots():
    c = np.array([1, 1, 1, 0, 1, 1, 1, 0, 0, 1, 1, 1, 1, 1, 1])
    assert fh.enough_consec_slots(c,  3) == 0 and not \
        fh.enough_consec_slots(c,  2) == 0


def test_enough_rounds():
    c = np.array([1, 1, 0, 0, 1, 1, 1, 0, 1, 1, 0, 1, 0, 1, 1])
    assert fh.enough_rounds(c,  5, 2) == 0 and not fh.enough_rounds(c,  3, 2) == 0
