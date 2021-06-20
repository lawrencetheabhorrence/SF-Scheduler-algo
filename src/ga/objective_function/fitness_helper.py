import re
import numpy as np
from itertools import chain
from functools import reduce
from typing import Dict, List, Callable
import ga.helper.Chromosome as chro
from ga.helper.bit_helper import bit_slice, bitlength


def occupieds(c) -> List[str]:
    """get all sequences of occupied slots
    in a chromosome """
    bitstr = ''.join(c.bitstring)
    # We retain this as a list of strings as
    # there is no place where we will need to
    # interact with the individual bits
    return np.array(list(
            filter(lambda x: len(x) > 0,
                   re.split(r'0+', bitstr))
           ))


def enough_consec_slots(c, min_slots) -> bool:
    """for this game and category, are there enough
    consecutive occupied slots?

    Checks if the number of slots of each group of
    occupied slots is a non zero multiple of the number
    of slots per round"""
    # We can easily now map len to the whole array
    # By executing map_len(x)
    # It also gives a very nice performance gain.
    map_len = np.vectorize(len)

    # cond will return a mask, replacing each element with
    # True if it passes the condition and False otherwise
    occ = occupieds(c)
    cond = (map_len(occ) >= min_slots) & (map_len(occ) % min_slots == 0)
    return cond.all()


def enough_rounds(c: str, rounds: int) -> bool:
    """for this game and category, are the
    number of rounds correct?"""
    return occupieds(c).size == rounds


def if_simultaneous(c, slots, first, cats) -> bool:
    """
    Does this game have a simultaneous slot occupied
    in two different categories?
    """
    bitstr = c.bitstring
    if cats == 1:
        return np.bitwise_and(bitstr[0:slots], bitstr[slots:slots*2]).sum() > 0

    # slice with all slots related to the game
    game_slice = bitstr[first:first + slots * cats]
    # we then reshape this array into a 2d array
    # where every subarray corresponds to a category of a game
    game_slice = game_slice.reshape(cats, slots)
    # we then "fold" over this array with the bitwise and
    # to get a resulting chromosome that *should* be 0
    # if there are no simultaneous events in two different categories
    return np.bitwise_and.reduce(game_slice, axis=0).sum() > 0


def split_chromosome(c, slots):
    """ splits chromosome into sections as long
    as the total timeslots for the SF """
    return c.bitstring.reshape(c.size // slots, slots)

def aggregate_occupied(c, slots):
    """ returns a bitstring as long as the total number
    of slots for the SF. A bit should only have 0 if
    there are absolutely no games in that slot """
    sections = split_chromosome(c, slots)
    return np.bitwise_and.reduce(sections, axis=0)

def has_even_share(c, section_len):
    """ when splitting a bitstring into groups of
    fixed width, there should be an equal number
    of 1's in each group (or as equal as possible)"""
    bitstr = c.bitstring
    n_occupied_slots = bitstr.sum()
    optimal_occupieds_per_section = n_occupied_slots / section_len
    n_occupied_per_section = split_chromosome(c, section_len).sum(axis=1)
    map_dist = np.vectorize(lambda x: abs(x - optimal_occupieds_per_section))
    return map_dist(n_occupied_per_section).sum() / n_occupied_per_section.size


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
    """ The same as split_chromosome_per_game but
    returns strings. Useful for when you need to preserve the
    original bitlengths of the sections """

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
