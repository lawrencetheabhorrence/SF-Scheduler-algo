locateBit(gameList, catsPerGame, game, cat, slot, totalSlots):
    # Note that cat is given as a number/index
    # returns the index of the gene based on the game, cat, and slot
    return cat * slot + sum([catsPerGame[g] * slot, for g in gameList if g != game])

isSet(n, bits):
    # is the byte at the nth position 1 ?
    loneBit = 0b1 << n;
    return ((bits && loneBit) >> n) % 2; # 1 if true, 0 otherwise
    
fitness(hardPenalty = -10, softPenalty=-1):
    return hardPenalty * (hc3 + hc4) + softPenalty * (sc1 + sc2);

hc3(c):
    totalSlots = bin(c).bit_Length();
    if isSet(locateBit(


