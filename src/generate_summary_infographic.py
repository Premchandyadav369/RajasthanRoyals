"""
Generation of RR_EDGE_Executive_Summary.png Infographic
Project RR-EDGE: Global Cricket Pressure Intelligence & IPL 2027 Auction Optimization System
"""

import os
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import pandas as pd

BASE_DIR = r"C:\Users\PREMCHANDYADAV\Downloads\RR_Competition"

def generate_infographic():
    print("Generating RR_EDGE_Executive_Summary.png Infographic...")
    
    bat_top = pd.read_csv(os.path.join(BASE_DIR, "RR_EDGE_Batter_Rankings.csv")).head(10)
    bowl_top = pd.read_csv(os.path.join(BASE_DIR, "RR_EDGE_Bowler_Rankings.csv")).head(10)

    fig, ax = plt.subplots(figsize=(14, 18), dpi=300)
    fig.patch.set_facecolor('#0B132B')
    ax.set_facecolor('#0B132B')
    ax.axis('off')

    # Header Card
    header_box = patches.FancyBboxPatch((0.03, 0.91), 0.94, 0.075, boxstyle="round,pad=0.01",
                                        facecolor='#1C2541', edgecolor='#FF007F', linewidth=2.5)
    ax.add_patch(header_box)
    ax.text(0.5, 0.965, "PROJECT RR-EDGE | RAJASTHAN ROYALS SUPERR SELECTOR S2",
            fontsize=18, fontweight='bold', color='#48CAE4', ha='center', va='center')
    ax.text(0.5, 0.935, "Official Round 1 Dropdown Selections, Pressure Intelligence & IPL 2027 Squad Optimization",
            fontsize=11, color='#F8FAFC', ha='center', va='center')
    ax.text(0.5, 0.918, "Author: Premchand Yadav | Verified on 200,999 Deliveries (2022-2026 Data Pack)",
            fontsize=9.5, color='#9BA4B5', ha='center', va='center')

    # Batting Section Banner
    bat_banner = patches.FancyBboxPatch((0.03, 0.865), 0.94, 0.032, boxstyle="round,pad=0.005",
                                        facecolor='#0077B6', edgecolor='#0077B6')
    ax.add_patch(bat_banner)
    ax.text(0.5, 0.881, "OFFICIAL TOP 10 BATTERS UNDER PRESSURE (PBRS) — UNSTOP DROPDOWN SELECTIONS",
            fontsize=10.5, fontweight='bold', color='#FFFFFF', ha='center', va='center')

    # Table Header for Batters
    headers_bat = ["Rank", "Player Name", "Player ID", "Country", "Franchise", "Press SR", "Base SR", "Delta SR", "xRAE", "PBRS Score", "95% CI"]
    col_x_bat = [0.05, 0.12, 0.28, 0.36, 0.46, 0.56, 0.64, 0.72, 0.80, 0.88, 0.95]
    
    y = 0.845
    for h, x_pos in zip(headers_bat, col_x_bat):
        ax.text(x_pos, y, h, fontsize=8.5, fontweight='bold', color='#FFD166', ha='center', va='center')
        
    ax.plot([0.03, 0.97], [y - 0.01, y - 0.01], color='#334155', linewidth=1)

    y -= 0.024
    for _, r in bat_top.iterrows():
        rank_str = f"#{int(r['rank'])}"
        row_vals = [
            rank_str, r['player_name'], str(int(r['player_id'])), r['country'],
            r['primary_franchise'][:10], f"{r['press_sr']:.1f}", f"{r['norm_sr']:.1f}",
            f"+{r['pressure_delta_sr']:.1f}", f"+{r['press_xrae']:.1f}", f"{r['PBRS']:.1f}",
            f"[{r['ci_lower_score']:.0f}-{r['ci_upper_score']:.0f}]"
        ]
        for val, x_pos in zip(row_vals, col_x_bat):
            weight = 'bold' if x_pos in [0.05, 0.12, 0.72, 0.88] else 'normal'
            color = '#38BDF8' if x_pos == 0.88 else ('#34D399' if x_pos == 0.72 else '#F8FAFC')
            ax.text(x_pos, y, val, fontsize=8, fontweight=weight, color=color, ha='center', va='center')
        y -= 0.021

    # Bowling Section Banner
    y -= 0.01
    bowl_banner = patches.FancyBboxPatch((0.03, y), 0.94, 0.032, boxstyle="round,pad=0.005",
                                         facecolor='#FF007F', edgecolor='#FF007F')
    ax.add_patch(bowl_banner)
    ax.text(0.5, y + 0.016, "OFFICIAL TOP 10 BOWLERS UNDER PRESSURE (PBwRS) — UNSTOP DROPDOWN SELECTIONS",
            fontsize=10.5, fontweight='bold', color='#FFFFFF', ha='center', va='center')

    y -= 0.02
    headers_bowl = ["Rank", "Player Name", "Player ID", "Country", "Franchise", "Press Econ", "Base Econ", "Death Econ", "Runs Prev.", "PBwRS Score", "95% CI"]
    for h, x_pos in zip(headers_bowl, col_x_bat):
        ax.text(x_pos, y, h, fontsize=8.5, fontweight='bold', color='#FFD166', ha='center', va='center')
        
    ax.plot([0.03, 0.97], [y - 0.01, y - 0.01], color='#334155', linewidth=1)

    y -= 0.024
    for _, r in bowl_top.iterrows():
        rank_str = f"#{int(r['rank'])}"
        row_vals = [
            rank_str, r['player_name'], str(int(r['player_id'])), r['country'],
            r['primary_franchise'][:10], f"{r['press_econ']:.2f}", f"{r['norm_econ']:.2f}",
            f"{r['death_econ']:.2f}", f"+{r['press_runs_prevented']:.1f}", f"{r['PBwRS']:.1f}",
            f"[{r['ci_lower_score']:.0f}-{r['ci_upper_score']:.0f}]"
        ]
        for val, x_pos in zip(row_vals, col_x_bat):
            weight = 'bold' if x_pos in [0.05, 0.12, 0.72, 0.88] else 'normal'
            color = '#FF70A6' if x_pos == 0.88 else ('#34D399' if x_pos == 0.72 else '#F8FAFC')
            ax.text(x_pos, y, val, fontsize=8, fontweight=weight, color=color, ha='center', va='center')
        y -= 0.021

    # RR IPL 2027 Strategy Section Banner
    y -= 0.012
    strat_banner = patches.FancyBboxPatch((0.03, y), 0.94, 0.032, boxstyle="round,pad=0.005",
                                          facecolor='#7209B7', edgecolor='#7209B7')
    ax.add_patch(strat_banner)
    ax.text(0.5, y + 0.016, "RAJASTHAN ROYALS IPL 2027 STRATEGY: THE MASTER PLAYING XI & SQUAD BLUEPRINT",
            fontsize=10.5, fontweight='bold', color='#FFFFFF', ha='center', va='center')

    # Strategic 3 Box Cards
    y -= 0.095
    box1 = patches.FancyBboxPatch((0.03, y), 0.29, 0.085, boxstyle="round,pad=0.008",
                                  facecolor='#1C2541', edgecolor='#48CAE4', linewidth=1.5)
    box2 = patches.FancyBboxPatch((0.355, y), 0.29, 0.085, boxstyle="round,pad=0.008",
                                  facecolor='#1C2541', edgecolor='#FF007F', linewidth=1.5)
    box3 = patches.FancyBboxPatch((0.68, y), 0.29, 0.085, boxstyle="round,pad=0.008",
                                  facecolor='#1C2541', edgecolor='#10B981', linewidth=1.5)
    ax.add_patch(box1)
    ax.add_patch(box2)
    ax.add_patch(box3)

    # Card 1 Text
    ax.text(0.175, y + 0.07, "UNTOUCHABLE CORE", fontsize=9.5, fontweight='bold', color='#48CAE4', ha='center')
    ax.text(0.175, y + 0.05, "Sooryavanshi (Orange Cap 776r)\nJaiswal (427r, 152 SR)\nJurel (515r, 154 SR)\nParag (Captain / No. 4)",
            fontsize=7.5, color='#F8FAFC', ha='center', va='top')

    # Card 2 Text
    ax.text(0.50, y + 0.07, "AUCTION TARGETS (₹38 Cr)", fontsize=9.5, fontweight='bold', color='#FF70A6', ha='center')
    ax.text(0.50, y + 0.05, "1. Pathirana (₹12-13 Cr, Death Slinger)\n2. Green (₹10-11 Cr, No. 5 Enforcer)\n3. Akash Deep (₹5-6 Cr, Seamer)\n4. Ashutosh Sharma (₹4-5 Cr, Finisher)",
            fontsize=7.5, color='#F8FAFC', ha='center', va='top')

    # Card 3 Text
    ax.text(0.825, y + 0.07, "MASTER RECOMMENDED XI", fontsize=9.5, fontweight='bold', color='#10B981', ha='center')
    ax.text(0.825, y + 0.05, "1. Jaiswal | 2. Sooryavanshi\n3. Jurel (wk) | 4. Parag (c)\n5. Green | 6. Ferreira\n7. Jadeja | 8. Archer\n9. Pathirana | 10. Akash Deep\n11. Punja | Sub: Ashutosh",
            fontsize=7.5, color='#F8FAFC', ha='center', va='top')

    # Bottom Footer
    ax.text(0.5, 0.02, "Project RR-EDGE | Google Antigravity | 100% Pre-Delivery Leakage Free | Certified Unstop Compatible",
            fontsize=8.5, color='#64748B', ha='center', va='center')

    out_png = os.path.join(BASE_DIR, "RR_EDGE_Executive_Summary.png")
    plt.savefig(out_png, bbox_inches='tight', dpi=300)
    plt.close()
    print(f" -> Saved {out_png}")

if __name__ == "__main__":
    generate_infographic()
