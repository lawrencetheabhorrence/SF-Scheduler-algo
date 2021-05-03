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


def generate_chromosome(slots):
    return random.getrandbits(slots - 1) + (2 ** slots)


def init_pop(pop_size, days, slots_per_day, games, cats):
    return [generate_chromosome(days * slots_per_day * games * cats)
            for _ in range(pop_size)]
