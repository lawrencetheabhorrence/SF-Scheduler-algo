import ga.objective_function.fitness as fit
import ga.data.reader as rea


def test_hc3():
    c = 0b1111001101111001101010111001
    cats_per_game = {'A': 3, 'B': 2, 'C': 4}
    slots = 3
    min_slots_per_game = {'A': 3, 'B': 3, 'C': 3}
    min_slots_true = {'A': 1, 'B': 1, 'C': 1}
    assert not fit.hc3(c, min_slots_per_game, cats_per_game, slots) > 0 \
        and fit.hc3(c, min_slots_true, cats_per_game, slots) > 0


def test_hc4():
    priority_per_game = {'A': 'Major', 'B': 'Major', 'C': 'Major'}
    cats_per_game = {'A': 3, 'B': 2, 'C': 3}
    slots = 3
    c = 0b1111010001001001110001010
    assert fit.hc4(c, cats_per_game, priority_per_game, slots) == 0


def test_hc5():
    cats_per_game = {'A': 3, 'B': 2, 'C': 3}
    slots = 3
    rounds_per_game = {g: 1 for g in ['A', 'B', 'C']}
    rounds_invalid = {g: 3 for g in ['A', 'B', 'C']}
    c = 0b1111010001001001110001010
    assert fit.hc5(c, cats_per_game, rounds_per_game, slots) == 1
    assert fit.hc5(c, cats_per_game, rounds_invalid, slots) == 0


def test_sc1():
    c = 0b1011100111001110
    days = 1
    slots = 5
    assert fit.sc1(c, slots, days) - 0.66 < 0.01


def test_centering_score():
    assert fit.centering_score('000111000') == 0
    assert fit.centering_score('000011000') > 0
    assert fit.centering_score('000011000') < fit.centering_score('000001100')


def test_sc2():
    slots = 9
    days = 3
    c = 0b1111010000
    c_skewed = 0b1001110011
    assert fit.sc2(c, slots, days) == 0
    assert fit.sc2(c_skewed, slots, days) > 0


def test_fitness():
    c = 0b1101111110110100
    c2 = 0b1010010010010010
    root = '~/GitHub/SF-Scheduler-algo/src/ga/data/test/'
    game_data = rea.read_game_data(root+"test_game_data.csv")
    sf_data = rea.read_sf_data(root+"test_sf_data.csv")
    assert fit.fitness(c2, game_data, sf_data) > fit.fitness(c, game_data, sf_data)
