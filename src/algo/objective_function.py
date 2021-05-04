from typing import List
from typing import Dict
from . bit_helper import is_set

# def fitness(hardPenalty = -10, softPenalty=-1):
# return hardPenalty * (hc3 + hc4) + softPenalty * (sc1 + sc2)


def if_simultaneous(c: int, slots: int, first: int):
    """
    Is there a simultaneous slot occupied with the same game and category?
    Note in the chromosome, timeslots are incremented first
    then categories then games

    Thus shifting by the total number of timeslots should move
    to the same timeslot but in a different category
    """
    for i in range(first, first+slots):
        if is_set(i, c) and is_set(i, c+slots):
            return True
        c << 1
    return False


def hc4(c: int, games: List[str], cats: int, priorityPerGame: Dict[str, int]):
    """ Hard Constraint 4: Major games cannot have simultaneous games
    in the same category """
    totalSlots = bin(c).bit_length()
    for i, g in enumerate(games):
        if (priorityPerGame[g] == 'Major'
                and if_simultaneous(c, totalSlots, i * totalSlots)):
            return 1
    return 0
