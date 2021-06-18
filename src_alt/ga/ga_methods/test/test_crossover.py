import random as r
from ..non_rand import crossover_non_rand as cnr
from ga.helper.bit_helper import bitlength

def generate_parents(n=8):
    """ generates two random parents with bitlength n """
    return (2**n | r.randrange(2**n + 1), 2**n | r.randrange(2**n + 1))

def test_one_point():
    c1 = 0b11111
    c2 = 0b10101
    result = cnr.one_point(c1, c2, 2)
    assert result == (0b11101, 0b10111)

def test_split_ks():
    test = "Hello World~"
    ks = [0, 3, 5, 7]
    result = cnr.split_ks(test, ks)
    assert result == [test[0:3], test[3:5], test[5:7], test[7:]]

def test_n_point():
    # generate 2 numbers with bitlength of 8
    c1, c2 = generate_parents()

    # initialize break_points
    k_length = r.randrange(7)
    ks = [0]*(k_length - 1) + [8]
    for i in range(1, len(ks)):
        while ks[i] <= ks[i-1]:
            ks[i] = r.randrange(1, 8)

    result = list(map(lambda x: bin(x)[2:], cnr.n_point(c1, c2, ks)))

    c1 = bin(c1)[2:]
    c2 = bin(c2)[2:]

    assert all(((c1[ks[i]:ks[i+1]] == result[0][ks[i]:ks[i+1]]
                 if i % 2 == 0
                 else c2[ks[i]:ks[i+1]] == result[0][ks[i]:ks[i+1]])
                for i in range(len(ks) - 1)))

    assert all(((c2[ks[i]:ks[i+1]] == result[0][ks[i]:ks[i+1]]
                 if i % 2 == 0
                 else c1[ks[i]:ks[i+1]] == result[0][ks[i]:ks[i+1]])
                for i in range(len(ks) - 1)))


def test_uniform():
    c1, c2 = generate_parents()
    result = cnr.uniform(c1, c2, 3)
    assert len(result) == 3

    assert all((n := bitlength(c1) == bitlength(x) for x in result))
