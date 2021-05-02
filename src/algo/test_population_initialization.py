from . population_initialization import generateChromosome
from . population_initialization import initPop

def test_generateChromosome():
    c = generateChromosome(50);
    assert c.bit_length() == 50;

def initPop_test():
    p = initPop(50, 7, 5, 2, 3);
    assert len(p) == 50 and len(p[0]) == 7 * 5 * 2 * 3;
