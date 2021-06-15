import pandas as pd
import random as r
from functools import partial
from ga.data.read_data import read_game_data, read_sf_data
from ga.objective_function.fitness import fitness
import ga.ga_methods.selection as sel
import ga.ga_methods.mutation as mut
import ga.ga_methods.crossover as cro


def ch_selection(selection_method, pop, game_src, sf_src):
    return {
        'rank': sel.rank(pop, game_src, sf_src)
    }[selection_method]


def ch_mutation(mutation_method):
    return {
        'bit_flip': partial(mut.bit_flip),
        'flip_all': partial(mut.flip_all),
        'non_uniform': partial(mut.non_uniform),
        'uniform': partial(mut.uniform)
    }[mutation_method]


def ch_crossover(crossover_method):
    return {
        'one_point': partial(cro.one_point),
        'n_point': partial(cro.n_point),
        'uniform': partial(cro.uniform)
    }[crossover_method]


def generate_chromosome(slots):
    return r.getrandbits(slots - 1) + (2 ** slots)


class GeneticAlgo:

    def __init__(self, selection_method,
                 crossover_method, mutation_method,
                 threshold, pop_size, mutation_rate,
                 fitness_src,
                 **kwargs):
        self.selection = ch_selection(selection_method)
        self.crossover = ch_crossover(crossover_method)
        self.mutation = ch_mutation(mutation_method)
        self.threshold = threshold
        self.game_data = (kwargs["game_data"] if not kwargs["game_data"] is
                          None else read_game_data(kwargs["game_src"]))
        self.sf_data = (kwargs["sf_data"] if not kwargs["sf_data"] is None else
                        read_sf_data(kwargs["sf_src"]))
        self.pop_size = pop_size
        self.mutation_rate = mutation_rate
        self.fitness_src = fitness_src

    def init_pop(self):
        slots = self.sf_data[0]
        games = len(self.game_data['cats'])
        cats = sum(self.game_data['cats'].values())
        self.population = [generate_chromosome(slots * games * cats)
                           for _ in range(self.pop_size)]

    def genetic_algo_cycle(self):
        children = []
        while len(children) < len(self.population):
            parent1 = self.selection()
            parent2 = self.selection()
            children.extend(self.crossover(parent1, parent2))
        r.shuffle(children)
        m_size = int(self.mutation_rate * len(children))
        self.population = list(map(self.mutation, children[0:m_size]) +
                    children[m_size:])

    def avg_fitness(self):
        return sum(map(lambda x: fitness(x, self.game_data, self.sf_data),
                       self.population)) / len(self.population)

    def genetic_algo_threshold_prop(self):
        self.init_pop()
        avg_fs = [self.avg_fitness()]
        while True:
            self.genetic_algo_cycle()
            avg_fs.append(self.avg_fitness())
            if abs(avg_fs[-1] - avg_fs[-2]) < self.threshold:
                pd.Series(data=avg_fs, dtype=float,
                          name="Average Fitness")\
                        .to_csv(self.fitness_src, index=True)
                return max(self.population,
                           key=(lambda x: fitness(x,
                                                  self.game_data,
                                                  self.sf_data)))

    def genetic_algo_fixed_generation(self):
        self.init_pop()
        avg_fs = [self.avg_fitness()]
        for _ in range(self.threshold):
            self.genetic_algo_cycle()
            avg_fs.append(self.avg_fitness())
        pd.Series(data=avg_fs, dtype=float,
                  name="Average Fitness")\
            .to_csv(self.fitness_src, index=True)
        return max(self.population,
                   key=(lambda x: fitness(x,
                                          self.game_data,
                                          self.sf_data)))
