import random as r
import pandas as pd
from functools import partial
from collections import Counter
from ga.data.reader import read_game_data, read_sf_data
from ga.objective_function.fitness import fitness
from ga.ga_methods.population_initialization import init_pop
import ga.ga_methods.selection as sel
import ga.ga_methods.mutation as mut
import ga.ga_methods.crossover as cro


def ch_selection(selection_method):
    return {
        'rank': partial(sel.rank)
    }[selection_method]


def ch_mutation(mutation_method, length=None):
    return {
        'bit_flip': partial(mut.bit_flip),
        'flip_all': partial(mut.flip_all),
        'uniform': partial(mut.uniform)
    }[mutation_method]


def ch_crossover(crossover_method, crossover_params):
    n_breaks = (None if crossover_params is None
                else crossover_params.get('n_breaks'))
    children = (None if crossover_params is None
                else crossover_params.get('children'))
    return {
        'one_point': partial(cro.one_point),
        'n_point': partial(cro.n_point,
                           n_breaks=n_breaks),
        'uniform': partial(cro.uniform, children=children)
    }[crossover_method]

def write_fitness_data(avgs,path):
    constraint_scores = [f[0] for f in avgs]
    overall_scores = [f[1] for f in avgs]
    c_df = pd.DataFrame(constraint_scores)
    s_df = pd.Series(data=overall_scores, dtype=float, name="Average Fitness")
    pd.concat((c_df,s_df), axis=1).to_csv(path,index=True)


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
        slots = self.sf_data['slots']
        games = len(self.game_data['cats'])
        cats = sum(self.game_data['cats'].values())
        length = slots * games * cats + 1
        self.mutation = ch_mutation(mutation_method,
                                    length)

    def init_pop(self):
        self.population = init_pop(self.pop_size,
                                   self.game_data,
                                   self.sf_data)

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
        fitness_vals = [fitness(x, self.game_data, self.sf_data) for x in self.population]
        avg_overall = sum([f[1] for f in fitness_vals])/len(self.population)
        constraint_scores = [f[0] for f in fitness_vals]
        c = Counter()
        for d in constraint_scores:
            c.update(d)
        avg_constraints = {k: v/len(self.population) for k,v in dict(c).items()}
        return (avg_constraints, avg_overall)

    def genetic_algo_threshold_prop(self):
        self.init_pop()
        avg_fs = [self.avg_fitness()]
        while True:
            self.genetic_algo_cycle()
            avg_fs.append(self.avg_fitness())
            if abs(avg_fs[-1][1] - avg_fs[-2][1]) < self.threshold:
                write_fitness_data(avg_fs,self.fitness_src)
                return max(self.population,
                           key=(lambda x: fitness(x,
                                                  self.game_data,
                                                  self.sf_data)[1]))

    def genetic_algo_fixed_generation(self):
        self.init_pop()
        avg_fs = [self.avg_fitness()]
        for i in range(self.threshold):
            self.genetic_algo_cycle()
            avgf = self.avg_fitness()
            print(f"Generation {i}/{self.threshold}, Avg Fitness: {avgf[1]}, Avg Per Constraint: {avgf[0]}")
            avg_fs.append(avgf)
            write_fitness_data(avg_fs,self.fitness_src)

        return max(self.population,
                   key=(lambda x: fitness(x,
                                          self.game_data,
                                          self.sf_data)[1]))

    def ga(self):
        if 0 <= self.threshold <= 1:
            return self.genetic_algo_threshold_prop()
        if self.threshold >= 1:
            return self.genetic_algo_fixed_generation()
        raise ValueError("Threshold must be nonnegative!")
