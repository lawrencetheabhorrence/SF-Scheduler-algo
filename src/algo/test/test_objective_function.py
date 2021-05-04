from . objective_function import if_simultaneous


def test_if_simultaneous():
    has_simultaneous = if_simultaneous(11011100, 4, 3)
    assert has_simultaneous
