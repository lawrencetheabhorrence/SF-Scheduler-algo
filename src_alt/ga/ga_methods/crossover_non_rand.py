import math
from ga.helper.bit_helper import bitlength
__all__ = ["one_point", "n_point", "uniform"]


def one_point(c1: int, c2: int, k: int):
    n = bitlength(c1)
    c1 = bin(c1)[2:]
    c2 = bin(c2)[2:]
    return (int(c1[0:k+1] + c2[k+1:n], 2), int(c2[0:k+1] + c1[k+1:n], 2))
