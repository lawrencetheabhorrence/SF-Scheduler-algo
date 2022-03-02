import time
import os
import sys
from ga.GeneticAlgo import GeneticAlgo
from ga.data.reader import read_game_data, read_sf_data
from ga.data.output import bits_to_sched
import datetime

root = os.path.dirname(os.path.abspath(__file__))
big_folder = '/data/model'
tiny_folder = '/ga/data/test'

# test parameters
ga_params = {
    'selection_method': 'rank',
    'crossover_method': 'uniform',
    'mutation_method': 'bit_flip',
    'threshold': 650,
    'pop_size': 50,
    'mutation_rate': 0.1,
    'game_src': root + big_folder + '/big_game_data_og.csv',
    'sf_src': root + big_folder + '/big_sf_data_og.csv',
    'fitness_src': root + big_folder + '/big_fitness.csv',
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
    best = ga_obj.ga()
    print(best)
    t_end = time.perf_counter()
    print(f"Time in seconds: {t_end-t_start:0.4f}")
    with open(f"{datetime.datetime.today().strftime('%Y-%m-%d-%H:%M:%S')}.txt", "w") as f:
        f.write(f"Time in seconds: {t_end-t_start:0.4f}")
    sf_data = read_sf_data(ga_params['sf_src'])
    # sf_data = read_sf_data(ga_params['sf_src'])
    # game_data = read_game_data(ga_params['game_src'])
    # df = bits_to_sched(best, sf_data, game_data)
    # for i, day in enumerate(df):
    #     day.to_html(root + big_folder + 'result' + str(i) + '.html', escape=False)
    #     day.to_csv(root + big_folder + 'result' + str(i) + '.csv')
    #     global days
    #     days = i + 1
    # print(df)
    # print(days)

__main__()
