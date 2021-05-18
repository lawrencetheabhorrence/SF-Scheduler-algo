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


def is_set(n: int, bits: int) -> bool:
    """ is the byte at the nth position 1 ?
    (1-indexed)
    """
    lone_bit = 0b1 << n
    return ((bits & lone_bit) >> n) % 2  # 1 if true, 0 otherwise


def bit_slice(start: int, end: int, bits: int) -> int:
    """ returns a bit string from start pos
    to end pos (inclusive and 1-indexed) """
    bits = bin(bits)
    return int(bits[start+1:end+2], 2)
