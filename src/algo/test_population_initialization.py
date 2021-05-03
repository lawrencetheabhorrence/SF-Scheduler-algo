from . population_initialization import generateChromosome
from . population_initialization import initPop
import random


def test_generateChromosome():
    c = generateChromosome(50)
    assert c.bit_length() == 51


def test_randomChromosomeLengths():
    cs = [random.randint(30, 300) for _ in range(50)]
    for x in cs:
        c = generateChromosome(x)
        assert c.bit_length() == x + 1


def test_initPop():
    p = initPop(50, 7, 5, 2, 3)
    assert len(p) == 50 and len(p[0]) == 7 * 5 * 2 * 3
