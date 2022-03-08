import numpy as np
from ga.ga_methods.population_initialization import \
        generate_chromosome, init_pop
from ga.data.reader import read_game_data, read_sf_data


def test_generate_chromosome():
    c = generate_chromosome(50)
    assert c.size == 50


def test_random_chromosome_lengths():
    cs = np.random.randint(low=0, high=2, size=50)
    for x in cs:
        c = generate_chromosome(x)
        assert c.size == x


def test_init_pop():
    root = "~/GitHub/SF-Scheduler-algo/ga/data/test/"
    sf_data = \
        read_sf_data(root + "test_sf_data.csv")
    game_data = \
        read_game_data(root + "test_game_data.csv", sf_data['teams'])
    p = init_pop(50, game_data, sf_data)
    assert len(p) == 50 and p[0].size == (5 * 1 * 5)
