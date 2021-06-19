import pandas as pd
import random as r
from functools import partial
from ga.data.reader import read_game_data, read_sf_data
from ga.objective_function.fitness import fitness
import ga.ga_methods.selection as sel
import ga.ga_methods.mutation as mut
import ga.ga_methods.crossover as cro


def ch_selection(selection_method):
    return {
        'rank': partial(sel.rank)
    }[selection_method]


def ch_mutation(mutation_method):
    return {
        'bit_flip': partial(mut.bit_flip),
        'flip_all': partial(mut.flip_all),
        'uniform': partial(mut.uniform)
    }[mutation_method]


def ch_crossover(crossover_method, crossover_params):
    n_breaks = (None if crossover_params is None
                else crossover_params.get('n_breaks'))
    return {
        'one_point': partial(cro.one_point),
        'n_point': partial(cro.n_point,
                           n_breaks=n_breaks),
        'uniform': partial(cro.uniform)
    }[crossover_method]


def generate_chromosome(slots):
    return r.getrandbits(slots - 1) + (2 ** slots)


class GeneticAlgo:

    def __init__(self, selection_method,
                 crossover_method, mutation_method,
                 threshold, pop_size, mutation_rate,
                 fitness_src, crossover_params,
                 **kwargs):
        self.threshold = threshold
        self.game_data = (read_game_data(kwargs['game_src'])
                          if 'game_data' not in kwargs
                          else kwargs['game_data'])
        self.sf_data = (read_sf_data(kwargs['sf_src'])
                        if 'sf_data' not in kwargs
                        else kwargs['sf_data'])
        self.pop_size = pop_size
        self.mutation_rate = mutation_rate
        self.fitness_src = fitness_src
        self.selection = ch_selection(selection_method)
        self.crossover_params = crossover_params
        self.crossover = ch_crossover(crossover_method,
                                      crossover_params)
        self.mutation = ch_mutation(mutation_method)

    def init_pop(self):
        print(self.sf_data)
        slots = self.sf_data['slots']
        games = len(self.game_data['cats'])
        cats = sum(self.game_data['cats'].values())
        print(slots, games, cats)
        self.population = [generate_chromosome(slots * games * cats)
                           for _ in range(self.pop_size)]

    def genetic_algo_cycle(self):
        children = []
        while len(children) < len(self.population):
            parent1 = self.selection(self.population,
                                     self.game_data, self.sf_data)
            parent2 = self.selection(self.population,
                                     self.game_data, self.sf_data)
            children.extend(self.crossover(parent1, parent2))

        r.shuffle(children)
        m_size = int(self.mutation_rate * len(children))
        self.population = list(map(self.mutation, children[0:m_size])) + children[m_size:]

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

    def ga(self):
        if 0 <= self.threshold <= 1:
            return self.genetic_algo_threshold_prop()
        if self.threshold >= 1:
            return self.genetic_algo_fixed_generation()
        raise ValueError("Threshold must be nonnegative!")
