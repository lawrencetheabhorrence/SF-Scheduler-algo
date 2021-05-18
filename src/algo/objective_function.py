from typing import Dict
from . bit_helper import locate_bit
from .objective_helper import \
        enough_consec_slots, if_simultaneous, \
        split_chromosome_per_game, aggregate_occupied, \
        split_chromosome, check_cond_for_each_game, \
        enough_rounds


# def fitness(hardPenalty = -10, softPenalty=-1):
# return hardPenalty * (hc3 + hc4) + softPenalty * (sc1 + sc2)


def hc3(c: int, min_slots_per_game: Dict[str, int],
        cats_per_game: Dict[str, int], slots):
    """ Events of games must have consecutive n timeslots,
    where n is given by the user for a particular game"""
    return check_cond_for_each_game(c, cats_per_game, slots,
                                    min_slots_per_game,
                                    enough_consec_slots)

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


def hc5(c: int, cats_per_game: Dict[str, int],
        rounds_per_game: Dict[str, int], slots: int):
    return check_cond_for_each_game(c, cats_per_game, slots,
                                    rounds_per_game,
                                    enough_rounds)

def sc1(c: int, slots: int, days: int):
    """The total number of events per day
    must be evenly distributed over the week."""
    occupieds = aggregate_occupied(c, slots).count('1')
    slots_per_day = slots // days
    occupieds_per_day = map(lambda x: x.count('1'),
                            split_chromosome(c, slots_per_day))
    optimal_slots = occupieds // days
    return sum(map(lambda x: abs(x - optimal_slots), occupieds_per_day))/days


def centering_score(c: str):
    first_one, last_one = c.find('1'), c.rfind('1')
    if first_one < 0:
        return 0

    ideal_zeroes_len = (len(c) - (last_one - first_one + 1))/2
    return abs(first_one - ideal_zeroes_len)


def sc2(c: int, slots: int, days: int):
    """ Minimize games nearer to the starting and
    ending time per day. """
    slots_per_day = slots // days
    sections = split_chromosome(c, slots_per_day)
    return sum((centering_score(x) for x in sections))/slots_per_day
