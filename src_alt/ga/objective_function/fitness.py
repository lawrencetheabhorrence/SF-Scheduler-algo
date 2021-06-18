from math import ceil, log2
from typing import Dict
from ga.data.reader import read_sf_data, read_game_data
from ga.helper.bit_helper import locate_bit
import ga.objective_function.fitness_helper as fh


def fitness(c,
            game_data, sf_data,
            hardReward=100, softPenalty=-20):
    """ fitness value """
    cats, priority, rounds, slots_per_round = game_data.values()
    slots, days = sf_data
    scores = {'hc3': hc3(c, slots_per_round, cats, slots),
              'hc4': hc4(c, cats, priority, slots),
              'hc5': hc5(c, cats, rounds, slots),
              'sc1': sc1(c, slots, days),
              'sc2': sc2(c, slots, days)}
    print(scores)
    return (hardReward * (scores['hc3'] + scores['hc4'] + scores['hc5'])
            + softPenalty * (scores['sc1'] + scores['sc2']))


def hc3(c: int, slots_per_round: Dict[str, int],
        cats_per_game: Dict[str, int], slots):
    """ Events of games must have consecutive n timeslots,
    where n is given by the user for a particular game"""
    return fh.check_cond_for_each_game(c, cats_per_game, slots,
                                    slots_per_round,
                                    fh.enough_consec_slots)


def hc4(c: int, cats_per_game: Dict[str, int],
        priority_per_game: Dict[str, int], slots):
    """ Hard Constraint 4: Major games cannot have simultaneous games
    in the same category """
    major_games = filter(lambda g: priority_per_game[g] == 'Major',
                         list(priority_per_game))

    for g in major_games:
        pos = locate_bit(cats_per_game, g, 1, 1, slots)
        if fh.if_simultaneous(c, slots, pos, cats_per_game[g]):
            return 0
    return 1


def hc5(c: int, cats_per_game: Dict[str, int],
        rounds_per_game: Dict[str, int], slots: int):
    """ Games must have exactly the given number of rounds """
    return fh.check_cond_for_each_game(c, cats_per_game, slots,
                                       rounds_per_game,
                                       fh.enough_rounds)

def sc1(c: int, slots: int, days: int):
    """The total number of events per day
    must be evenly distributed over the week."""
    return fh.has_even_share(fh.aggregate_occupied(c, slots),
                             slots // days)


def centering_score(c: str):
    first_one, last_one = c.find('1'), c.rfind('1')
    if first_one < 0:
        return 0

    ideal_zeroes_len = (len(c) - (last_one - first_one + 1))/2
    return abs(first_one - ideal_zeroes_len)/len(c)


def sc2(c: int, slots: int, days: int):
    """ Minimize games farther to the starting and
    ending time per day.  (or games closer to the "middle") """
    slots_per_day = slots // days
    sections = fh.split_chromosome(c, slots_per_day)
    return sum((centering_score(x) for x in sections))/len(sections)
