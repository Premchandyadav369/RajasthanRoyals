"""
High-Resolution Chart Generation for Project RR-EDGE Reports & Dashboard
Project RR-EDGE: Global Cricket Pressure Intelligence & IPL 2027 Auction Optimization System
"""

import os
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

BASE_DIR = r"C:\Users\PREMCHANDYADAV\Downloads\RR_Competition"
CHARTS_DIR = os.path.join(BASE_DIR, "charts")
os.makedirs(CHARTS_DIR, exist_ok=True)

def generate_all_charts():
    print("Generating high-resolution publication charts...")
    
    bat_top = pd.read_csv(os.path.join(BASE_DIR, "RR_EDGE_Batter_Rankings.csv"))
    bowl_top = pd.read_csv(os.path.join(BASE_DIR, "RR_EDGE_Bowler_Rankings.csv"))
    
    # --- CHART 1: BATTING SCATTER (Normal vs Pressure SR) ---
    fig, ax = plt.subplots(figsize=(8, 6), dpi=300)
    fig.patch.set_facecolor('#0B132B')
    ax.set_facecolor('#1C2541')
    
    x = bat_top['norm_sr']
    y = bat_top['press_sr']
    sizes = bat_top['press_balls'] * 1.2
    colors_arr = bat_top['PBRS']
    
    scatter = ax.scatter(x, y, s=sizes, c=colors_arr, cmap='plasma', alpha=0.85, edgecolors='#48CAE4', linewidths=1.5)
    
    # 1:1 Diagonal
    ax.plot([90, 185], [90, 185], '--', color='#9BA4B5', alpha=0.7, label='Zero Resilience Baseline (1:1)')
    
    for _, row in bat_top.iterrows():
        ax.annotate(row['player_name'], (row['norm_sr'] + 1.2, row['press_sr'] + 0.8),
                    color='#F8FAFC', fontsize=8.5, fontweight='bold')
                    
    ax.set_title("RR-EDGE: Normal Strike Rate vs Pressure Strike Rate (Top 10 Batters)", fontsize=11, fontweight='bold', color='#48CAE4', pad=12)
    ax.set_xlabel("Normal Baseline Strike Rate (<45 Pressure Index)", fontsize=9.5, color='#E0E6ED')
    ax.set_ylabel("Pressure Strike Rate (≥45 Pressure Index)", fontsize=9.5, color='#E0E6ED')
    ax.tick_params(colors='#E0E6ED', labelsize=8.5)
    ax.grid(True, linestyle=':', alpha=0.3, color='#9BA4B5')
    
    cbar = plt.colorbar(scatter, ax=ax)
    cbar.set_label('Pressure Batting Reliability Score (PBRS)', color='#E0E6ED', fontsize=8.5)
    cbar.ax.tick_params(colors='#E0E6ED', labelsize=8)
    
    c1_path = os.path.join(CHARTS_DIR, "figure1_batting_scatter.png")
    plt.savefig(c1_path, bbox_inches='tight', dpi=300)
    plt.close()
    print(f" -> Saved {c1_path}")

    # --- CHART 2: BOWLER QUADRANT (Pressure Econ vs Runs Prevented) ---
    fig, ax = plt.subplots(figsize=(8, 6), dpi=300)
    fig.patch.set_facecolor('#0B132B')
    ax.set_facecolor('#1C2541')
    
    xb = bowl_top['press_econ']
    yb = bowl_top['press_runs_prevented']
    sizes_b = bowl_top['press_balls'] * 0.9
    colors_b = bowl_top['PBwRS']
    
    scatter_b = ax.scatter(xb, yb, s=sizes_b, c=colors_b, cmap='viridis', alpha=0.85, edgecolors='#FF007F', linewidths=1.5)
    
    for _, row in bowl_top.iterrows():
        ax.annotate(row['player_name'], (row['press_econ'] + 0.1, row['press_runs_prevented'] + 3),
                    color='#F8FAFC', fontsize=8.5, fontweight='bold')
                    
    ax.set_title("RR-EDGE: Pressure Economy vs Cumulative Runs Prevented (Top 10 Bowlers)", fontsize=11, fontweight='bold', color='#FF007F', pad=12)
    ax.set_xlabel("Pressure Economy Rate (rpo)", fontsize=9.5, color='#E0E6ED')
    ax.set_ylabel("Context Runs Prevented Above Expected (xRP)", fontsize=9.5, color='#E0E6ED')
    ax.tick_params(colors='#E0E6ED', labelsize=8.5)
    ax.grid(True, linestyle=':', alpha=0.3, color='#9BA4B5')
    
    cbar_b = plt.colorbar(scatter_b, ax=ax)
    cbar_b.set_label('Pressure Bowling Reliability Score (PBwRS)', color='#E0E6ED', fontsize=8.5)
    cbar_b.ax.tick_params(colors='#E0E6ED', labelsize=8)
    
    c2_path = os.path.join(CHARTS_DIR, "figure2_bowling_quadrant.png")
    plt.savefig(c2_path, bbox_inches='tight', dpi=300)
    plt.close()
    print(f" -> Saved {c2_path}")

    # --- CHART 3: RADAR CHART (RR 2026 Bowling vs RR 2027 Projected) ---
    fig = plt.figure(figsize=(7, 7), dpi=300)
    fig.patch.set_facecolor('#0B132B')
    ax = fig.add_subplot(111, polar=True)
    ax.set_facecolor('#1C2541')

    categories = ['Powerplay (1-6)', 'Middle Overs (7-11)', 'Middle Overs (12-15)', 'Death Overs (16-20)', 'High Leverage (P≥70)']
    N = len(categories)
    angles = [n / float(N) * 2 * np.pi for n in range(N)]
    angles += angles[:1]

    # Inverted scale: lower economy is better, so plot (13.0 - Economy)
    # RR 2026 actual economy: PP 8.85, 7-11 9.71, 12-15 9.40, Death 11.85, P>=70 12.20
    rr_2026 = [13.0 - 8.85, 13.0 - 9.71, 13.0 - 9.40, 13.0 - 11.85, 13.0 - 12.20]
    rr_2026 += rr_2026[:1]

    # RR 2027 Projected with Pathirana + Akash Deep + Archer + Jadeja + Punja:
    # PP 7.20, 7-11 7.10, 12-15 7.45, Death 8.40, P>=70 8.80
    rr_2027 = [13.0 - 7.20, 13.0 - 7.10, 13.0 - 7.45, 13.0 - 8.40, 13.0 - 8.80]
    rr_2027 += rr_2027[:1]

    ax.plot(angles, rr_2026, 'o-', linewidth=2, color='#E63946', label='RR 2026 Baseline Attack')
    ax.fill(angles, rr_2026, alpha=0.25, color='#E63946')

    ax.plot(angles, rr_2027, 'o-', linewidth=2.5, color='#48CAE4', label='RR 2027 Optimized Attack')
    ax.fill(angles, rr_2027, alpha=0.35, color='#48CAE4')

    ax.set_xticks(angles[:-1])
    ax.set_xticklabels(categories, color='#F8FAFC', size=8.5, fontweight='bold')
    ax.set_yticklabels([])
    ax.grid(color='#9BA4B5', linestyle=':', alpha=0.5)
    
    plt.title("RR Bowling Phase Defensive Strength\n(Larger Polygon = Lower Economy / Better Containment)",
              size=11, color='#48CAE4', fontweight='bold', pad=15)
    plt.legend(loc='upper right', bbox_to_anchor=(1.25, 1.1), facecolor='#1C2541', edgecolor='#48CAE4', labelcolor='#F8FAFC', fontsize=8.5)
    
    c3_path = os.path.join(CHARTS_DIR, "figure3_squad_radar.png")
    plt.savefig(c3_path, bbox_inches='tight', dpi=300)
    plt.close()
    print(f" -> Saved {c3_path}")

    # --- CHART 4: MONTE CARLO PURSE ALLOCATION PIE ---
    fig, ax = plt.subplots(figsize=(7, 5), dpi=300)
    fig.patch.set_facecolor('#0B132B')
    ax.set_facecolor('#1C2541')

    labels = ['Matheesha Pathirana (Death Pacer)', 'Cameron Green (No. 5 Finisher)', 'Akash Deep (Indian Seamer)', 'Ashutosh Sharma (Clutch Batter)', 'Surplus Purse Reserve']
    sizes_pie = [13.06, 10.08, 5.59, 4.81, 4.46]
    colors_pie = ['#FF007F', '#3A86FF', '#48CAE4', '#F72585', '#10B981']

    wedges, texts, autotexts = ax.pie(
        sizes_pie, labels=labels, autopct='%1.1f%%', startangle=140,
        colors=colors_pie, textprops=dict(color='#F8FAFC', size=8.5),
        wedgeprops=dict(width=0.45, edgecolor='#0B132B', linewidth=1.5)
    )
    for at in autotexts:
        at.set_color('#FFFFFF')
        at.set_fontweight('bold')

    ax.set_title("Optimal ₹38.0 Cr Auction Purse Allocation\n(1,000 Monte Carlo Simulations)", fontsize=11, fontweight='bold', color='#48CAE4', pad=10)
    
    c4_path = os.path.join(CHARTS_DIR, "figure4_monte_carlo_budget.png")
    plt.savefig(c4_path, bbox_inches='tight', dpi=300)
    plt.close()
    print(f" -> Saved {c4_path}")

    print("All visual charts successfully created.")

if __name__ == "__main__":
    generate_all_charts()
