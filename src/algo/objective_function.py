from itertools import chain
from typing import Dict, List
import re
from . bit_helper import is_set, locate_bit, bit_slice

# def fitness(hardPenalty = -10, softPenalty=-1):
# return hardPenalty * (hc3 + hc4) + softPenalty * (sc1 + sc2)


def enough_consec_slots(c: int, min_slots: int):
    """for this game and category, are there enough
    consecutive occupied slots?"""
    # remove 0b prefix, split the string by the zero
    # to get all sequences of occupied slots
    # thus check if they are a nonzero multiple of the minimum timeslots
    return all(x >= min_slots and x % min_slots == 0
               for x in map(len, re.split(r'0+', bin(c)[2:])))


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


def split_chromosome(c: int, cats_per_game: Dict[str, int], slots):
    c = bin(c)[3:]
    return {g: [bit_slice(
        pos := locate_bit(cats_per_game, g, 1 + slots*cat),
        pos + slots*(cat+1) - 1,
        slots) for cat in range(cats_per_game[g])]
        for g in cats_per_game}


def hc3(c: int, min_slots_per_game: Dict[str, int],
        cats_per_game: Dict[str, int], slots):
    splits = split_chromosome(c, cats_per_game, slots)
    return all(chain(*[[enough_consec_slots(game_slice,
                                            min_slots_per_game[g])
                        for game_slice in splits[g]]
                     for g in splits]))


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
