import numpy as np
import random as r
from typing import List
__all__ = ["one_point", "n_point", "uniform"]


def one_point(c1, c2, k=None):
    n = c1.size
    if k is None:
        k = n // 2
    return(np.concatenate((c1[:k], c2[k:])),
           np.concatenate((c2[:k], c1[k:])))


def n_point(c1, c2, ks=None):
    n = c1.size
    if ks is None:
        return one_point(c1, c2, k=r.randrange(n))

    b1, b2 = np.split(c1, ks), np.split(c2, ks)
    print(b1, b2)

    # this "trick" allows us to concatenate two
    # arrays while alternating the elements
    # b1[::2] takes every other element starting from
    # index 0, b1[1::2] is the same but from index 1
    # the ravel would store our 2d array formed
    # by stacking b1 and b2 vertically as a
    # 1d array.
    # 'F' stands for Fortran style ordering
    # or column major ordering
    # https://en.wikipedia.org/wiki/Row-_and_column-major_order
    merged_slices1 = np.hstack(
        np.ravel([b1[0::2], b2[1::2]], 'F'))
    merged_slices2 = np.hstack(
        np.ravel([b2[0::2], b1[1::2]], 'F'))
    print(merged_slices1, merged_slices2)

    return np.vstack((merged_slices1, merged_slices2))


def uniform(c1, c2, children=None):
    n = c1.size

    # This should gives us rows
    # where each row (index r) with
    # [c1[r], c2[r]]
    choices = np.vstack((c1, c2)).T

    offspring = []

    for x in range(children):
        # we randomly sample indices by
        # simply generating a random array and
        # getting the indices of each element
        # if the array were "sorted" by row
        # this is similar to actually shuffling the array row wise
        # this method is also much faster than using
        # np.random.choice
        # https://stackoverflow.com/questions/45437988/numpy-random-choice-to-produce-a-2d-array-with-all-unique-values/45438143#45438143
        idx = np.random.rand(*choices.shape).argsort(1)

        # we can now use these indices along each row
        # on our choices
        offspring.append(np.take_along_axis(choices, idx, axis=1)[:,0].T)

    return offspring
