from . bit_helper import locateBit
from . bit_helper import isSet


def test_isSet():
    assert isSet(3, 111001)
