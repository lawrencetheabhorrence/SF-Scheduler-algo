"""
Chromosomes (timetables) are generated as bit strings
where each gene stands for whether a certain game and category is selected on a certain timeslot.
To calculate the length of the bit string we have:
    (days) * (timeslots per day) * (games) * (categories)
The initial population size is 50, but another value can be passed to the initialization function.
"""
import random

def generateChromosome(slots):
    return random.getrandbits(slots - 1) + (2 ** slots);

def initPop(popSize, days, slotsPerDay, games, cats):
    return [generateChromosome(days * slotsPerday * games * cats) for _ in range(popSize)];


