"""
Phase 2: Scientific Delivery-Level Cricket Pressure Engine
Project RR-EDGE: Global Cricket Pressure Intelligence & IPL 2027 Auction Optimization System
"""

import os
import numpy as np
import pandas as pd

def compute_delivery_pressure(bbb_df, matches_df, comps_df):
    """
    Computes rigorous, pre-delivery contextual pressure for both batting and bowling sides.
    Guarantees ZERO target leakage by using strictly pre-delivery cumulative match state.
    """
    print("Computing pre-delivery cumulative match state...")
    
    # Sort chronologically by match_id, innings, overid, over_ball_num, innings_ball_num
    df = bbb_df.sort_values(['match_id', 'innings', 'overid', 'over_ball_num', 'innings_ball_num']).copy()
    
    # Total runs on delivery
    df['total_delivery_runs'] = df['runs'] + df['extras1_runs'] + df['extras_2_runs']
    
    # Legal delivery flag (wides and no-balls do not count as legal balls in the over)
    df['is_legal_ball'] = ~df['extras_type'].isin(['wide', 'Overstep'])
    
    # Pre-delivery cumulative stats within innings
    # Shift by 1 to guarantee strictly PRE-DELIVERY state
    grouped_inn = df.groupby(['match_id', 'innings'])
    
    df['cum_runs_pre'] = grouped_inn['total_delivery_runs'].cumsum() - df['total_delivery_runs']
    df['cum_wickets_pre'] = grouped_inn['is_wicket'].cumsum() - df['is_wicket']
    df['cum_legal_balls_pre'] = grouped_inn['is_legal_ball'].cumsum() - df['is_legal_ball']
    
    # Merge match-level context: knock_out, revised_target, revised_overs
    match_meta = matches_df[['match_id', 'knock_out', 'revised_target', 'first_inn_revised_overs', 'second_inn_revised_overs']].copy()
    df = df.merge(match_meta, on='match_id', how='left')
    
    # Determine Innings 1 total score for each match to set target for Innings 2
    inn1_totals = df[df['innings'] == 1].groupby('match_id')['total_delivery_runs'].sum().reset_index().rename(columns={'total_delivery_runs': 'inn1_actual_total'})
    df = df.merge(inn1_totals, on='match_id', how='left')
    
    # Compute Target for Innings 2
    # If revised_target is specified, use revised_target; otherwise inn1_actual_total + 1
    df['target_score'] = np.where(df['revised_target'].notna() & (df['revised_target'] > 0),
                                  df['revised_target'],
                                  df['inn1_actual_total'] + 1)
    
    # Scheduled overs for innings
    df['scheduled_overs'] = np.where(df['innings'] == 1,
                                     df['first_inn_revised_overs'].fillna(20.0),
                                     df['second_inn_revised_overs'].fillna(20.0))
    df['scheduled_balls'] = (df['scheduled_overs'] * 6).astype(int)
    
    # Balls remaining & wickets in hand pre-delivery
    df['balls_remaining'] = np.maximum(1, df['scheduled_balls'] - df['cum_legal_balls_pre'])
    df['wickets_in_hand'] = np.maximum(0, 10 - df['cum_wickets_pre'])
    
    # Current Run Rate (CRR)
    df['crr'] = np.where(df['cum_legal_balls_pre'] > 0,
                         (df['cum_runs_pre'] / df['cum_legal_balls_pre']) * 6.0,
                         8.0) # default opening CRR baseline
    
    # Innings Phase: Powerplay (overs 1-6), Middle (7-15), Death (16-20)
    df['over_num'] = df['overid'] # 1-indexed
    df['phase'] = np.where(df['over_num'] <= 6, 'Powerplay',
                           np.where(df['over_num'] <= 15, 'Middle', 'Death'))

    print("Calculating scientific pressure components...")
    
    # --- CHASE PRESSURE (Innings 2 & 4) ---
    runs_needed = np.maximum(0, df['target_score'] - df['cum_runs_pre'])
    rrr = np.where(df['balls_remaining'] > 0, (runs_needed / df['balls_remaining']) * 6.0, 36.0)
    
    # Bounded transformations
    # 1. Scoring Urgency (0 to 1): par is 8.0 rpo; 14+ is severe urgency
    scoring_urgency = np.clip((rrr - 6.0) / 10.0, 0.0, 1.2)
    
    # 2. Wicket Scarcity (0 to 1)
    wicket_scarcity = 1.0 - (df['wickets_in_hand'] / 10.0)
    
    # 3. Time Scarcity (0 to 1)
    time_scarcity = 1.0 - np.clip(df['balls_remaining'] / 120.0, 0.0, 1.0)
    
    # 4. RRR vs CRR spread
    rate_escalation = np.clip((rrr - df['crr']) / 6.0, -0.5, 1.2)
    
    # 5. Leverage / Closeness
    # Highest when runs needed is within reach but balls and wickets are few
    leverage = (1.0 / (1.0 + np.exp((runs_needed - 30) / 15.0))) * (1.0 - (df['balls_remaining'] / 120.0)) * (1.5 - (df['wickets_in_hand'] / 10.0))
    leverage = np.clip(leverage, 0.0, 1.0)
    
    # Innings 2 Batting Pressure Index (0 - 100)
    raw_chase_pressure = (
        0.28 * scoring_urgency +
        0.22 * wicket_scarcity +
        0.20 * time_scarcity +
        0.18 * np.maximum(0, rate_escalation) +
        0.12 * leverage
    ) * 100.0
    
    # --- FIRST INNINGS PRESSURE (Innings 1 & 3) ---
    # Expected par runs in 1st innings ~ 168 (8.4 rpo)
    par_score = 168.0
    overs_done = df['cum_legal_balls_pre'] / 6.0
    expected_score_so_far = overs_done * 8.4
    deficit = expected_score_so_far - df['cum_runs_pre']
    
    inn1_urgency = np.clip(deficit / 25.0, -0.2, 1.0)
    inn1_phase_weight = np.where(df['phase'] == 'Death', 0.85, np.where(df['phase'] == 'Middle', 0.45, 0.25))
    
    # High wicket loss early causes acute pressure (e.g. 30/4 in powerplay)
    early_collapse = np.where((df['cum_legal_balls_pre'] <= 36) & (df['wickets_in_hand'] <= 7),
                              (8 - df['wickets_in_hand']) * 0.15, 0.0)
    
    raw_inn1_pressure = (
        0.30 * wicket_scarcity +
        0.25 * inn1_phase_weight +
        0.25 * np.maximum(0, inn1_urgency) +
        0.20 * early_collapse
    ) * 100.0
    
    # Select Chase vs 1st Innings
    is_chase = df['innings'].isin([2, 4])
    base_batting_pressure = np.where(is_chase, raw_chase_pressure, raw_inn1_pressure)
    
    # Super Over is guaranteed maximum pressure
    is_super_over = df['innings'].isin([3, 4])
    base_batting_pressure = np.where(is_super_over, 100.0, base_batting_pressure)
    
    # Knockout Multiplier (Playoffs / Finals carry higher psychological & tactical stakes)
    knockout_boost = np.where(df['knock_out'] == 1, 1.12, 1.0)
    final_batting_pressure = np.clip(base_batting_pressure * knockout_boost, 0.0, 100.0)
    
    # --- BOWLING PRESSURE MODEL ---
    # Bowler pressure mirrors batting pressure but incorporates defending requirements:
    # Defending a low target in death overs or facing an aggressive batter who is ahead of RRR
    # If chasing side needs 12 off 12 balls, bowling pressure is extreme (85+)
    # If chasing side needs 75 off 12 balls, bowling pressure is very low (20)
    raw_bowling_chase_pressure = np.where(
        is_chase,
        # Chasing team close to target with balls in hand -> intense bowler pressure
        (0.35 * scoring_urgency + 0.30 * time_scarcity + 0.20 * (1.0 - wicket_scarcity) + 0.15 * leverage) * 100.0,
        # 1st innings bowling pressure: Death overs, or when batting team is scoring heavily (CRR > 10)
        (0.40 * inn1_phase_weight + 0.35 * np.clip((df['crr'] - 7.5) / 5.0, 0.0, 1.0) + 0.25 * (1.0 - wicket_scarcity)) * 100.0
    )
    raw_bowling_pressure = np.where(is_super_over, 100.0, raw_bowling_chase_pressure)
    final_bowling_pressure = np.clip(raw_bowling_pressure * knockout_boost, 0.0, 100.0)

    # Attach to DataFrame
    df['batting_pressure_index'] = np.round(final_batting_pressure, 2)
    df['bowling_pressure_index'] = np.round(final_bowling_pressure, 2)
    
    # Categorical bins
    def categorize(score):
        if score < 45.0:
            return 'Normal'
        elif score < 70.0:
            return 'High'
        else:
            return 'Extreme'
            
    df['batting_pressure_category'] = df['batting_pressure_index'].apply(categorize)
    df['bowling_pressure_category'] = df['bowling_pressure_index'].apply(categorize)
    
    print(f"Pressure Engine computation complete. Average Batting Pressure: {df['batting_pressure_index'].mean():.2f}, Bowling: {df['bowling_pressure_index'].mean():.2f}")
    print("Batting Pressure Category Distribution:")
    print(df['batting_pressure_category'].value_counts(normalize=True).round(3))
    
    return df

if __name__ == "__main__":
    BASE_DIR = r"C:\Users\PREMCHANDYADAV\Downloads\RR_Competition"
    DATA_DIR = os.path.join(BASE_DIR, r"6af458274c1e8_data_pack\Data Pack")
    bbb = pd.read_csv(os.path.join(DATA_DIR, 'ball_by_ball.csv'), low_memory=False)
    matches = pd.read_csv(os.path.join(DATA_DIR, 'matches.csv'), low_memory=False)
    comps = pd.read_csv(os.path.join(DATA_DIR, 'competitions.csv'), low_memory=False)
    df_pressure = compute_delivery_pressure(bbb, matches, comps)
    print("Sample Output:")
    print(df_pressure[['innings', 'overid', 'over_ball_num', 'batting_pressure_index', 'batting_pressure_category', 'bowling_pressure_index']].head(10))
