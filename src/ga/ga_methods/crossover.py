import numpy as np
import random as r
from typing import List
import ga.ga_methods.non_rand.crossover_non_rand as cnr
__all__ = ["one_point"]


def one_point(c1, c2):
    """ one point crossover of 2 bit strings (randomized) """
    n = c1.size
    k = r.randrange(n)
    return cnr.one_point(c1, c2, k=k)


def n_point(c1, c2, n_breaks=3):
    """ n point crossover of 2 bitstrings (randomized)
    a list of breakpoints is generated then the children
    will be generated with the 'splits' from each parent
    alternating in the child """
    n = c1.size

    if n_breaks % 2 == 0:
        # there is very weird behavior with
        # even numbers of breakpoints
        # i have a hypothesis but i didnt
        # verify it so dont @ me lmao
        n_breaks = n_breaks - 1

    # generate the breakpoints
    # breakpoints must be in ascending order
    # the breakpoints should start with 0 and
    # end with n but this is also adjusted in the
    # non random function too.
    rng = np.random.default_rng()
    ks = rng.choice(np.arange(1, n),
                    size=n_breaks,
                    shuffle=False,
                    replace=False)
    ks.sort()

    return cnr.n_point(c1, c2, ks)


def uniform(c1, c2, children=2):
    """ uniform crossover, the
    method is already inherently
    randomized. """
    return cnr.uniform(c1, c2, children)
