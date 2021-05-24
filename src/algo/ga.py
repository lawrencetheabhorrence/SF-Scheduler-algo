import random as r
from typing import List
from .bit_helper import is_set
from .objective_function import fitness


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
    return r.choices(pop, weights=range(50, 1, -1), k=breeding_pop_size)
