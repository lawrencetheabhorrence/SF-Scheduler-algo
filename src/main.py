import time
from ga.GeneticAlgo import GeneticAlgo
from ga.data.reader import read_game_data, read_sf_data

root = '~/GitHub/SF-Scheduler-algo/src/'
big_folder = 'data/model'
tiny_folder = 'ga/data/test'

# test parameters
ga_params = {
    'selection_method': 'rank',
    'crossover_method': 'one_point',
    'mutation_method': 'flip_all',
    'threshold': 100,
    'pop_size': 50,
    'mutation_rate': 0.1,
    'game_src': root + big_folder + '/big_game_data.csv',
    'sf_src': root + big_folder + '/big_sf_data.csv',
    'fitness_src': root + big_folder + 'big_fitness.csv',
    'crossover_params': {'children': 2, 'n_breaks': 5}
}

def all_cross_mut():
    for i in ['one_point', 'n_point', 'uniform']:
        ga_params['crossover_method'] = i
        for j in ['bit_flip', 'flip_all', 'uniform']:
            ga_params['mutation_method'] = j
            ga_params['fitness_src'] = (root + big_folder +
            '/cross_mut/fitness_' + i[0] + j[0] + '.csv')
            __main__()

def __main__():
    ga_obj = GeneticAlgo(**ga_params)

    t_start = time.perf_counter()
    print(ga_obj.ga())
    t_end = time.perf_counter()
    print(f"Time in seconds: {t_end-t_start:0.4f}")

all_cross_mut()
