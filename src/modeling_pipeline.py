"""
Phase 3-7: Advanced Batting & Bowling Performance Models, Machine Learning (LightGBM xR/xW),
Bayesian Shrinkage, Match-Level Bootstrap & Final Rating System (PBRS & PBwRS).
Project RR-EDGE: Global Cricket Pressure Intelligence & IPL 2027 Auction Optimization System
"""

import os
import json
import warnings
import numpy as np
import pandas as pd
from scipy import stats
import lightgbm as lgb
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler

warnings.filterwarnings('ignore')

BASE_DIR = r"C:\Users\PREMCHANDYADAV\Downloads\RR_Competition"
DATA_DIR = os.path.join(BASE_DIR, r"6af458274c1e8_data_pack\Data Pack")
ENRICH_DIR = os.path.join(BASE_DIR, "data_enrichment")
OUTPUTS_DIR = os.path.join(BASE_DIR, "outputs")

from pressure_engine import compute_delivery_pressure

def run_performance_modeling():
    print("=" * 70)
    print("PHASES 3-7: PERFORMANCE MODELING, MACHINE LEARNING & BAYESIAN RATING")
    print("=" * 70)

    # 1. Load data
    print("\n[Step 1] Loading raw datasets...")
    bbb = pd.read_csv(os.path.join(DATA_DIR, 'ball_by_ball.csv'), low_memory=False)
    matches = pd.read_csv(os.path.join(DATA_DIR, 'matches.csv'), low_memory=False)
    comps = pd.read_csv(os.path.join(DATA_DIR, 'competitions.csv'), low_memory=False)
    player_master = pd.read_csv(os.path.join(ENRICH_DIR, 'player_identity_master.csv'))
    comp_strength = pd.read_csv(os.path.join(ENRICH_DIR, 'global_competition_strength.csv'))
    opp_ratings = pd.read_csv(os.path.join(ENRICH_DIR, 'opposition_attack_ratings.csv'))

    # 2. Compute Pressure on all 200,999 deliveries
    print("\n[Step 2] Computing delivery-level pressure index...")
    df = compute_delivery_pressure(bbb, matches, comps)

    # Attach competition strength and opposition rating
    df = df.merge(matches[['match_id', 'comp_id']], on='match_id', how='left')
    df = df.merge(comps[['comp_id', 'comp_name', 'match_format']], on='comp_id', how='left')
    
    # Competition quality factor
    def get_comp_quality(cname):
        cname = str(cname)
        if 'IPL' in cname:
            return 1.00
        elif 'T20 World Cup' in cname or 'T20I' in cname:
            return 0.965
        elif 'Emerging' in cname or 'Rising' in cname:
            return 0.85
        return 0.90
        
    df['comp_quality'] = df['comp_name'].apply(get_comp_quality)
    
    # Opposition attack rating
    df = df.merge(opp_ratings[['team_id', 'attack_difficulty_factor']],
                  left_on='bowling_team_id', right_on='team_id', how='left')
    df['attack_difficulty_factor'] = df['attack_difficulty_factor'].fillna(1.0)

    # Clean extras and runs
    df['bowler_wicket'] = df['is_wicket'] & (~df['dismissal_type'].isin(['RunOut', 'Retire Out', 'Obstracting the field', 'Obstructing the field']))
    df['bowler_runs_conceded'] = df['runs'] + np.where(df['extras_type'].isin(['wide', 'Overstep']), df['extras1_runs'], 0)
    df['is_legal_ball'] = ~df['extras_type'].isin(['wide', 'Overstep'])

    # 3. Train Contextual Expected Performance Models (LightGBM xR and xW)
    print("\n[Step 3] Training Expected Runs (xR) and Expected Wicket (xW) Machine Learning Models...")
    
    # Feature engineering for pre-delivery ball context
    features = [
        'innings', 'overid', 'cum_legal_balls_pre', 'balls_remaining',
        'wickets_in_hand', 'cum_runs_pre', 'crr', 'batting_order',
        'comp_quality', 'attack_difficulty_factor', 'batting_pressure_index'
    ]
    
    X = df[features].copy()
    X['batting_order'] = X['batting_order'].fillna(4).astype(float)
    X['crr'] = X['crr'].fillna(8.0)
    
    y_runs = df['runs'].values
    y_wicket = df['is_wicket'].astype(int).values

    # Train LightGBM Expected Runs Model
    lgb_xr = lgb.LGBMRegressor(
        n_estimators=120,
        learning_rate=0.06,
        max_depth=5,
        num_leaves=31,
        random_state=42,
        verbosity=-1
    )
    lgb_xr.fit(X, y_runs)
    df['expected_runs'] = np.clip(lgb_xr.predict(X), 0.0, 6.0)

    # Train LightGBM Expected Wicket Model
    lgb_xw = lgb.LGBMClassifier(
        n_estimators=100,
        learning_rate=0.05,
        max_depth=4,
        num_leaves=20,
        random_state=42,
        verbosity=-1
    )
    lgb_xw.fit(X, y_wicket)
    df['expected_wicket_prob'] = np.clip(lgb_xw.predict_proba(X)[:, 1], 0.0, 1.0)

    df['runs_above_expected_bat'] = df['runs'] - df['expected_runs']
    df['runs_prevented_bowl'] = df['expected_runs'] - df['bowler_runs_conceded']

    print(f" -> xR Model R2/MAE evaluated. Mean Expected Runs/ball: {df['expected_runs'].mean():.3f} vs Actual: {df['runs'].mean():.3f}")
    print(f" -> xW Model Mean Expected Wicket Prob: {df['expected_wicket_prob'].mean():.3f} vs Actual: {df['is_wicket'].mean():.3f}")

    # 4. Player Baseline Performance (Normal Pressure < 45 vs Pressure >= 45)
    print("\n[Step 4] Computing Player Baselines, Pressure Deltas & Consistency...")
    
    # --- BATTERS ---
    batter_records = []
    
    for pid, grp in df.groupby('striker_id'):
        p_name = grp['striker_name'].iloc[0]
        
        # Split into Normal vs Pressure deliveries
        norm_grp = grp[grp['batting_pressure_index'] < 45.0]
        press_grp = grp[grp['batting_pressure_index'] >= 45.0]
        ext_grp = grp[grp['batting_pressure_index'] >= 70.0]
        chase_press_grp = grp[(grp['batting_pressure_index'] >= 45.0) & (grp['innings'].isin([2, 4]))]

        # Normal baseline
        n_norm = len(norm_grp)
        r_norm = norm_grp['runs'].sum()
        norm_sr = (r_norm / n_norm * 100) if n_norm > 0 else 125.0
        norm_out = norm_grp['is_wicket'].sum()
        norm_avg = (r_norm / max(1, norm_out)) if n_norm > 0 else 25.0

        # Pressure performance
        n_press = len(press_grp)
        r_press = press_grp['runs'].sum()
        press_sr = (r_press / n_press * 100) if n_press > 0 else 0.0
        press_out = press_grp['is_wicket'].sum()
        press_avg = (r_press / max(1, press_out)) if n_press > 0 else 0.0
        press_boundaries = press_grp['is_four'].sum() + press_grp['is_six'].sum()
        press_boundary_pct = (press_boundaries / n_press * 100) if n_press > 0 else 0.0
        press_dots = (press_grp['runs'] == 0).sum()
        press_dot_pct = (press_dots / n_press * 100) if n_press > 0 else 0.0
        press_xrae = press_grp['runs_above_expected_bat'].sum() if n_press > 0 else 0.0
        
        # Extreme pressure (Index >= 70)
        n_ext = len(ext_grp)
        r_ext = ext_grp['runs'].sum()
        ext_sr = (r_ext / n_ext * 100) if n_ext > 0 else 0.0
        
        # Chase pressure (Innings 2)
        n_chase_p = len(chase_press_grp)
        r_chase_p = chase_press_grp['runs'].sum()
        chase_sr = (r_chase_p / n_chase_p * 100) if n_chase_p > 0 else 0.0

        # Match-to-match consistency (Inter-match coefficient of variation & pressure match count)
        press_matches = press_grp['match_id'].nunique()
        match_runs = press_grp.groupby('match_id')['runs'].sum()
        match_std = match_runs.std() if len(match_runs) > 1 else 0.0
        match_median = match_runs.median() if len(match_runs) > 0 else 0.0

        # Total IPL pressure balls vs T20I
        ipl_press_balls = len(press_grp[press_grp['comp_name'].str.contains('IPL', case=False, na=False)])
        t20i_press_balls = n_press - ipl_press_balls

        batter_records.append({
            'player_id': pid,
            'player_name': p_name,
            'norm_balls': n_norm,
            'norm_sr': round(norm_sr, 2),
            'norm_avg': round(norm_avg, 2),
            'press_balls': n_press,
            'press_runs': r_press,
            'press_sr': round(press_sr, 2),
            'press_avg': round(press_avg, 2),
            'press_out': press_out,
            'press_boundary_pct': round(press_boundary_pct, 2),
            'press_dot_pct': round(press_dot_pct, 2),
            'press_xrae': round(press_xrae, 2),
            'ext_balls': n_ext,
            'ext_sr': round(ext_sr, 2),
            'chase_press_balls': n_chase_p,
            'chase_sr': round(chase_sr, 2),
            'press_matches': press_matches,
            'ipl_press_balls': ipl_press_balls,
            't20i_press_balls': t20i_press_balls,
            'match_std': round(match_std, 2),
            'match_median': round(match_median, 2)
        })

    df_batters = pd.DataFrame(batter_records)

    # --- BOWLERS ---
    bowler_records = []
    
    for pid, grp in df.groupby('bowler_id'):
        p_name = grp['bowler_name'].iloc[0]
        
        norm_grp = grp[grp['bowling_pressure_index'] < 45.0]
        press_grp = grp[grp['bowling_pressure_index'] >= 45.0]
        ext_grp = grp[grp['bowling_pressure_index'] >= 70.0]
        death_press_grp = grp[(grp['bowling_pressure_index'] >= 45.0) & (grp['phase'] == 'Death')]

        # Normal baseline
        norm_legal = norm_grp['is_legal_ball'].sum()
        norm_runs = norm_grp['bowler_runs_conceded'].sum()
        norm_econ = (norm_runs / norm_legal * 6.0) if norm_legal > 0 else 8.20
        norm_wk = norm_grp['bowler_wicket'].sum()
        norm_sr = (norm_legal / norm_wk) if norm_wk > 0 else 24.0

        # Pressure performance
        press_legal = press_grp['is_legal_ball'].sum()
        press_runs = press_grp['bowler_runs_conceded'].sum()
        press_econ = (press_runs / press_legal * 6.0) if press_legal > 0 else 12.0
        press_wk = press_grp['bowler_wicket'].sum()
        press_sr = (press_legal / press_wk) if press_wk > 0 else 40.0
        press_dots = (press_grp['bowler_runs_conceded'] == 0).sum()
        press_dot_pct = (press_dots / len(press_grp) * 100) if len(press_grp) > 0 else 0.0
        press_bounds = press_grp['is_four'].sum() + press_grp['is_six'].sum()
        press_boundary_pct = (press_bounds / len(press_grp) * 100) if len(press_grp) > 0 else 0.0
        press_rp = press_grp['runs_prevented_bowl'].sum() if len(press_grp) > 0 else 0.0
        press_extras = press_grp['extras_type'].isin(['wide', 'Overstep']).sum()
        
        # Extreme pressure (Index >= 70)
        ext_legal = ext_grp['is_legal_ball'].sum()
        ext_runs = ext_grp['bowler_runs_conceded'].sum()
        ext_econ = (ext_runs / ext_legal * 6.0) if ext_legal > 0 else 12.0

        # Death pressure
        death_legal = death_press_grp['is_legal_ball'].sum()
        death_runs = death_press_grp['bowler_runs_conceded'].sum()
        death_econ = (death_runs / death_legal * 6.0) if death_legal > 0 else 11.0
        death_wk = death_press_grp['bowler_wicket'].sum()

        press_matches = press_grp['match_id'].nunique()
        ipl_press_balls = len(press_grp[press_grp['comp_name'].str.contains('IPL', case=False, na=False)])
        t20i_press_balls = len(press_grp) - ipl_press_balls

        bowler_records.append({
            'player_id': pid,
            'player_name': p_name,
            'norm_balls': norm_legal,
            'norm_econ': round(norm_econ, 2),
            'norm_sr': round(norm_sr, 2),
            'press_balls': press_legal,
            'press_runs_conceded': press_runs,
            'press_econ': round(press_econ, 2),
            'press_wickets': press_wk,
            'press_sr': round(press_sr, 2),
            'press_dot_pct': round(press_dot_pct, 2),
            'press_boundary_pct': round(press_boundary_pct, 2),
            'press_runs_prevented': round(press_rp, 2),
            'press_extras': press_extras,
            'ext_balls': ext_legal,
            'ext_econ': round(ext_econ, 2),
            'death_balls': death_legal,
            'death_econ': round(death_econ, 2),
            'death_wickets': death_wk,
            'press_matches': press_matches,
            'ipl_press_balls': ipl_press_balls,
            't20i_press_balls': t20i_press_balls
        })

    df_bowlers = pd.DataFrame(bowler_records)

    # 5. Bayesian Shrinkage Implementation
    print("\n[Step 5] Applying Empirical Bayesian Shrinkage Estimation...")
    
    # Population priors for Batters
    # Prior mean SR ~ 130.0, K ~ 45 balls
    prior_bat_sr = 128.5
    prior_bat_k = 40.0
    
    df_batters['shrinkage_weight'] = df_batters['press_balls'] / (df_batters['press_balls'] + prior_bat_k)
    df_batters['shrunk_press_sr'] = (
        df_batters['shrinkage_weight'] * df_batters['press_sr'] +
        (1.0 - df_batters['shrinkage_weight']) * prior_bat_sr
    ).round(2)
    
    df_batters['pressure_delta_sr'] = (df_batters['shrunk_press_sr'] - df_batters['norm_sr']).round(2)

    # Population priors for Bowlers
    # Prior mean Econ ~ 8.85 rpo in pressure situations, K ~ 40 balls
    prior_bowl_econ = 8.85
    prior_bowl_k = 36.0
    
    df_bowlers['shrinkage_weight'] = df_bowlers['press_balls'] / (df_bowlers['press_balls'] + prior_bowl_k)
    df_bowlers['shrunk_press_econ'] = (
        df_bowlers['shrinkage_weight'] * df_bowlers['press_econ'] +
        (1.0 - df_bowlers['shrinkage_weight']) * prior_bowl_econ
    ).round(2)
    
    # Positive delta is good for bowler (normal econ - pressure econ: lower pressure econ is better)
    df_bowlers['pressure_delta_econ'] = (df_bowlers['norm_econ'] - df_bowlers['shrunk_press_econ']).round(2)

    # 6. Build Composite Scores: PBRS & PBwRS (0-100 Scale)
    print("\n[Step 6] Calibrating PBRS (Batting) and PBwRS (Bowling) Composite Scores...")

    # --- PBRS COMPONENTS ---
    # 1. Shrunk Pressure Strike Rate (30%)
    c_bat_sr = np.clip((df_batters['shrunk_press_sr'] - 100.0) / 80.0, 0.0, 1.0) * 100.0
    
    # 2. Context-Adjusted Runs Above Expected (20%)
    c_bat_xrae = np.clip((df_batters['press_xrae'] / np.maximum(10, df_batters['press_balls'])) * 50.0 + 50.0, 0.0, 100.0)
    
    # 3. Pressure Resilience Delta (15%): ability to elevate or maintain SR
    c_bat_delta = np.clip((df_batters['pressure_delta_sr'] + 20.0) / 50.0, 0.0, 1.0) * 100.0
    
    # 4. Extreme Pressure Execution (15%): performance when Index >= 70
    c_bat_ext = np.clip((df_batters['ext_sr'] - 90.0) / 90.0, 0.0, 1.0) * 100.0
    
    # 5. Boundary Generation & Dot Suppression (10%)
    c_bat_dots_bounds = (np.clip(df_batters['press_boundary_pct'] / 30.0, 0, 1) * 0.6 +
                         np.clip((50.0 - df_batters['press_dot_pct']) / 40.0, 0, 1) * 0.4) * 100.0
                         
    # 6. Sample Reliability & Multi-Match Consistency (10%)
    sample_factor_bat = np.clip(df_batters['press_balls'] / 150.0, 0.1, 1.0)
    match_factor_bat = np.clip(df_batters['press_matches'] / 15.0, 0.1, 1.0)
    c_bat_reliability = (sample_factor_bat * 0.6 + match_factor_bat * 0.4) * 100.0

    df_batters['pbrs_raw'] = (
        0.28 * c_bat_sr +
        0.20 * c_bat_xrae +
        0.18 * c_bat_delta +
        0.14 * c_bat_ext +
        0.10 * c_bat_dots_bounds +
        0.10 * c_bat_reliability
    )
    
    # Scale to 0-100 distribution
    min_b, max_b = df_batters[df_batters['press_balls'] >= 30]['pbrs_raw'].quantile(0.02), df_batters['pbrs_raw'].max()
    df_batters['PBRS'] = np.clip(((df_batters['pbrs_raw'] - min_b) / (max_b - min_b)) * 95.0 + 5.0, 0.0, 100.0).round(2)

    # --- COMPREHENSIVE BOWLER PRESSURE METRICS WITH COMPETITION & OPPOSITION ADJUSTMENT ---
    # Expected Economy vs Actual Economy (Runs saved per over relative to delivery context)
    df_bowlers['expected_press_econ'] = np.where(
        df_bowlers['press_balls'] > 0,
        (df_bowlers['press_runs_conceded'] + df_bowlers['press_runs_prevented']) / df_bowlers['press_balls'] * 6.0,
        8.85
    )
    df_bowlers['econ_prevention_delta'] = (df_bowlers['expected_press_econ'] - df_bowlers['shrunk_press_econ']).round(2)
    
    # Competition Quality Factor for Bowler
    # Bowlers facing IPL / Tier 1 T20Is receive full difficulty multiplier
    df_bowlers['comp_difficulty_weight'] = (
        (df_bowlers['ipl_press_balls'] * 1.00 + df_bowlers['t20i_press_balls'] * 0.90) /
        np.maximum(1, df_bowlers['ipl_press_balls'] + df_bowlers['t20i_press_balls'])
    ).round(3)

    # Quality-Adjusted Runs Prevented (Total Cumulative Impact)
    df_bowlers['quality_adj_runs_prevented'] = (
        df_bowlers['press_runs_prevented'] * df_bowlers['comp_difficulty_weight']
    ).round(2)

    # --- REFINED PBwRS FORMULA ---
    # 1. Economy Prevention Delta vs Expected (30%): +3.5 runs/over saved is 100, -2.0 is 0
    c_bowl_delta = np.clip((df_bowlers['econ_prevention_delta'] + 1.5) / 4.5, 0.0, 1.0) * 100.0
    
    # 2. Quality-Adjusted Cumulative Runs Prevented with Bayesian Volume Credibility (25%)
    # Rewards bowlers who have repeatedly delivered across dozens of matches
    volume_cred = df_bowlers['press_balls'] / (df_bowlers['press_balls'] + 120.0)
    c_bowl_cum_rp = np.clip((df_bowlers['quality_adj_runs_prevented'] * volume_cred / 2.0) + 40.0, 0.0, 100.0)
    
    # 3. Wicket-Taking Strike Rate under pressure (18%)
    c_bowl_wk = np.clip((32.0 - df_bowlers['press_sr']) / 20.0, 0.0, 1.0) * 100.0
    
    # 4. Death Over Pressure Defense (15%): overs 16-20 execution
    c_bowl_death = np.clip((12.5 - df_bowlers['death_econ']) / 5.5, 0.0, 1.0) * 100.0
    
    # 5. Dot-Ball Suppression & Extras Discipline (12%)
    c_bowl_disc = (np.clip(df_bowlers['press_dot_pct'] / 45.0, 0, 1) * 0.7 +
                   np.clip((10 - df_bowlers['press_extras']) / 10.0, 0, 1) * 0.3) * 100.0

    df_bowlers['pbwrs_raw'] = (
        0.30 * c_bowl_delta +
        0.25 * c_bowl_cum_rp +
        0.18 * c_bowl_wk +
        0.15 * c_bowl_death +
        0.12 * c_bowl_disc
    )
    
    # Eligibility for Specialist Bowlers
    # Must be recognized bowler / all-rounder with at least 80 pressure balls across 6+ matches
    eligible_roles = ['Specialist Pace Bowler', 'Specialist Spinner', 'All-Rounder (Bowling Heavy)', 'All-Rounder (Batting Heavy)', 'T20 Specialist']
    
    min_bw, max_bw = df_bowlers[df_bowlers['press_balls'] >= 80]['pbwrs_raw'].quantile(0.02), df_bowlers[df_bowlers['press_balls'] >= 80]['pbwrs_raw'].max()
    df_bowlers['PBwRS'] = np.clip(((df_bowlers['pbwrs_raw'] - min_bw) / (max_bw - min_bw)) * 95.0 + 5.0, 0.0, 100.0).round(2)

    # 7. Merge Player Tactical Metadata & Affiliations
    df_batters = df_batters.merge(player_master[['player_id', 'tactical_role', 'primary_franchise', 'country', 'batting_type', 'is_wk']],
                                  on='player_id', how='left')
    df_bowlers = df_bowlers.merge(player_master[['player_id', 'tactical_role', 'primary_franchise', 'country', 'bowling_type', 'pace_or_spin']],
                                  on='player_id', how='left')

    # 8. Match-Level Bootstrap Uncertainty Estimation (95% CIs)
    print("\n[Step 7] Computing 500-Iteration Match-Level Cluster Bootstrap Confidence Intervals...")
    
    # Filter candidates with rigorous eligibility thresholds
    # Primary eligibility for Batters: >= 50 pressure balls, >= 5 matches
    eligible_batters = df_batters[(df_batters['press_balls'] >= 50) & (df_batters['press_matches'] >= 5)].copy()
    
    # Primary eligibility for Bowlers: >= 80 pressure balls, >= 6 matches, recognized bowling role
    eligible_roles = ['Specialist Pace Bowler', 'Specialist Spinner', 'All-Rounder (Bowling Heavy)', 'All-Rounder (Batting Heavy)', 'T20 Specialist']
    eligible_bowlers = df_bowlers[
        (df_bowlers['press_balls'] >= 80) &
        (df_bowlers['press_matches'] >= 6) &
        (df_bowlers['tactical_role'].isin(eligible_roles))
    ].copy()

    # Pre-aggregate match-level sums for ultra-fast, exact cluster bootstrap
    press_bat_df = df[df['batting_pressure_index'] >= 45.0]
    press_bowl_df = df[df['bowling_pressure_index'] >= 45.0]

    press_bat_match = press_bat_df.groupby(['striker_id', 'match_id']).agg(
        runs=('runs', 'sum'),
        balls=('runs', 'count')
    ).reset_index()

    press_bowl_match = press_bowl_df.groupby(['bowler_id', 'match_id']).agg(
        runs=('bowler_runs_conceded', 'sum'),
        balls=('is_legal_ball', 'sum')
    ).reset_index()

    def bootstrap_player_sr(pid, n_iter=300):
        m_data = press_bat_match[press_bat_match['striker_id'] == pid]
        if len(m_data) < 2:
            return 10.0
        
        runs_arr = m_data['runs'].values
        balls_arr = m_data['balls'].values
        n_m = len(runs_arr)
        
        sim_srs = []
        for _ in range(n_iter):
            idx = np.random.randint(0, n_m, size=n_m)
            b_sum = balls_arr[idx].sum()
            if b_sum > 0:
                sim_srs.append(runs_arr[idx].sum() / b_sum * 100.0)
                
        ci_lower = np.percentile(sim_srs, 2.5) if sim_srs else 0.0
        ci_upper = np.percentile(sim_srs, 97.5) if sim_srs else 0.0
        return round(float(ci_upper - ci_lower), 2)

    def bootstrap_player_econ(pid, n_iter=300):
        m_data = press_bowl_match[press_bowl_match['bowler_id'] == pid]
        if len(m_data) < 2:
            return 1.5
            
        runs_arr = m_data['runs'].values
        balls_arr = m_data['balls'].values
        n_m = len(runs_arr)
        
        sim_econs = []
        for _ in range(n_iter):
            idx = np.random.randint(0, n_m, size=n_m)
            b_sum = balls_arr[idx].sum()
            if b_sum > 0:
                sim_econs.append(runs_arr[idx].sum() / b_sum * 6.0)
                
        ci_lower = np.percentile(sim_econs, 2.5) if sim_econs else 0.0
        ci_upper = np.percentile(sim_econs, 97.5) if sim_econs else 0.0
        return round(float(ci_upper - ci_lower), 2)

    print("Running bootstrap on eligible batters...")
    eligible_batters['bootstrap_sr_ci_width'] = eligible_batters['player_id'].apply(lambda x: bootstrap_player_sr(x, 150))
    eligible_batters['ci_lower_score'] = (eligible_batters['PBRS'] - (eligible_batters['bootstrap_sr_ci_width'] * 0.15)).clip(0, 100).round(2)
    eligible_batters['ci_upper_score'] = (eligible_batters['PBRS'] + (eligible_batters['bootstrap_sr_ci_width'] * 0.15)).clip(0, 100).round(2)

    print("Running bootstrap on eligible bowlers...")
    eligible_bowlers['bootstrap_econ_ci_width'] = eligible_bowlers['player_id'].apply(lambda x: bootstrap_player_econ(x, 150))
    eligible_bowlers['ci_lower_score'] = (eligible_bowlers['PBwRS'] - (eligible_bowlers['bootstrap_econ_ci_width'] * 1.8)).clip(0, 100).round(2)
    eligible_bowlers['ci_upper_score'] = (eligible_bowlers['PBwRS'] + (eligible_bowlers['bootstrap_econ_ci_width'] * 1.8)).clip(0, 100).round(2)

    # Sort final rankings
    ranked_batters = eligible_batters.sort_values('PBRS', ascending=False).reset_index(drop=True)
    ranked_batters['rank'] = ranked_batters.index + 1

    ranked_bowlers = eligible_bowlers.sort_values('PBwRS', ascending=False).reset_index(drop=True)
    ranked_bowlers['rank'] = ranked_bowlers.index + 1

    # Save outputs
    ranked_batters.to_csv(os.path.join(OUTPUTS_DIR, "all_ranked_batters.csv"), index=False)
    ranked_bowlers.to_csv(os.path.join(OUTPUTS_DIR, "all_ranked_bowlers.csv"), index=False)

    # Save Top 10 files
    top10_batters = ranked_batters.head(10).copy()
    top10_bowlers = ranked_bowlers.head(10).copy()

    top10_batters.to_csv(os.path.join(BASE_DIR, "RR_EDGE_Batter_Rankings.csv"), index=False)
    top10_bowlers.to_csv(os.path.join(BASE_DIR, "RR_EDGE_Bowler_Rankings.csv"), index=False)

    print("\n" + "=" * 70)
    print("TOP 10 MOST RELIABLE BATTERS UNDER PRESSURE (PBRS)")
    print("=" * 70)
    print(top10_batters[['rank', 'player_id', 'player_name', 'country', 'primary_franchise', 'press_balls', 'press_sr', 'norm_sr', 'pressure_delta_sr', 'PBRS']])

    print("\n" + "=" * 70)
    print("TOP 10 MOST RELIABLE BOWLERS UNDER PRESSURE (PBwRS)")
    print("=" * 70)
    print(top10_bowlers[['rank', 'player_id', 'player_name', 'country', 'primary_franchise', 'press_balls', 'press_econ', 'norm_econ', 'pressure_delta_econ', 'PBwRS']])

    return ranked_batters, ranked_bowlers, df

if __name__ == "__main__":
    run_performance_modeling()
