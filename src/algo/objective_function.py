""" guys i should really add in parameter types """
""" this parameter naming just sucks ass """
import typing
    
fitness(hardPenalty = -10, softPenalty=-1):
    return hardPenalty * (hc3 + hc4) + softPenalty * (sc1 + sc2);

ifSimultaneous(c: int, slots: int, first: int):
    # Is there a simultaneous slot occupied with the same game and category?
    # Note in the chromosome, timeslots are incremented first then categories then games
    # Thus shifting by the total number of timeslots should move to the same timeslot but in a different category
    # go study modular arithmetic if you dont get it
    for i in range(first, first+slots):
        if isSet (i, c) and isSet(i, c+slots): return True;
        c << 1;
    return False;

hc4(c: int, games: list[string], cats: int, priorityPerGame: dict[string, int]):
    """ Hard Constraint 4: Major games cannot have simultaneous game in the same category """
    totalSlots = bin(c).bit_Length();
    for i, g in enumerate(games):
        if priorityPerGame[g] == 'Major' and ifSimultaneous(c, totalSlots, i * totalSlots) return 1
    return 0


