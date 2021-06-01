import pandas as pd


def read_game_data(src="data/game_data.csv"):
    df = pd.read_csv(src, index_col="Games",
                     dtype={'cats': int, 'priority': 'string',
                            'slots/round': int, 'rounds': int})
    return df.to_dict()


def read_sf_data(src="data/sf_data.csv"):
    df = pd.read_csv(src).astype(int)
    return (df['slots'][0], df['days'][0])
