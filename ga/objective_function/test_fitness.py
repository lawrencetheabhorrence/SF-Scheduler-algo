import numpy as np
import ga.objective_function.fitness as fit
import ga.data.reader as rea


def test_hc3():
    c = np.array([1,1,1,1,0,0,1,1,0,1,1,1,1,0,0,1,1,0,1,0,1,0,1,1,1,0,0,1])
    cats_per_game = {'A': 3, 'B': 2, 'C': 2}
    slots = 4
    min_slots_per_game = {'A': 3, 'B': 3, 'C': 3}
    min_slots_true = {'A': 1, 'B': 1, 'C': 1}
    assert not fit.hc3(c, min_slots_true, cats_per_game, slots) > 0 \
        and fit.hc3(c, min_slots_per_game, cats_per_game, slots) > 0


def test_hc4():
    c = np.array([1,1,1,1,0,1,0,0,1,0,0,1,0,0,1,1,1,0,0,0,1,0,1,0])
    priority_per_game = {'A': 'Major', 'B': 'Major', 'C': 'Major'}
    cats_per_game = {'A': 3, 'B': 2, 'C': 3}
    slots = 3
    assert fit.hc4(c, cats_per_game, priority_per_game, slots) == 0


def test_hc5():
    c = np.array([1,1,0,0,1,1,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1])
    cats_per_game = {'A': 3, 'B': 2, 'C': 3}
    slots = 3
    rounds_per_game = {g: 1 for g in ['A', 'B', 'C']}
    rounds_invalid = {g: 3 for g in ['A', 'B', 'C']}
    min_slots_per_game = {'A': 2, 'B': 3, 'C': 3}
    assert fit.hc5(c, rounds_per_game, min_slots_per_game, cats_per_game, slots) == 0
    assert fit.hc5(c, rounds_invalid, min_slots_per_game, cats_per_game, slots) > 0


def test_sc1():
    c = np.array([0,1,1,1,0,0,1,1,1,0,0,1,1,1,0])
    days = 1
    slots = 5
    assert fit.sc1(c, slots, days) - 2.4 < 0.01


def test_centering_score():
    c = np.array([0,0,0,1,1,1,0,0,0])
    c2 = np.array([0,0,0,0,1,1,0,0,0])
    assert fit.centering_score(c) == 0
    assert fit.centering_score(c2) > 0
    assert fit.centering_score(c) < fit.centering_score(c2)


def test_sc2():
    slots = 9
    days = 3
    c = np.array([0,1,0,1,1,1,0,0,0])
    c_skewed = np.array([1,0,0,1,1,1,0,0,0])
    assert fit.sc2(c, slots, days) == 0
    assert fit.sc2(c_skewed, slots, days) > 0


# def test_fitness():
    # c = np.array([1,0,1,1,1,1,1,1,0,1,1,0,1,0,0])
    # c2 = np.array([0,1,0,0,1,0,0,1,0,0,1,0,0,1,0])
    # root = '~/GitHub/SF-Scheduler-algo/ga/data/test/'
    # game_data = rea.read_game_data(root+"test_game_data.csv")
    # sf_data = rea.read_sf_data(root+"test_sf_data.csv")
    # assert fit.fitness(c2, game_data, sf_data) == fit.fitness(c, game_data, sf_data)
