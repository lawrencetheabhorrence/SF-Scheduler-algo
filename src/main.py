import time
from ga.GeneticAlgo import GeneticAlgo
from ga.data.reader import read_game_data, read_sf_data

def __main__():
    pop_size = 50
    threshold = 0.05
    mutation_prop = 0.1
    root = "~/GitHub/SF-Scheduler-algo/src_alt/data/model/"
    game_data = read_game_data(root + "big_game_data.csv")
    sf_data = read_sf_data(root + "big_sf_data.csv")
    fitness_src = root + "big_fitness.csv"
    crossover_method = "n_point"
    selection_method = "rank"
