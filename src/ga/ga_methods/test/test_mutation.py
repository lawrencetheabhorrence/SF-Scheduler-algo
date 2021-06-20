import random as r
import ga.ga_methods.non_rand.mutation_non_rand as mnr
import ga.ga_methods.mutation as mt
from ga.helper.bit_helper import bitlength


def test_bit_flip():
    c = 0b11101101
    assert mnr.bit_flip(c, 1) == 0b11101111
    assert mnr.bit_flip(c, 2) == 0b11101001


def test_flip_all():
    c = 2**8 | r.randrange(2**8 + 1)
    assert c & mnr.flip_all(c) == 2**8


def test_uniform():
    c = 2 ** 8 | r.randrange(2**8)
    assert bitlength(c) == bitlength(mt.uniform(c))
