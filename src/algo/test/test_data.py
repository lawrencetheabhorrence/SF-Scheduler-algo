from ..data import bits_to_sched


def test_bits_to_sched():
    c = 0b1111010001010110
    sf_src = 'test/data/test_sf_data.csv'
    game_src = 'test/data/test_game_data.csv'
    result = bits_to_sched(c, sf_src, game_src)[0]['Games']
    assert result[0] == 'A Cat 1\nB Cat 2'
    assert result[1] == 'A Cat 1\nA Cat 2\nB Cat 1\nB Cat 2'
    assert result[2] == 'A Cat 1\nA Cat 3'
