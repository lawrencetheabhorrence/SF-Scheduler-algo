import random
from ..population_initialization import generate_chromosome
from ..population_initialization import init_pop


def test_generate_chromosome():
    c = generate_chromosome(50)
    assert c.bit_length() == 51


def test_random_chromosome_lengths():
    cs = [random.randint(30, 300) for _ in range(50)]
    for x in cs:
        c = generate_chromosome(x)
        assert c.bit_length() == x + 1


def test_init_pop():
    p = init_pop(50, "test/data/test_game_data.csv",
                 "test/data/test_sf_data.csv")
    assert len(p) == 50 and int(p[0]).bit_length() == (3 * 2 * 5) + 1
