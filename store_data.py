from nba_api.stats.static import players
from nba_api.stats.endpoints import shotchartdetail
from nba_api.stats.endpoints import playerdashptshots
from nba_api.stats.endpoints import playerdashboardbyclutch
import pandas as pd
from icecream import ic


player_dict = players.get_active_players()
master_scd = pd.DataFrame()
master_pdc_last1_5point = pd.DataFrame()
ids = [1629638, 1628960]

for p in player_dict:
    p_id = p['id']
    p_name = [p['full_name']]
    """sc = shotchartdetail.ShotChartDetail(
        0, p_id, context_measure_simple='FGA', season_nullable='2020-21')
    sc_df = sc.get_data_frames()[0]
    master_scd = master_scd.append(sc_df)
    """
    pdash_clutch = playerdashboardbyclutch.PlayerDashboardByClutch(
        p_id, season='2020-21')
    last1_5point_df = pdash_clutch.get_data_frames()[3]
    last1_5point_df['PLAYER_NAME'] = p_name
    master_pdc_last1_5point = master_pdc_last1_5point.append(
        last1_5point_df)

master_pdc_last1_5point.to_csv(
    r'/Users/johanketkar/Projects/KahunaIndex/playerdashbyclutch1min5point.csv', index=False)


""" master_scd.to_csv(
    r'/Users/johanketkar/Projects/KahunaIndex/shortchartdetail.csv', index=False) """
