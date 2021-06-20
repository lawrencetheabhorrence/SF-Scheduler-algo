import numpy as np
from typing import Dict

class Chromosome:

    def __init__(self, length):
        self.fitness = 0
        self.bitstring = np.choice([0, 1], size=length)

    def is_set(self, pos: int) -> int:
        """ is the byte as the nth postion 1?
        (0-indexed) """
        return self.bitstring[pos]

    def locate_bit(self,
                   cats_per_game: Dict[str, int],
                   game: str, cat: int,
                   slot: int, slots: int) -> int:
        """ returns index of the gene based on
        the game, cat and timeslot (in whole SF)
        the gene is supposed to represent """
        partial = 0
        for g in cats_per_game.keys():
            if g == game:
                return slot + (cat - 1) * slots + partial
            partial += cats_per_game[g] * slots

        raise ValueError('Game name is not in the list of games')

    def AND(self, other):
        return np.bitwise_and(self.bitstring, other.bitstring)

    def OR(self, other):
        return np.bitwise_or(self.bitstring, other.bitstring)

    def NOT(self):
        return np.invert(self.bitstring)
