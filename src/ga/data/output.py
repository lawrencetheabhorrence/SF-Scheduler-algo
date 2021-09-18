import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from ga.data.reader import read_sf_data, read_game_data
from ga.objective_function.fitness_helper import split_chromosome_per_game


def place_events_in_sched(c: str, event_name: str, sched):
    """ place events into the Dataframe, multiple events can happen in
    a timeslot, so events are separated by newlines """
    for i in range(c.size):
        if c[i] == 1:
            if sched.iloc[i,0] == '':
                sched.iloc[i,0] = event_name
            else:
                sched.iloc[i,0] = sched.iloc[i,0] + '\n' + event_name


def generate_empty_scheds(sf_data):
    """ generates a list of dataframes (one per day),
    with no events but with time indexes corresponding to time slots """
    slots_per_day = sf_data['slots']
    dates = pd.date_range(sf_data['start_date'] + ' ' +
                          sf_data['start_time'],
                          periods=sf_data['days'])
    time_ranges = (pd.date_range(start=d, periods=slots_per_day,
                                 freq=f"{sf_data['minutes_per_slot']}T")
                   for d in dates)
    data = [''] * slots_per_day
    return [pd.DataFrame(index=tr,
                         columns=['Games'],
                         data=data)
            for tr in time_ranges]


def bits_to_sched(c, sf_data, game_data):
    """ transforms a complete chromosome into a schedule in a
    csv """

    slots_per_day = sf_data['slots']

    # dictionary with {g: []} where g is a game and [] is a list of
    # bitstrings corresponding to schedules of categories of games
    sched_per_game = split_chromosome_per_game(c,
                                               game_data['cats'],
                                               sf_data['slots'] *
                                               sf_data['days'])

    # dictionary with {g: [[]]} where g is a game and the outer list
    # corresponds to the categories of a game
    # the inner list is a list of bitstrings corresponding to scheds
    # for one day
    sched_per_game = {g: [x.reshape(x.size // slots_per_day, slots_per_day)
                          for x in sched_per_game[g]]
                      for g in sched_per_game}
    # suppose we want to get the schedules only for one day,
    # we can achieve that through taking an element from the second dimension
    # or the innerlist of the dictionary item
    # thus this list is a list of dictionaries with the games as keys
    # and the keys are a numpy array of bitstrings
    # that correspond to schedules for a day for the categories of a game
    scheds_per_day = [{g: [sched_per_game[g][c][d, :]
                           for c in range(game_data['cats'][g])]
                       for g in sched_per_game}
                      for d in range(sf_data['days'])]

    empty_scheds = generate_empty_scheds(sf_data)

    for day in range(sf_data['days']):
        for game in scheds_per_day[day]:
            for cat, sched in enumerate(scheds_per_day[day][game], start=1):
                event_name = f"{game} Cat {cat}"
                place_events_in_sched(sched, event_name, empty_scheds[day])

    return empty_scheds


def plot_mut_cross_graphs():
    root = '~/GitHub/SF-Scheduler-algo/src/data/model/cross_mut'
    crossover = ['one point', 'n point (5)', 'uniform']
    mutation = ['bit flip', 'flip all', 'uniform']
    fig, ax = plt.subplots(3, 3)
    plt.title('Crossover + Mutation')
    for i, c in enumerate(crossover):
        for j, m in enumerate(mutation):
            src = f'{root}/fitness_{c[0]}{m[0]}.csv'
            df = pd.read_csv(src, sep=",")
            df['Average Fitness'].plot(ax=ax[i, j])
            ax[i, j].set_title(c + ' + ' + m)

    # plt.savefig(f'{root}/graph.png')
    plt.subplots_adjust(top=0.948,
                        bottom=0.057,
                        left=0.05,
                        right=0.989,
                        hspace=0.36,
                        wspace=0.181)
    plt.show()
