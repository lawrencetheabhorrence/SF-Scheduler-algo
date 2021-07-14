import random as r
from typing import List, Dict, Tuple
from ga.objective_function.fitness import fitness


def rank(pop,
         game_data: Dict[str, int],
         sf_data: Tuple[int, int]):
    """ choose parent by ranking fitness """
    pop.sort(key=(lambda x: fitness(x, game_data, sf_data)),
             reverse=False)
    return r.choices(pop,
                     weights=[i/sum(range(1, len(pop)+1))
                              for i in range(len(pop), 0, -1)],
                     k=1)[0]
