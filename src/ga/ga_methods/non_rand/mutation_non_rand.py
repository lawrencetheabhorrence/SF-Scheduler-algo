import random as r
from ga.helper.bit_helper import is_set, bitlength
__all__ = ['bit_flip', 'flip_all']


def bit_flip(c: int, k: int):
    """ flip bit at position k """
    return c - 2**k if is_set(k, c) > 0 else c + 2**k


def flip_all(c: int, length=None):
    """ flip all bits (unsigned 64bit int)"""
    n = bitlength(c)
    return abs(2 ** (n-1) | ~c)
