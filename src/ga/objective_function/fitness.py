import numpy as np
from typing import Dict
from ga.data.reader import read_sf_data, read_game_data
from ga.helper.bit_helper import locate_bit
from itertools import chain
import ga.objective_function.fitness_helper as fh


def fitness(c,
            game_data, sf_data,
            hardReward=-100, softPenalty=-10):
    """ fitness value """
    cats, priority, rounds, slots_per_round = game_data.values()
    slots, days = sf_data['slots'] * sf_data['days'], sf_data['days']
    scores = {'hc3': hc3(c, slots_per_round, rounds, cats, slots),
              'hc4': hc4(c, cats, priority, slots),
              'sc1': sc1(c, slots, days),
              'sc2': sc2(c, slots, days)}
    print(scores, c.size)
    return (hardReward * (scores['hc3'] + scores['hc4'])
            + softPenalty * (scores['sc1'] + scores['sc2']))


def hc3(c, slots_per_round: Dict[str, int],
        rounds_per_game: Dict[str, int],
        cats_per_game: Dict[str, int], slots):
    """ Events of games must have consecutive n timeslots,
    where n is given by the user for a particular game"""
    slices_per_game = fh.split_chromosome_per_game(c, cats_per_game, slots)
    fulfilled = list(chain(*[[fh.enough_consec_slots(
                                   game_slice,
                                   slots_per_round[g], 
                                   rounds_per_game[g])
                              for game_slice in slices_per_game[g]]
                             for g in slices_per_game]))
    print(fulfilled)
    return sum(fulfilled)/len(fulfilled)
    

def hc4(c, cats_per_game: Dict[str, int],
        priority_per_game: Dict[str, int], slots):
    """ Hard Constraint 4: Major games cannot have simultaneous games
    in the same category """
    major_games = filter(lambda g: priority_per_game[g] == 'Major',
                         list(priority_per_game))
    game_slices = fh.split_chromosome_per_game(c, cats_per_game, slots)
    game_slices = [game_slices[g] for g in major_games]
    for g in range(len(game_slices) - 1):
        for cat in range(g):
            for o in range(g+1, len(game_slices)):
                if np.bitwise_and(game_slices[g][cat],
                                  game_slices[o][cat]).sum() > 0:
                    return 1
    
    return 0


def sc1(c, slots: int, days: int):
    """The total number of events per day
    must be evenly distributed over the week."""
    return fh.has_even_share(fh.aggregate_occupied(c, slots),
                             slots // days)


def centering_score(c):
    if c.sum() == 0:
        return 0
    one_index = c.nonzero()[0]
    first_one, last_one = one_index[0], one_index[-1]

    ideal_zeroes_len = (c.size - (last_one - first_one + 1))/2
    return abs(first_one - ideal_zeroes_len)/c.size


def sc2(c, slots: int, days: int):
    """ Minimize games farther to the starting and
    ending time per day.  (or games closer to the "middle") """
    slots_per_day = slots // days
    sections = fh.split_chromosome(c, slots_per_day)
    return np.apply_along_axis(centering_score, 1,
                               sections).sum()/len(sections)
