import math
import random as r
from typing import List
import ga.ga_methods.non_rand.crossover_non_rand as cnr
from ga.helper.bit_helper import bitlength
__all__ = ["one_point"]


def one_point(c1: int, c2: int):
    """ one point crossover of 2 bit strings (randomized) """
    n = bitlength(c1)
    k = r.randrange(n)
    return cnr.one_point(c1, c2, k=k)


def n_point(c1: int, c2: int, n_breaks=3):
    """ n point crossover of 2 bitstrings (randomized)
    a list of breakpoints is generated then the children
    will be generated with the 'splits' from each parent
    alternating in the child """
    n = bitlength(c1)

    # generate the breakpoints
    # breakpoints must be in ascending order
    # the breakpoints should start with 0 and
    # end with n but this is also adjusted in the
    # non random function too.
    ks = [0,n] + r.sample(range(1,9), k=n_breaks-1)

    return cnr.n_point(c1, c2, ks)


def uniform(c1: int, c2: int, children=2):
    """ uniform crossover, the
    method is already inherently
    randomized. """
    return cnr.uniform(c1, c2, children)
