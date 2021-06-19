import random
from ga.ga_methods.population_initialization import \
        generate_chromosome, init_pop
from ga.data.reader import read_game_data, read_sf_data


def test_generate_chromosome():
    c = generate_chromosome(50)
    assert c.bit_length() == 51


def test_random_chromosome_lengths():
    cs = [random.randint(30, 300) for _ in range(50)]
    for x in cs:
        c = generate_chromosome(x)
        assert c.bit_length() == x + 1


def test_init_pop():
    root = "~/GitHub/SF-Scheduler-algo/src/ga/data/test/"
    game_data = \
        read_game_data(root + "test_game_data.csv")
    sf_data = \
        read_sf_data(root + "test_sf_data.csv")
    p = init_pop(50, game_data, sf_data)
    assert len(p) == 50 and int(p[0]).bit_length() == (3 * 2 * 5) + 1
