from typing import Dict
from . bit_helper import is_set
from . bit_helper import locate_bit
from . bit_helper import bit_slice
from . bit_helper import all_set

# def fitness(hardPenalty = -10, softPenalty=-1):
# return hardPenalty * (hc3 + hc4) + softPenalty * (sc1 + sc2)


def if_simultaneous(c: int, slots: int, first: int, cats: int):
    """
    Is there a simultaneous slot occupied with the same game and category?
    Note in the chromosome, timeslots are incremented first
    then categories then games

    Thus shifting by the total number of timeslots should move
    to the same timeslot but in a different category
    """
    if cats == 1:
        return bit_slice(1, slots, c) \
                & bit_slice(slots + 1, slots * 2, c) > 0
    else:
        for cat in range(1, cats):
            first = bit_slice(1, cats, c)
            comp = bit_slice(1 + (slots * cat), (slots * (cat + 1)), c)
            if (first & comp) > 0:
                return True
    return False


def hc4(c: int, cats_per_game: Dict[str, int],
        priority_per_game: Dict[str, int], slots):
    """ Hard Constraint 4: Major games cannot have simultaneous games
    in the same category """
    major_games = filter(lambda g: priority_per_game[g] == 'Major',
                         list(priority_per_game))

    for g in major_games:
        pos = locate_bit(cats_per_game, g, 1, 2, slots)
        if if_simultaneous(c, slots, pos, cats_per_game[g]):
            return 1
    return 0
