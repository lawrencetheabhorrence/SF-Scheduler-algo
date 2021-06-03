import time
from algo.ga import genetic_algo


def __main__():
    pop_size = 50
    threshold = 0.05
    mutation_prop = 0.1
    game_src = "algo/test/data/test_game_data.csv"
    sf_src = "algo/test/data/test_sf_data.csv"
    t_start = time.perf_counter()
    print(genetic_algo(pop_size, threshold, mutation_prop, game_src, sf_src))
    t_end = time.perf_counter()
    print(f"Time in seconds: {t_end-t_start:0.4f}")


__main__()
