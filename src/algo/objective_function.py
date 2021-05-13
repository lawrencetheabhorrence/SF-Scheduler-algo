from typing import Dict
from itertools import chain
from . bit_helper import locate_bit
from .objective_helper import \
        enough_consec_slots, if_simultaneous, \
        split_chromosome


# def fitness(hardPenalty = -10, softPenalty=-1):
# return hardPenalty * (hc3 + hc4) + softPenalty * (sc1 + sc2)


def hc3(c: int, min_slots_per_game: Dict[str, int],
        cats_per_game: Dict[str, int], slots):
    """ Events of games must have consecutive n timeslots,
    where n is given by the user for a particular game"""
    slices_per_game = split_chromosome(c, cats_per_game, slots)
    print(slices_per_game)
    # okay... so unpacking all of this
    # we are basically running the constraint on each slice
    # since we are processing it on a dictionary, the bools
    # are in a 2d list since each sublist
    # corresponds to a game
    # (mapping over each value in the dict .. basically)
    # we then flatten that list and check if it is true for
    # all slices
    fulfilled = list(chain(*[[enough_consec_slots(game_slice,
                                                  min_slots_per_game[g])
                              for game_slice in slices_per_game[g]]
                             for g in slices_per_game]))
    return 1 if all(fulfilled) else 0


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
