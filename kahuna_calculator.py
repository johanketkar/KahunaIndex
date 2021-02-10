import pandas as pd

scd_df = pd.read_csv(
    r'/Users/johanketkar/Projects/KahunaIndex/shortchartdetail.csv')

pdbc_1min_5pt_df = pd.read_csv(
    r'/Users/johanketkar/Projects/KahunaIndex/playerdashbyclutch1min5point.csv')

scd_dict = {}
pdbc_1min_5pt_dict = {}
kahuna_dict = {}

grouped = scd_df.groupby(scd_df.PLAYER_NAME)
pdbc_1min_5pt_grouped = pdbc_1min_5pt_df.groupby(pdbc_1min_5pt_df.PLAYER_NAME)

for key, item in grouped:
    scd_dict[key] = grouped.get_group(key)

for key, item in pdbc_1min_5pt_grouped:
    pdbc_1min_5pt_dict[key] = pdbc_1min_5pt_grouped.get_group(key)


def calculate(sc_df, pdbc_df):
    longshot_total = 0
    clutch_attempts = 0
    late_game = False
    for index, row in sc_df.iterrows():
        if(row['PERIOD'] == 4 and row['MINUTES_REMAINING'] <= 5):
            late_game = True
        else:
            late_game = False
        if(row['SHOT_DISTANCE'] > 24):
            if(late_game):
                longshot_total += (2*(row['SHOT_DISTANCE'] - 24))/100
            else:
                longshot_total += (row['SHOT_DISTANCE'] - 24)/100

    for index, row in pdbc_df.iterrows():
        if(row['FGA']):
            clutch_attempts = row['FGA']

    return round(longshot_total+clutch_attempts, 2)


def normalize(d, target=100.0):
    raw = sum(d.values())
    factor = target/raw
    return {key: value*factor for key, value in d.items()}


for player in scd_dict:
    kahuna_dict[player] = calculate(
        scd_dict[player], pdbc_1min_5pt_dict[player])

norm_kahuna_dict = normalize(kahuna_dict)

kahuna_df = pd.DataFrame.from_dict(kahuna_dict, orient='index')
kahuna_df = kahuna_df.rename(columns={0: "KahunaIndex"}, errors="raise")
kahuna_df = kahuna_df.sort_values(by=['KahunaIndex'], ascending=False)
kahuna_df.to_csv(
    r'/Users/johanketkar/Projects/KahunaIndex/kahuna.csv')
