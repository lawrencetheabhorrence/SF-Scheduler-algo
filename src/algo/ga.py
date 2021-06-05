import random as r
import numpy as np
import pandas as pd
import math
from typing import List
from .bit_helper import is_set
from .objective_function import fitness
from .population_initialization import init_pop


def crossover(c1: int, c2: int, k: int):
    """ one point crossover of 2 bit strings """
    n = math.ceil(math.log2(c1))
    c1 = bin(c1)[2:]
    c2 = bin(c2)[2:]
    return int(c1[0:k+1] + c2[k+1:n], 2)


def crossover_rand(c1: int, c2: int):
    """ one point crossover of 2 bit strings (randomized) """
    n = math.ceil(math.log2(c1))
    k = r.randrange(n)
    return crossover(c1, c2, k)


def mutation(c: int, k: int):
    """ bit flip mutation """
    return c - 2**k if is_set(k, c) > 0 else c + 2**k


def mutation_rand(c: int):
    """ bit flip mutation (randomized) """
    return mutation(c, r.randrange(c.bit_length()))


def rank_selection(pop: List[int],
                   game_src="data/game_data.csv",
                   sf_src="data/sf_data.csv"):
    """ choose breeding population by ranking fitness """
    pop.sort(key=(lambda x: fitness(x, game_src, sf_src)))
    return r.choices(pop,
                     weights=[i/sum(range(1, len(pop)+1))
                              for i in range(len(pop), 0, -1)],
                     k=len(pop)*2)


def genetic_algo_cycle(mutation_prop: float, pop: List[int],
                       game_src="data/game_data.csv",
                       sf_src="data/sf_data.csv"):
    """ generates a generation of individuals """
    breeding_pop = rank_selection(pop, game_src, sf_src)
    parents = (breeding_pop[i:i+2] for i in range(0, len(breeding_pop), 2))
    children = [crossover_rand(p[0], p[1]) for p in parents]
    r.shuffle(children)
    m_size = int(mutation_prop*len(children))
    return list(map(mutation_rand, children[0:m_size])) + \
        children[m_size:]

def genetic_algo(pop_size: int, threshold: int,
                 mutation_prop: float,
                 game_src="data/game_data.csv",
                 sf_src="data/sf_data.csv",
                 fitness_src="data/fitness.csv"):
    """ The genetic algorithm first generates
    an initial population and generates new solutions
    through the genetic_algo_cycle function.
    The algo eventually stops when the generations converge,
    (fitness doesnt change much) then returns the fittest
    individual from the latest generation """

    def avg_fitness(population):
        return sum(map(lambda x: fitness(x, game_src, sf_src),
                       population)) / len(population)

    population = init_pop(pop_size, game_src, sf_src)
    avg_fs=[avg_fitness(population)]
    while True:
        population = genetic_algo_cycle(mutation_prop, population,
                                        game_src, sf_src)
        avg_fs.append(avg_fitness(population))
        if abs(avg_fs[-1] - avg_fs[-2]) < threshold:
            pd.Series(data=avg_fs, dtype=float, name="Average\
                      Fitness").to_csv(fitness_src, index=False)
            return max(population, key=(lambda x: fitness(x, game_src,
                                                          sf_src)))
