import random as r
import math
from typing import List
from ga.helper.bit_helper import bitlength
__all__ = ["one_point", "n_point", "uniform"]


def get_bits_and_len(c1: int, c2: int):
    return (bitlength(c1), bin(c1)[2:], bin(c2)[2:])


def one_point(c1: int, c2: int, k=None):
    n, b1, b2 = get_bits_and_len(c1, c2)
    if k is None:
        k = n // 2
    return (int(b1[0:k+1] + b2[k+1:n], 2), int(b2[0:k+1] + b1[k+1:n], 2))


def split_ks(c1: str, ks: List[int]):
    """ split according to breakpoints """
    n = len(c1)
    if ks[0] != 0:
        ks = [0] + ks
    if ks[-1] != n:
        ks.append(n)

    return [c1[ks[i]:ks[i+1]] for i in range(len(ks)-1)]


def n_point(c1: int, c2: int, ks=None):
    n, b1, b2 = get_bits_and_len(c1, c2)

    if ks is None:
        return one_point(c1, c2, k=r.randrange(n))

    b1, b2 = split_ks(b1, ks), split_ks(b2, ks)
    n = len(b1)
    return (int(''.join((b1[i] if i % 2 == 0 else b2[i]
                         for i in range(n))), 2),
            int(''.join((b2[i] if i % 2 == 0 else b1[i]
                         for i in range(n))), 2))


def uniform(c1: int, c2: int, children=None):
    n, b1, b2 = get_bits_and_len(c1, c2)
    return [int(''.join((r.choice((b1[i], b2[i])) for i in range(n))), 2)
            for c in range(children)]
