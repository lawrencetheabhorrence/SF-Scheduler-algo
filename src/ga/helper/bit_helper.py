from typing import Dict

def locate_bit(cats_per_game: Dict[str, int],
               game: str, cat: int,
               slot: int, slots: int) -> int:
    # Note that cat is given as a number/index
    """ returns the index of the gene based on the game, cat, and slot """
    partial = 0
    for g in cats_per_game.keys():
        if g == game:
            break
        partial += cats_per_game[g] * slots
    return slot + (cat - 1) * slots + partial
