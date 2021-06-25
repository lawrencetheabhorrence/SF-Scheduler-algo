import random as r
import numpy as np
import numpy.testing as test
from ga.ga_methods.population_initialization import generate_chromosome
from ..non_rand import crossover_non_rand as cnr


def generate_parents(n=8):
    """ generates two random parents with bitlength n """
    return (generate_chromosome(n), generate_chromosome(n))

def test_one_point():
    c1 = np.array([1,1,1,1,1])
    c2 = np.array([1,0,1,0,1])
    result = cnr.one_point(c1, c2, 2)
    test.assert_array_equal(result[0],[1,1,1,0,1])
    test.assert_array_equal(result[1],[1,0,1,1,1])


def test_n_point():
    # generate 2 numbers with bitlength of 9
    c1, c2 = generate_parents()
    print(c1, c2)
    n = c1.size

    # initialize break_points
    rng = np.random.default_rng()
    ks = rng.choice(np.arange(1, n),
                    size=3,
                    shuffle=False,
                    replace=False)
    ks = np.sort(ks)

    print(ks)

    result = cnr.n_point(c1, c2, ks)
    print(result)
    ks = np.concatenate(([0], ks, [n]))


    for i in range(len(ks) - 1):
        if i % 2 == 0:
            test.assert_array_equal(c1[ks[i]:ks[i+1]],
                                    result[0,ks[i]:ks[i+1]])
            test.assert_array_equal(c2[ks[i]:ks[i+1]],
                                    result[1,ks[i]:ks[i+1]])
        else:
            test.assert_array_equal(c1[ks[i]:ks[i+1]],
                                    result[1,ks[i]:ks[i+1]])
            test.assert_array_equal(c2[ks[i]:ks[i+1]],
                                    result[0,ks[i]:ks[i+1]])


def test_uniform():
    c1, c2 = generate_parents()
    result = cnr.uniform(c1, c2, 3)
    print(result)
    assert len(result) == 3
    assert result[0].shape == c1.shape
