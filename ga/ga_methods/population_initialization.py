"""
Chromosomes (timetables) are generated as bit strings
where each gene stands for whether a certain game
and category is selected on a certain timeslot.

To calculate the length of the bit string we have:
    (days) * (timeslots per day) * (games) * (categories)

The initial population size is 50,
but another value can be passed to the initialization function.
"""
import numpy as np


def generate_chromosome(slots):
    rng = np.random.default_rng()
    return rng.integers(2, size=slots)


def init_pop(pop_size, game_data, sf_data):
    slots = sf_data['slots']
    days = sf_data['days']
    # games = len(game_data['cats'])
    cats = sum(game_data['cats'].values())
    return [generate_chromosome(slots * cats * days)
            for _ in range(pop_size)]
