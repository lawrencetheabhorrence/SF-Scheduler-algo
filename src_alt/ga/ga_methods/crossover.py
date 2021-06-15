import math
import random as r
import ga.ga_methods.crossover_non_rand as cnr
from ga.helper.bit_helper import bitlength
__all__ = ["one_point", "n_point", "uniform"]


def one_point(c1: int, c2: int):
    """ one point crossover of 2 bit strings (randomized) """
    n = bitlength(c1)
    k = r.randrange(n)
    return cnr.one_point(c1, c2, k)
