import pandas as pd
__all__ = ["read_game_data", "read_sf_data"]


def read_game_data(src="data/game_data.csv"):
    df = pd.read_csv(src, sep=',',
                     dtype={
                         'cats': int,
                         'priority': 'string',
                         'slots/round': int, 'rounds': int
                     })
    return df.to_dict()


def read_sf_data(src="data/sf_data.csv"):
    df = pd.read_csv(src, sep=',',
                     dtype={'slots': int,
                            'days': int,
                            'minutes_per_slot': int,
                            'start_time': str,
                            'start_date': str})
    d = df.to_dict()
    return {p: d[p][0] for p in d}
