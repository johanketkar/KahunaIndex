from nba_api.stats.static import players
from nba_api.stats.endpoints import shotchartdetail
from nba_api.stats.endpoints import playerdashptshots
import pandas as pd
from icecream import ic
import time

player_dict = players.get_players()
master_list = []
current_player = {'name': None, 'id': None, 'kahuna': None}


def get_scd_stats(id):
    ic(id)
    sc = shotchartdetail.ShotChartDetail(0, id, last_n_games=5)
    ic()
    df = sc.get_data_frames()[0]
    longshot_total = 0
    for index, row in df.iterrows():
        if(row['SHOT_DISTANCE'] > 24):
            longshot_total += row['SHOT_DISTANCE']

    return longshot_total


def get_pds_stats(id):
    return (0, 0, 0)


def kahunator(id):
    kahuna = 0
    pds_stats = get_pds_stats(id)
    scd_stats = get_scd_stats(id)
    kahuna = scd_stats
    return kahuna


def master_list_entry_creator(p):
    player_id = p['id']
    player_name = p['full_name']
    current_player['name'] = player_name
    current_player['id'] = player_id
    current_player['kahuna'] = kahunator(player_id)
    master_list.append(current_player.copy())


for p in player_dict:
    if(p['is_active']):
        master_list_entry_creator(p)

kahuna_df = pd.DataFrame.from_dict(master_list)
final_df = kahuna_df.sort_values(by=['kahuna'], ascending=False)
print(final_df)


""" def get_kahuna_index(df):
    kahuna = 0
    for index, row in df.iterrows():
        if(row["SHOT_DISTANCE"] > 24):
            kahuna += (row["SHOT_DISTANCE"]-24)
    return kahuna


test_name = "LeBron James"


def kahunator(name):
    df = get_stats(name)
    kahuna = get_kahuna_index(df)
    print(name, " Kahuna Index: ", kahuna)


df = get_shots(test_name)
print(df) """
