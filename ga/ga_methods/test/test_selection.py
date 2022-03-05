import numpy as np
from ga.ga_methods.population_initialization import init_pop
from ga.data.reader import read_sf_data, read_game_data
import ga.ga_methods.selection as sel

def test_rank():
    root = "~/GitHub/SF-Scheduler-algo/ga/data/test/"
    game_data = \
        read_game_data(root + "test_game_data.csv")
    sf_data = \
        read_sf_data(root + "test_sf_data.csv")
    pop = init_pop(10, game_data, sf_data)
    assert sel.rank(pop, game_data, sf_data).tolist() in map(lambda x:
                                                             x.tolist(), pop)
