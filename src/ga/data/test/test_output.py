import ga.data.output as o
import ga.data.reader as rea


root = '~/GitHub/SF-Scheduler-algo/src/ga/data/test/'


def test_bits_to_sched():
    c = np.array([1,1,1,1,0,1,0,0,0,1,0,1,0,1,1,0])
    sf_data = rea.read_sf_data(root + 'test_sf_data.csv')
    game_data = rea.read_game_data(root + 'test_game_data.csv')
    result = o.bits_to_sched(c, sf_data, game_data)[0]['Games']
    assert result[0] == 'A Cat 1\nB Cat 2'
    assert result[1] == 'A Cat 1\nA Cat 2\nB Cat 1\nB Cat 2'
    assert result[2] == 'A Cat 1\nA Cat 3'
