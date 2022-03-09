import pandas as pd
__all__ = ["read_game_data", "read_sf_data"]

def calc_rounds_from_teams(n_teams, priority):
    return (n_teams) * (n_teams -1) / 2 if priority == "Major" else n_teams - 1


def read_game_data(src="data/game_data.csv", teams=3):
    df = pd.read_csv(src, sep=', ',
                     dtype={
                         'cats': int,
                         'priority': 'string',
                         'slots/round': int, 'rounds': float
                     })
    df['rounds'] = df['rounds'].fillna(df['priority'].apply(lambda p: calc_rounds_from_teams(teams, p)))
    return df.to_dict()


def read_sf_data(src="data/sf_data.csv"):
    df = pd.read_csv(src, sep=',',
                     dtype={'slots': int,
                            'days': int,
                            'minutes_per_slot': int,
                            'start_time': str,
                            'start_date': str,
                            'teams': int})
    d = df.to_dict()
    return {p: d[p][0] for p in d}
