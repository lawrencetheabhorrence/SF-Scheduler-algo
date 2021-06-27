"""
Chromosomes (timetables) are generated as bit strings
where each gene stands for whether a certain game
and category is selected on a certain timeslot.

To calculate the length of the bit string we have:
    (days) * (timeslots per day) * (games) * (categories)

The initial population size is 50,
but another value can be passed to the initialization function.
"""
import random
import numpy as np
from ..data.reader import read_game_data, read_sf_data


def generate_chromosome(slots):
    return np.random.randint(low=0, high=2, size=slots)


def init_pop(pop_size, game_data, sf_data):
    slots = sf_data['slots']
    games = len(game_data['cats'])
    cats = sum(game_data['cats'].values())
    return [generate_chromosome(slots * games * cats)
            for _ in range(pop_size)]
