import numpy as np
import random as r
from ga.ga_methods.population_initialization import generate_chromosome
import ga.ga_methods.non_rand.mutation_non_rand as mnr
import ga.ga_methods.mutation as mt


def test_bit_flip():
    c = 0b11101101
    c = np.array([1,1,1,0,1,1,0,1])
    np.testing.assert_array_equal(mnr.bit_flip(c,1),
                                  np.array([1,0,1,0,1,1,0,1]))
    np.testing.assert_array_equal(mnr.bit_flip(c, 2),
                                  np.array([1,1,0,0,1,1,0,1]))


def test_flip_all():
    c = generate_chromosome(8)
    assert np.bitwise_and(c, mnr.flip_all(c)).sum() == 0


def test_uniform():
    c = generate_chromosome(8)
    assert c.size == mt.uniform(c).size
