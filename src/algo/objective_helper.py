import re
from typing import Dict
from . bit_helper import bit_slice, locate_bit


def enough_consec_slots(c: str, min_slots: int) -> bool:
    """for this game and category, are there enough
    consecutive occupied slots?"""
    # remove 0b prefix, split the string by the zero
    # to get all sequences of occupied slots
    # thus check if they are a nonzero multiple of the minimum timeslots
    return all(x >= min_slots and x % min_slots == 0
               for x in map(len, re.split(r'0+', bin(c)[2:])))


def if_simultaneous(c: int, slots: int,
                    first: int, cats: int) -> bool:
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
    for cat in range(1, cats):
        first = bit_slice(1, cats, c)
        comp = bit_slice(1 + (slots * cat), (slots * (cat + 1)), c)
        if (first & comp) > 0:
            return True
    return False


def split_chromosome(c: int,
                     cats_per_game: Dict[str, int],
                     slots) -> Dict[str, int]:
    """
    Splits chromosome into sections per game-chromosome.
    basically each section should be as long as the number of
    total slots.
    The result is stored in a dictionary with the keys
    as the games of the timetable and the values
    corresponding to the slices associated
    with each game.
    """
    # strip 0b prefix and leading 1
    c = bin(c)[3:]
    sections = [c[s: s + slots] for s in range(0, len(c), slots)]

    end = 0
    game_slices = {}
    for g in cats_per_game:
        game_slices[g] = list(map(lambda x: int(x, 2), \
                                  sections[end:end+cats_per_game[g]]))
        end += cats_per_game[g]

    return game_slices
