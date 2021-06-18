import random as r
from ga.helper.bit_helper import bitlength
import ga.ga_methods.non_rand.mutation_non_rand as mnr


def bit_flip(c: int):
   return mnr.bit_flip(c, r.randrange(bitlength(c)))


def uniform(c: int):
    n = bitlength(c) - 1
    return 2 ** n | int(r.uniform(0, 2 ** n))

def flip_all(c):
    return mnr.flip_all(c)
