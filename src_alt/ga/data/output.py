import numpy as np
import pandas as pd
from ga.data.reader import read_sf_data, read_game_data
from ga.objective_function.fitness_helper import split_chromosome_per_game_str


def split_sched(c, slots):
    """ splits bitstrings w/o prefix into sections """
    return [c[s: s + slots] for s in range(0, len(c), slots)]


def place_events_in_sched(c: str, event_name: str, sched: pd.DataFrame):
    """ place events into the Dataframe, multiple events can happen in
    a timeslot, so events are separated by newlines """
    for i, x in enumerate(c):
        if x == '1':
            if sched['Games'][i] == '':
                sched['Games'][i] = event_name
            else:
                sched['Games'][i] = sched['Games'][i] + '\n' + event_name


def generate_empty_scheds(sf_data):
    """ generates a list of dataframes (one per day),
    with no events but with time indexes corresponding to time slots """
    slots_per_day = sf_data['slots'][0] // sf_data['days'][0]
    dates = pd.date_range(sf_data['start_date'][0] + ' ' +
                          sf_data['start_time'][0],
                          periods=sf_data['days'][0])
    time_ranges = (pd.date_range(d, periods=slots_per_day,
                                 freq=f"{sf_data['minutes_per_slot'][0]}T")
                   for d in dates)
    data = [''] * slots_per_day
    return [pd.DataFrame(index=tr,
                         columns=['Games'],
                         data=data)
            for tr in time_ranges]

def bits_to_sched(c,
                  sf_src="data/sf_data.csv",
                  game_src="data/game_data.csv"):
    """ transforms a complete chromosome into a schedule in a
    csv """
    sf_data = pd.read_csv(sf_src,
                          dtype={'slots': int, 'days': int,
                                 'minutes_per_slot': int,
                                 'start_time': str,
                                 'start_date': str})
    game_data = read_game_data(game_src)

    slots_per_day = sf_data['slots'][0] // sf_data['days'][0]

    # dictionary with {g: []} where g is a game and [] is a list of
    # bitstrings corresponding to schedules of categories of games
    sched_per_game = split_chromosome_per_game_str(c,
                                                   game_data['cats'],
                                                   sf_data['slots'][0])

    # dictionary with {g: [[]]} where g is a game and the outer list
    # corresponds to the categories of a game
    # the inner list is a list of bitstrings corresponding to scheds
    # for one day
    sched_per_game = {g: np.array([split_sched(x, slots_per_day)
                                   for x in sched_per_game[g]])
                      for g in sched_per_game}

    # suppose we want to get the schedules only for one day,
    # we can achieve that through taking an element from the second dimension
    # or the innerlist of the dictionary item
    # thus this list is a list of dictionaries with the games as keys
    # and the keys are a numpy array of bitstrings
    # that correspond to schedules for a day for the categories of a game
    scheds_per_day = [{g: sched_per_game[g][:, d] for g in sched_per_game}
                      for d in range(sf_data['days'][0])]

    empty_scheds = generate_empty_scheds(sf_data)

    for day in range(sf_data['days'][0]):
        for game in scheds_per_day[day]:
            for cat, sched in enumerate(scheds_per_day[day][game], start=1):
                event_name = f"{game} Cat {cat}"
                place_events_in_sched(sched, event_name, empty_scheds[day])

    return empty_scheds
