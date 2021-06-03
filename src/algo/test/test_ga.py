from .. ga import crossover, mutation, genetic_algo, genetic_algo_cycle,\
        rank_selection


def test_crossover():
    c1 = 0b11111
    c2 = 0b10101
    assert crossover(c1, c2, 2) == 0b11101


def test_mutation():
    c = 0b11101101
    assert mutation(c, 1) == 0b11101111
    assert mutation(c, 2) == 0b11101001


def test_rank_selection():
    assert len(rank_selection([1, 3, 4, 5, 6],
                              "test/data/test_game_data.csv",
                              "test/data/test_sf_data.csv")) == 10


def test_ga_cycle():
    result = genetic_algo_cycle(0.5, [1, 5, 4, 5, 3],
                                "test/data/test_game_data.csv",
                                "test/data/test_sf_data.csv")
    assert len(result) == 5

def test_ga():
    assert isinstance(genetic_algo(5, 5, 0.1,
                                   "test/data/test_game_data.csv",
                                   "test/data/test_sf_data.csv"), int)
