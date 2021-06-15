import re
from math import ceil, log2
from itertools import chain
from functools import reduce
from typing import Dict, List, Callable
from ga.helper.bit_helper import bit_slice
__all__ = ["occupieds", "enough_consec_slots", "enough_rounds",
           "if_simultaneous", "split_chromosome",
           "aggregate_occupied", "has_even_share",
           "split_chromosome_per_game", "check_cond_for_each_game"]

def occupieds(c: int) -> List[str]:
    """get all sequences of occupied slots
    in bit string """
    # remove 0b prefix, split the string by the zero
    # to get all sequences of occupied slots
    return \
        list(filter(lambda x: len(x) > 0, re.split(r'0+', bin(c)[2:])))


def enough_consec_slots(c: int, min_slots: int) -> bool:
    """for this game and category, are there enough
    consecutive occupied slots?"""
    # check if the occupieds
    # are a nonzero multiple of the minimum timeslots
    return all(x >= min_slots and x % min_slots == 0
               for x in map(len, occupieds(c)))


def enough_rounds(c: str, rounds: int) -> bool:
    """for this game and category, are the
    number of rounds correct?"""
    return len(occupieds(c)) == rounds
"

def if_simultaneous(c: int, slots: int,
                    first: int, cats: int) -> bool:
    """
    Is there a simultaneous slot occupied with the same game and category?
    Note in the chromosome, timeslots are
    incremented first then categories then games

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


def split_chromosome(c: int, slots: int) -> List[str]:
    """ splits chromosome into sections as long
    as the total timeslots for the SF """
    # strip 0b prefix and leading 1
    c = bin(c)[3:]
    return [c[s: s + slots] for s in range(0, len(c), slots)]

def aggregate_occupied(c: int, slots: int):
    """ returns a bitstring as long as the total number
    of slots for the SF. A bit should only have 0 if
    there are absolutely no games in that slot """
    sections = map(int, split_chromosome(c, slots))
    return reduce(lambda x, y: x | y, sections) | 1 << (ceil(log2(c))-1)


def has_even_share(c: int, section_len: int):
    """ when splitting a bitstring into groups of
    fixed width, there should be an equal number
    of 1's in each group (or as equal as possible)"""
    occupieds = bin(c)[3:].count('1')
    optimal_occupieds_per_section = occupieds / section_len
    occupieds_per_section = list(map(lambda x: x.count('1'),
                                 split_chromosome(c, section_len)))
    return sum(map(lambda x: abs(x - optimal_occupieds_per_section),
                   occupieds_per_section))/len(occupieds_per_section)


def split_chromosome_per_game(c: int,
                              cats_per_game: Dict[str, int],
                              slots: int) -> Dict[str, int]:
    """
    Splits chromosome into sections per game-chromosome.
    basically each section should be as long as the number of
    total slots.
    The result is stored in a dictionary with the keys
    as the games of the timetable and the values
    corresponding to the slices associated
    with each game.
    """
    sections = split_chromosome(c, slots)

    end = 0
    game_slices = {}
    for g in cats_per_game:

        game_slices[g] = list(map(lambda x: int(x, 2),
                                  sections[end:end+cats_per_game[g]]))
        end += cats_per_game[g]
    return game_slices

def split_chromosome_per_game_str(c: int,
                                  cats_per_game: Dict[str, int],
                                  slots: int) -> Dict[str, str]:
    sections = split_chromosome(c, slots)
    end = 0
    game_slices = {}
    for g in cats_per_game:
        game_slices[g] = list(sections[end:end+cats_per_game[g]])
        end += cats_per_game[g]

    return game_slices


def check_cond_for_each_game(c: int,
                             cats_per_game: Dict[str, int], slots,
                             min_per_game: Dict[str, int],
                             pred: Callable[[int, int], bool]):
    """ Runs the constraint on each slice with all timeslots
    Useful for constraints where the condition is dependent
    on the game """
    # we are basically running the constraint on each slice
    # since we are processing it on a dictionary, the bools
    # are in a 2d list since each sublist
    # corresponds to a game
    # (mapping over each value in the dict .. basically)
    # we then flatten that list and check if it is true for
    # all slices
    slices_per_game = split_chromosome_per_game(c, cats_per_game, slots)
    fulfilled = list(chain(*[[pred(game_slice, min_per_game[g])
                              for game_slice in slices_per_game[g]]
                             for g in slices_per_game]))
    return 1 if all(fulfilled) else 0
