from math import ceil, log2
from .. ga import crossover, mutation, genetic_algo, genetic_algo_cycle,\
        rank_selection
from .. population_initialization import init_pop


def test_crossover():
    c1 = 0b11111
    c2 = 0b10101
    assert crossover(c1, c2, 2)[0] == 0b11101 and crossover(c1, c2, 2)[1] == 0b10111


def test_mutation():
    c = 0b11101101
    assert mutation(c, 1) == 0b11101111
    assert mutation(c, 2) == 0b11101001


def generate_test_pop():
    return init_pop(10, "test/data/test_game_data.csv",
                    "test/data/test_sf_data.csv")


def test_rank_selection():
    pop = generate_test_pop()
    assert rank_selection(pop,
                          "test/data/test_game_data.csv",
                          "test/data/test_sf_data.csv") in pop


def test_ga_cycle():
    result = genetic_algo_cycle(0.5, generate_test_pop(),
                                "test/data/test_game_data.csv",
                                "test/data/test_sf_data.csv")
    assert len(result) == 10

def test_ga():
    assert isinstance(genetic_algo(5, 5, 0.1,
                                   "test/data/test_game_data.csv",
                                   "test/data/test_sf_data.csv",
                                   "test/data/test_fitness.csv"), int)
