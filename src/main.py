import time
from algo.ga import genetic_algo, genetic_algo_fixed_gen


def __main__():
    pop_size = 50
    # threshold = 0.05
    generations = 100
    mutation_prop = 0.1
    game_src = "algo/test/data/big_game_data.csv"
    sf_src = "algo/test/data/big_sf_data.csv"
    fitness_src = "algo/test/data/big_fitness.csv"
    t_start = time.perf_counter()
    genetic_algo_fixed_gen(pop_size, mutation_prop, generations,
                           game_src, sf_src, fitness_src)
    t_end = time.perf_counter()
    print(f"Time in seconds: {t_end-t_start:0.4f}")


__main__()
