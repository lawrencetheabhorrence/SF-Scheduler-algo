import random as r
import numpy as np
from typing import List
from .bit_helper import is_set
from .objective_function import fitness
from .population_initialization import init_pop


def crossover(c1: int, c2: int, k: int):
    """ one point crossover of 2 bit strings """
    n = c1.bit_length()
    c1 = bin(c1)[2:]
    c2 = bin(c2)[2:]
    return int(c1[0:k+1] + c2[k+1:n], 2)


def crossover_rand(c1: int, c2: int):
    """ one point crossover of 2 bit strings (randomized) """
    n = c1.bit_length()
    k = r.randrange(n)
    return crossover(c1, c2, k)


def mutation(c: int, k: int):
    """ bit flip mutation """
    return c - 2**k if is_set(k, c) > 0 else c + 2**k


def mutation_rand(c: int):
    """ bit flip mutation (randomized) """
    return mutation(c, r.randrange(c.bit_length()))


def rank_selection(pop: List[int], proportion: float):
    """ choose breeding population by ranking fitness """
    pop = pop.sort(key=fitness)
    if not 0 <= proportion <= 1:
        raise ValueError("Please give a number between \
                         0 and 1")
    breeding_pop_size = int(len(pop) * proportion)
    return np.random.choice(pop, p=range(50, 1, -1), size=(breeding_pop_size),
                            replace=False)


def genetic_algo_cycle(proportion: int, pop: List[int], mutation_prop: int):
    breeding_pop = rank_selection(pop, proportion).shuffle()
    children = [breeding_pop[i:i+2] for i in range(0, len(breeding_pop), 2)]
    final_pop = breeding_pop.append(children).shuffle()
    m_size = int(mutation_prop*len(final_pop))
    return list(map(mutation_rand,
                    final_pop[0:m_size])).append(final_pop[m_size:])


def genetic_algo(pop_size: int, threshold: int, proportion: int):
    population = population_initialization(pop_size)
    past_fit = sum(map(fitness, population))/len(population)
    while True:
        population = genetic_algo_cycle(proportion, population_initialization)
        fit = sum(map(fitness, population))/len(population))
        if (abs(fit - past_fit) < threshold):
            return max(population, key=fitness)
