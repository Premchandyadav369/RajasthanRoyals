"""
Generates 2 new 4K (3840x2160, 16:9) presentation visual assets
following PPT Image DESIGN.md principles:
1. pareto_frontier_plate.png: Concept visualization of Portfolio Pareto Frontier & Surplus Region
2. crisis_hazard_plate.png: Concept visualization of Bayesian Hazard Survival & Domino Interruption
"""

import os
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, Circle, Polygon, FancyBboxPatch
import matplotlib.patheffects as pe

BASE_DIR = r"C:\Users\PREMCHANDYADAV\Downloads\RR_Competition"
ASSETS_DIR = os.path.join(BASE_DIR, "slide_assets")
os.makedirs(ASSETS_DIR, exist_ok=True)

W_INCH, H_INCH = 16.0, 9.0
DPI = 240  # 3840 x 2160

# Palette
C_BG = "#0B132B"          # Ink Navy Anchor
C_SURFACE = "#131E3D"     # Graphite / Deep Surface
C_PINK = "#EA1A85"        # Rajasthan Royals Royal Pink
C_GOLD = "#D4AF37"        # Imperial Gold
C_WHITE = "#F8FAFC"       # Paper White
C_MUTED = "#64748B"       # Slate Support
C_ALERT = "#EF4444"       # Signal Red
C_SUCCESS = "#10B981"     # Emerald Green

def generate_pareto_frontier_plate():
    fig = plt.figure(figsize=(W_INCH, H_INCH), dpi=DPI, facecolor=C_BG)
    ax = fig.add_axes([0, 0, 1, 1])
    ax.set_facecolor(C_BG)
    ax.set_xlim(0, 16)
    ax.set_ylim(0, 9)
    ax.axis('off')

    # Background subtle radial atmospheric glow on right side (focal region)
    Y, X = np.ogrid[:2160, :3840]
    dist = np.sqrt((X - 3840 * 0.72)**2 + (Y - 2160 * 0.52)**2)
    max_d = np.sqrt((3840 * 0.72)**2 + (2160 * 0.52)**2)
    gradient = 1.0 - (dist / max_d) * 0.7
    gradient = np.clip(gradient, 0.2, 1.0)
    ax.imshow(gradient, extent=[0, 16, 0, 9], cmap="magma", alpha=0.15, aspect='auto', zorder=1)

    # Architectural coordinate grid on right (x: 7.5 to 14.8, y: 1.5 to 7.8)
    # Left 0 to 7 is clean text-safe space
    grid_x = np.linspace(7.5, 14.8, 8)
    grid_y = np.linspace(1.8, 7.8, 7)
    for gx in grid_x:
        ax.plot([gx, gx], [1.8, 7.8], color="#1E2D56", lw=0.8, alpha=0.5, zorder=2)
    for gy in grid_y:
        ax.plot([7.5, 14.8], [gy, gy], color="#1E2D56", lw=0.8, alpha=0.5, zorder=2)

    # Pareto Optimal Curve (Risk vs Win Shares / Net WAR)
    t = np.linspace(0, 1, 100)
    # Curve from lower-right (suboptimal high risk) to top-left (optimal low risk, high WAR)
    curve_x = 8.2 + 6.0 * (1 - t)**1.8
    curve_y = 2.4 + 5.0 * np.sin(t * np.pi / 2)
    
    # Shaded Surplus Region under curve
    poly_pts = np.vstack([np.column_stack([curve_x, curve_y]), [[14.2, 2.0], [8.2, 2.0]]])
    ax.add_patch(Polygon(poly_pts, facecolor=C_PINK, alpha=0.08, zorder=3))

    # Glow line for the frontier
    ax.plot(curve_x, curve_y, color=C_GOLD, lw=4, alpha=0.9, zorder=5)
    ax.plot(curve_x, curve_y, color=C_PINK, lw=8, alpha=0.25, zorder=4)

    # Portfolio Points
    # Optimal Portfolio B (Low Risk, High Return)
    pt_b_x, pt_b_y = 8.8, 7.1
    ax.plot([pt_b_x, pt_b_x], [1.8, pt_b_y], color=C_SUCCESS, lw=1.2, ls="--", alpha=0.7, zorder=6)
    ax.plot([7.5, pt_b_x], [pt_b_y, pt_b_y], color=C_SUCCESS, lw=1.2, ls="--", alpha=0.7, zorder=6)
    ax.scatter([pt_b_x], [pt_b_y], s=380, color=C_SUCCESS, edgecolors=C_WHITE, lw=2.5, zorder=7)
    ax.scatter([pt_b_x], [pt_b_y], s=900, color=C_SUCCESS, alpha=0.25, zorder=6)

    # Suboptimal Portfolio A (Winner's Curse Trap: High Risk, Low Return)
    pt_a_x, pt_a_y = 13.5, 3.8
    ax.plot([pt_a_x, pt_a_x], [1.8, pt_a_y], color=C_ALERT, lw=1.2, ls="--", alpha=0.7, zorder=6)
    ax.scatter([pt_a_x], [pt_a_y], s=300, color=C_ALERT, edgecolors=C_WHITE, lw=2, zorder=7)

    # Intermediate Portfolios C & D
    ax.scatter([11.2, 10.4], [5.2, 5.8], s=200, color=C_MUTED, edgecolors="#A8A29A", lw=1.5, zorder=7)

    out_path = os.path.join(ASSETS_DIR, "pareto_frontier_plate.png")
    fig.savefig(out_path, dpi=DPI, facecolor=C_BG, edgecolor='none')
    plt.close(fig)
    print(f"Generated: {out_path} ({os.path.getsize(out_path)} bytes)")

