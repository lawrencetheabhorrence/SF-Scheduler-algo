import time
from ga.GeneticAlgo import GeneticAlgo
from ga.data.reader import read_game_data, read_sf_data


def __main__():
    root = '~/GitHub/SF-Scheduler-algo/src/'

    # test parameters
    ga_params = {
        'selection_method': 'rank',
        'crossover_method': 'one_point',
        'mutation_method': 'flip_all',
        'threshold': 0.01,
        'pop_size': 10,
        'mutation_rate': 0.1,
        'game_src': root + 'data/model/big_game_data.csv',
        'sf_src': root + 'data/model/big_sf_data.csv',
        'fitness_src': root + 'data/model/big_fitness.csv',
        'crossover_params': None
    }

    ga_obj = GeneticAlgo(**ga_params)

    t_start = time.perf_counter()
    print(ga_obj.ga())
    t_end = time.perf_counter()
    print(f"Time in seconds: {t_end-t_start:0.4f}")


__main__()
