"""
Generation of RR_EDGE_Player_Intelligence.csv
Project RR-EDGE: Global Cricket Pressure Intelligence & IPL 2027 Auction Optimization System
"""

import os
import pandas as pd
import numpy as np

BASE_DIR = r"C:\Users\PREMCHANDYADAV\Downloads\RR_Competition"

def generate_player_intelligence():
    print("Generating comprehensive RR_EDGE_Player_Intelligence.csv...")
    
    top_bat = pd.read_csv(os.path.join(BASE_DIR, "RR_EDGE_Batter_Rankings.csv"))
    top_bowl = pd.read_csv(os.path.join(BASE_DIR, "RR_EDGE_Bowler_Rankings.csv"))
    
    records = []
    
    # Process Batters
    for _, row in top_bat.iterrows():
        # Build comprehensive rationale
        rationale = (
            f"Exemplary pressure execution: elevated strike rate by +{row['pressure_delta_sr']} SR points "
            f"under pressure ({row['press_sr']} vs {row['norm_sr']} baseline) across {row['press_matches']} matches. "
            f"Delivered +{row['press_xrae']} runs above expected with {row['press_boundary_pct']}% boundary conversion "
            f"and exceptional extreme-pressure strike rate of {row['ext_sr']}."
        )
        
        records.append({
            'rank': int(row['rank']),
            'discipline': 'Batting',
            'player_id': int(row['player_id']),
            'player_name': row['player_name'],
            'country': row['country'],
            'primary_franchise': row['primary_franchise'],
            'tactical_role': row['tactical_role'],
            'style_or_stance': row['batting_type'],
            'reliability_score': float(row['PBRS']),
            'ci_lower_score': float(row['ci_lower_score']),
            'ci_upper_score': float(row['ci_upper_score']),
            'pressure_sample_balls': int(row['press_balls']),
            'pressure_matches': int(row['press_matches']),
            'ipl_pressure_balls': int(row['ipl_press_balls']),
            't20i_pressure_balls': int(row['t20i_press_balls']),
            'normal_baseline_metric': f"{row['norm_sr']} SR ({row['norm_avg']} Avg)",
            'pressure_performance_metric': f"{row['press_sr']} SR ({row['press_avg']} Avg)",
            'pressure_delta': f"+{row['pressure_delta_sr']} SR (shrunk)",
            'extreme_pressure_metric': f"{row['ext_sr']} SR ({row['ext_balls']} balls)",
            'context_adjusted_value': f"+{row['press_xrae']} xRAE",
            'dot_or_boundary_execution': f"{row['press_boundary_pct']}% Boundaries | {row['press_dot_pct']}% Dots",
            'consistency_rating': f"Med {row['match_median']} runs/m (Std {row['match_std']})",
            'selection_rationale': rationale
        })

    # Process Bowlers
    for _, row in top_bowl.iterrows():
        rationale = (
            f"Dominant defensive and wicket-taking execution: conceded only {row['press_econ']} rpo under pressure "
            f"across {row['press_matches']} matches ({row['press_balls']} pressure balls). "
            f"Prevented {row['press_runs_prevented']} runs above expected, taking {row['press_wickets']} pressure wickets "
            f"(SR {row['press_sr']}). Death overs economy of {row['death_econ']} rpo across {row['death_balls']} balls."
        )
        
        records.append({
            'rank': int(row['rank']),
            'discipline': 'Bowling',
            'player_id': int(row['player_id']),
            'player_name': row['player_name'],
            'country': row['country'],
            'primary_franchise': row['primary_franchise'],
            'tactical_role': row['tactical_role'],
            'style_or_stance': row['bowling_type'],
            'reliability_score': float(row['PBwRS']),
            'ci_lower_score': float(row['ci_lower_score']),
            'ci_upper_score': float(row['ci_upper_score']),
            'pressure_sample_balls': int(row['press_balls']),
            'pressure_matches': int(row['press_matches']),
            'ipl_pressure_balls': int(row['ipl_press_balls']),
            't20i_pressure_balls': int(row['t20i_press_balls']),
            'normal_baseline_metric': f"{row['norm_econ']} Econ ({row['norm_sr']} SR)",
            'pressure_performance_metric': f"{row['press_econ']} Econ ({row['press_sr']} SR)",
            'pressure_delta': f"{row['pressure_delta_econ']} Econ Delta",
            'extreme_pressure_metric': f"{row['ext_econ']} Econ ({row['ext_balls']} balls)",
            'context_adjusted_value': f"+{row['press_runs_prevented']} Runs Prevented",
            'dot_or_boundary_execution': f"{row['press_dot_pct']}% Dots | {row['press_boundary_pct']}% Boundaries",
            'consistency_rating': f"Death Econ: {row['death_econ']} ({row['death_wickets']} wk)",
            'selection_rationale': rationale
        })

    df_intel = pd.DataFrame(records)
    out_path = os.path.join(BASE_DIR, "RR_EDGE_Player_Intelligence.csv")
    df_intel.to_csv(out_path, index=False)
    print(f"Successfully generated RR_EDGE_Player_Intelligence.csv ({len(df_intel)} records).")

if __name__ == "__main__":
    generate_player_intelligence()
