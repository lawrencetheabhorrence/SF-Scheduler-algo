from ga.GeneticAlgo import GeneticAlgo


root = '~/GitHub/SF-Scheduler-algo/src/ga'


# test parameters
ga_params = {
    'selection_method': 'rank',
    'crossover_method': 'one_point',
    'mutation_method': 'flip_all',
    'threshold': 0.01,
    'pop_size': 10,
    'mutation_rate': 0.1,
    'game_src': root + '/data/test/test_game_data.csv',
    'sf_src': root + '/data/test/test_sf_data.csv',
    'fitness_src': root + '/data/test/test_fitness.csv',
    'crossover_params': None
}


ga_obj = GeneticAlgo(**ga_params)


def test_ga_cycle():
    ga_obj.init_pop()
    ga_obj.genetic_algo_cycle()
    assert len(ga_obj.population) == 10


def test_ga():
    ga_obj.init_pop()
    assert isinstance(ga_obj.ga(), int)
