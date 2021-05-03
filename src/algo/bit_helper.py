import typing


def locateBit(gameList: list[str], catsPerGame: dict[str, int],
              game: str, cat: int, slot: int, totalSlots: int):
    # Note that cat is given as a number/index
    # returns the index of the gene based on the game, cat, and slot
    return cat * slot
    + ([catsPerGame[g] * totalSlots for g in gameList if g != game])


def isSet(n: int, bits: int):
    # is the byte at the nth position 1 ?
    loneBit = 0b1 << n
    return ((bits & loneBit) >> n) % 2  # 1 if true, 0 otherwise
