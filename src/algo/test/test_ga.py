from .. ga import crossover, mutation


def test_crossover():
    c1 = 0b11111
    c2 = 0b10101
    assert crossover(c1, c2, 2) == 0b11101


def test_mutation():
    c = 0b11101101
    assert mutation(c, 1) == 0b11101111
    assert mutation(c, 2) == 0b11101001
