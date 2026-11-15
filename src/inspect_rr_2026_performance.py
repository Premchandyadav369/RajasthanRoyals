import os
import pandas as pd
import numpy as np

base = r"C:\Users\PREMCHANDYADAV\Downloads\RR_Competition\6af458274c1e8_data_pack\Data Pack"
bbb = pd.read_csv(os.path.join(base, 'ball_by_ball.csv'), low_memory=False)
matches = pd.read_csv(os.path.join(base, 'matches.csv'), low_memory=False)

m_2026 = matches[matches['comp_id'] == 3298]
rr_m_ids = set(m_2026[(m_2026['home_team'].str.contains('Royals', case=False, na=False)) | 
                      (m_2026['away_team'].str.contains('Royals', case=False, na=False))]['match_id'])

bbb_rr = bbb[bbb['match_id'].isin(rr_m_ids)].copy()
bbb_rr['is_wide'] = bbb_rr['extras_type'].str.lower() == 'wide'
bbb_rr['is_noball'] = bbb_rr['extras_type'].str.lower().isin(['overstep', 'no ball', 'noball'])
bbb_rr['is_legal'] = ~bbb_rr['is_wide'] & ~bbb_rr['is_noball']
bbb_rr['total_runs'] = bbb_rr['runs'] + bbb_rr['extras1_runs']

rr_bat = bbb_rr[bbb_rr['batting_team_id'] == 3]
rr_bowl = bbb_rr[bbb_rr['bowling_team_id'] == 3]

print("=== RR BATTING IN IPL 2026 ===")
print("Total Sixes Hit:", rr_bat['is_six'].sum())
print("Total Fours Hit:", rr_bat['is_four'].sum())
print("Total Runs Scored:", rr_bat['total_runs'].sum())
legal_balls = rr_bat['is_legal'].sum()
print("Overall Batting Run Rate:", round(rr_bat['total_runs'].sum() / (legal_balls / 6.0), 2))

# Phases: PP (overs 0-5), Middle 7-11 (overs 6-10), Middle 12-16 (overs 11-15), Death (overs 16-19)
pp_bat = rr_bat[rr_bat['overid'] <= 5]
m7_11_bat = rr_bat[(rr_bat['overid'] >= 6) & (rr_bat['overid'] <= 10)]
death_bat = rr_bat[rr_bat['overid'] >= 16]

print(f"PP Run Rate (Overs 1-6): {pp_bat['total_runs'].sum() / (pp_bat['is_legal'].sum() / 6.0):.2f}")
print(f"Overs 7-11 Run Rate: {m7_11_bat['total_runs'].sum() / (m7_11_bat['is_legal'].sum() / 6.0):.2f}")
print(f"Death Run Rate (Overs 17-20): {death_bat['total_runs'].sum() / (death_bat['is_legal'].sum() / 6.0):.2f}")

print("\n=== RR BOWLING IN IPL 2026 ===")
print("Total Runs Conceded:", rr_bowl['total_runs'].sum())
legal_bowl = rr_bowl['is_legal'].sum()
print("Overall Bowling Economy:", round(rr_bowl['total_runs'].sum() / (legal_bowl / 6.0), 2))

pp_bowl = rr_bowl[rr_bowl['overid'] <= 5]
m7_11_bowl = rr_bowl[(rr_bowl['overid'] >= 6) & (rr_bowl['overid'] <= 10)]
death_bowl = rr_bowl[rr_bowl['overid'] >= 16]

print(f"PP Bowling Economy (Overs 1-6): {pp_bowl['total_runs'].sum() / (pp_bowl['is_legal'].sum() / 6.0):.2f}")
print(f"Overs 7-11 Bowling Economy: {m7_11_bowl['total_runs'].sum() / (m7_11_bowl['is_legal'].sum() / 6.0):.2f}")
print(f"Death Bowling Economy (Overs 17-20): {death_bowl['total_runs'].sum() / (death_bowl['is_legal'].sum() / 6.0):.2f}")

# Wickets taken
non_bowler = ['run out', 'retired hurt', 'obstructing the field']
rr_bowl['is_bowler_wkt'] = (rr_bowl['is_wicket'] == 1) & (~rr_bowl['dismissal_type'].str.lower().isin(non_bowler))
total_wkts = rr_bowl['is_bowler_wkt'].sum()
print("Total Bowler Wickets Taken:", total_wkts)
print(f"Bowling Strike Rate (balls/wkt): {legal_bowl / total_wkts:.2f}")

print("\n=== INDIVIDUAL RR BATTERS 2026 ===")
bat_grp = rr_bat.groupby(['striker_id', 'striker_name']).agg(
    runs=('runs', 'sum'),
    balls=('is_legal', 'sum'),
    sixes=('is_six', 'sum'),
    fours=('is_four', 'sum')
).reset_index()
bat_grp['strike_rate'] = (bat_grp['runs'] / bat_grp['balls']) * 100.0
print(bat_grp.sort_values('runs', ascending=False).to_string())

print("\n=== INDIVIDUAL RR BOWLERS 2026 ===")
bowl_grp = rr_bowl.groupby(['bowler_id', 'bowler_name']).agg(
    runs=('total_runs', 'sum'),
    balls=('is_legal', 'sum'),
    wkts=('is_bowler_wkt', 'sum')
).reset_index()
bowl_grp['overs'] = bowl_grp['balls'] / 6.0
bowl_grp['economy'] = bowl_grp['runs'] / bowl_grp['overs']
print(bowl_grp.sort_values('wkts', ascending=False).to_string())
