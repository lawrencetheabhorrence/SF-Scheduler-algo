import numpy as np
__all__ = ['bit_flip', 'flip_all']


def bit_flip(c, k: int):
    """ flip bit at position k """
    cop = c.copy()
    cop[k] = abs(c[k]-1)
    return cop

def flip_bit(b):
    return abs(b-1)

def flip_all(c):
    """ flip all bits (unsigned 64bit int)"""
    return np.vectorize(flip_bit)(c.copy())