def generate_crisis_hazard_plate():
    fig = plt.figure(figsize=(W_INCH, H_INCH), dpi=DPI, facecolor=C_BG)
    ax = fig.add_axes([0, 0, 1, 1])
    ax.set_facecolor(C_BG)
    ax.set_xlim(0, 16)
    ax.set_ylim(0, 9)
    ax.axis('off')

    # Radial gradient glow on focal right region
    Y, X = np.ogrid[:2160, :3840]
    dist = np.sqrt((X - 3840 * 0.72)**2 + (Y - 2160 * 0.5)**2)
    max_d = np.sqrt((3840 * 0.72)**2 + (2160 * 0.5)**2)
    gradient = 1.0 - (dist / max_d) * 0.7
    gradient = np.clip(gradient, 0.2, 1.0)
    ax.imshow(gradient, extent=[0, 16, 0, 9], cmap="magma", alpha=0.15, aspect='auto', zorder=1)

    # Time axes / Match Over markers (Overs 1 to 20 across x: 7.5 to 14.8)
    ax.plot([7.5, 14.8], [2.0, 2.0], color="#1E2D56", lw=1.5, zorder=2)
    ax.plot([7.5, 7.5], [2.0, 7.8], color="#1E2D56", lw=1.5, zorder=2)

    overs = np.linspace(7.5, 14.8, 20)
    for ox in overs[::4]:
        ax.plot([ox, ox], [1.8, 2.0], color=C_MUTED, lw=1, zorder=2)

    # Curve 1: 2026 Structural Collapse (Steep drop in overs 7-11)
    x_overs = np.linspace(7.5, 14.8, 200)
    # Steep decline in overs 7-11 (corresponding to x: 9.6 to 11.2)
    y_2026 = 7.2 - 3.8 / (1 + np.exp(-(x_overs - 10.3) * 3.5)) - (x_overs - 7.5) * 0.15
    ax.plot(x_overs, y_2026, color=C_ALERT, lw=3.5, zorder=4)
    ax.plot(x_overs, y_2026, color=C_ALERT, lw=7.0, alpha=0.25, zorder=3)

    # Curve 2: 2027 RR-EDGE Stabilized Survival (Plateau via Henry + Suyash + Jurel + Jadeja)
    y_2027 = 7.3 - 1.2 / (1 + np.exp(-(x_overs - 10.3) * 1.5)) - (x_overs - 7.5) * 0.05
    ax.plot(x_overs, y_2027, color=C_SUCCESS, lw=4.0, zorder=5)
    ax.plot(x_overs, y_2027, color=C_GOLD, lw=8.0, alpha=0.25, zorder=3)

    # Shaded Stabilization Gain Region
    ax.fill_between(x_overs, y_2026, y_2027, color=C_SUCCESS, alpha=0.12, zorder=2)

    # Crisis Interruption Anchor Point (Overs 7-11 Chokehold)
    inter_x = 10.3
    inter_y = 6.6
    ax.scatter([inter_x], [inter_y], s=350, color=C_GOLD, edgecolors=C_WHITE, lw=2.5, zorder=7)
    ax.scatter([inter_x], [inter_y], s=800, color=C_GOLD, alpha=0.3, zorder=6)

    # Finishing Anchor Point (Overs 18-20 Jurel Icebox Finish)
    fin_x = 14.2
    fin_y = 6.2
    ax.scatter([fin_x], [fin_y], s=320, color=C_PINK, edgecolors=C_WHITE, lw=2, zorder=7)
    ax.scatter([fin_x], [fin_y], s=750, color=C_PINK, alpha=0.3, zorder=6)

    out_path = os.path.join(ASSETS_DIR, "crisis_hazard_plate.png")
    fig.savefig(out_path, dpi=DPI, facecolor=C_BG, edgecolor='none')
    plt.close(fig)
    print(f"Generated: {out_path} ({os.path.getsize(out_path)} bytes)")

if __name__ == "__main__":
    generate_pareto_frontier_plate()
    generate_crisis_hazard_plate()
