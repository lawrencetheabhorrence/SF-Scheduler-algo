from .algo.ga import genetic_algo


def __main__():
    pop_size = 50
    threshold = 0.05
    mutation_prop = 0.1
    game_src = "algo/test/data/test_game_data.csv"
    sf_src = "algo/test/data/test_sf_data.csv"
    genetic_algo(pop_size, threshold, mutation_prop, game_src, sf_src)


__main__()
