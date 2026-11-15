import os
import pandas as pd
import numpy as np

base = r"C:\Users\PREMCHANDYADAV\Downloads\RR_Competition\6af458274c1e8_data_pack\Data Pack"
bbb = pd.read_csv(os.path.join(base, 'ball_by_ball.csv'), low_memory=False)
matches = pd.read_csv(os.path.join(base, 'matches.csv'), low_memory=False)
teams = pd.read_csv(os.path.join(base, 'teams.csv'), low_memory=False)

m_2026 = matches[matches['comp_id'] == 3298]
m_ids_2026 = set(m_2026['match_id'])
bbb_2026 = bbb[bbb['match_id'].isin(m_ids_2026)].copy()

bbb_2026['is_wide'] = bbb_2026['extras_type'].str.lower() == 'wide'
bbb_2026['is_noball'] = bbb_2026['extras_type'].str.lower().isin(['overstep', 'no ball', 'noball'])
bbb_2026['is_legal'] = ~bbb_2026['is_wide'] & ~bbb_2026['is_noball']
bbb_2026['total_runs'] = bbb_2026['runs'] + bbb_2026['extras1_runs']

# Map team names
t_map = teams[teams['comp_id'] == 3298].set_index('team_id')['team_name'].to_dict()
bbb_2026['bat_team'] = bbb_2026['batting_team_id'].map(t_map)
bbb_2026['bowl_team'] = bbb_2026['bowling_team_id'].map(t_map)

print("=== LEAGUE BATTING STATS 2026 ===")
team_bat = bbb_2026.groupby('bat_team').agg(
    sixes=('is_six', 'sum'),
    runs=('total_runs', 'sum'),
    balls=('is_legal', 'sum')
).reset_index()
team_bat['run_rate'] = team_bat['runs'] / (team_bat['balls'] / 6.0)
print(team_bat.sort_values('sixes', ascending=False).to_string())

# PP Batting
pp = bbb_2026[bbb_2026['overid'] <= 5]
pp_bat = pp.groupby('bat_team').agg(
    runs=('total_runs', 'sum'),
    balls=('is_legal', 'sum')
).reset_index()
pp_bat['pp_rr'] = pp_bat['runs'] / (pp_bat['balls'] / 6.0)
print("\n=== POWERPLAY BATTING RUN RATE ===")
print(pp_bat.sort_values('pp_rr', ascending=False).to_string())

# Middle Overs 7-11 (overid 6 to 10)
m711 = bbb_2026[(bbb_2026['overid'] >= 6) & (bbb_2026['overid'] <= 10)]
m711_bat = m711.groupby('bat_team').agg(
    runs=('total_runs', 'sum'),
    balls=('is_legal', 'sum')
).reset_index()
m711_bat['m711_rr'] = m711_bat['runs'] / (m711_bat['balls'] / 6.0)
print("\n=== OVERS 7-11 BATTING RUN RATE ===")
print(m711_bat.sort_values('m711_rr', ascending=False).to_string())

# Bowling Economy Overs 7-11
m711_bowl = m711.groupby('bowl_team').agg(
    runs=('total_runs', 'sum'),
    balls=('is_legal', 'sum')
).reset_index()
m711_bowl['m711_bowl_econ'] = m711_bowl['runs'] / (m711_bowl['balls'] / 6.0)
print("\n=== OVERS 7-11 BOWLING ECONOMY ===")
print(m711_bowl.sort_values('m711_bowl_econ', ascending=True).to_string())
