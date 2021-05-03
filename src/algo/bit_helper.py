from typing import Dict


def locate_bit(cats_per_game: Dict[str, int],
               game: str, cat: int, slot: int, total_slots: int):
    # Note that cat is given as a number/index
    """ returns the index of the gene based on the game, cat, and slot """
    return cat * slot \
        + ([cats_per_game[g] * total_slots for g in len(cats_per_game)
            if g != game])


def is_set(n: int, bits: int):
    """ is the byte at the nth position 1 ? """
    lone_bit = 0b1 << n
    return ((bits & lone_bit) >> n) % 2  # 1 if true, 0 otherwise
