import random as r
import numpy as np
import ga.ga_methods.non_rand.mutation_non_rand as mnr


def bit_flip(c: int):
   return mnr.bit_flip(c, r.randrange(c.size))


def uniform(c: int):
    n = c.size
    return np.random.randint(low=0, high=2, size=n)

def flip_all(c):
    return mnr.flip_all(c)
