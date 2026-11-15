"""
Generates high-resolution (3840x2160, 16:9 4K) presentation visual assets
following PPT Image DESIGN.md principles:
- Editorial poster & structured visual essay aesthetic
- One dominant focal point with 25% to 35% clean text-safe space
- Minimal / zero baked-in text (room for editable PowerPoint layers)
- Restrained franchise palette: Ink Navy #0B132B, Royal Pink #EA1A85, Imperial Gold #D4AF37
- Zero 'AI slop', zero generic SaaS illustrations, zero noisy AI wallpaper
"""

import os
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, Circle, Arc, Polygon, FancyBboxPatch
import matplotlib.patheffects as pe

BASE_DIR = r"C:\Users\PREMCHANDYADAV\Downloads\RR_Competition"
ASSETS_DIR = os.path.join(BASE_DIR, "slide_assets")
os.makedirs(ASSETS_DIR, exist_ok=True)

# 16:9 4K dimensions
W_INCH, H_INCH = 16.0, 9.0
DPI = 240  # 3840 x 2160

# Palette
C_BG = "#0B132B"          # Ink Navy Anchor
C_SURFACE = "#131E3D"     # Graphite / Deep Surface
C_PINK = "#EA1A85"        # Rajasthan Royals Royal Pink
C_GOLD = "#D4AF37"        # Imperial Gold
C_WHITE = "#F8FAFC"       # Paper White
C_MUTED = "#64748B"       # Slate Support
C_ALERT = "#EF4444"       # Signal Red (for 2026 leakage)
C_SUCCESS = "#10B981"     # Emerald Green (for Plan B choke)

# -----------------------------------------------------------------------------
# ASSET 1: COVER HERO PLATE (Sawai Mansingh Stadium Pitch & Floodlight Geometry)
# -----------------------------------------------------------------------------
def generate_cover_hero_plate():
    fig = plt.figure(figsize=(W_INCH, H_INCH), dpi=DPI, facecolor=C_BG)
    ax = fig.add_axes([0, 0, 1, 1])
    ax.set_facecolor(C_BG)
    ax.set_xlim(0, 16)
    ax.set_ylim(0, 9)
    ax.axis('off')

    # Subtle radial atmospheric gradient in background
    Y, X = np.ogrid[:2160, :3840]
    dist_from_focal = np.sqrt((X - 3840 * 0.72)**2 + (Y - 2160 * 0.5)**2)
    max_d = np.sqrt((3840 * 0.72)**2 + (2160 * 0.5)**2)
    gradient = 1.0 - (dist_from_focal / max_d) * 0.65
    gradient = np.clip(gradient, 0.25, 1.0)
    
    # Base dark gradient background
    ax.imshow(gradient, extent=[0, 16, 0, 9], cmap="magma", alpha=0.18, aspect='auto', zorder=1)

    # Architectural Pitch Strip (Focal subject on right 65-85%, left is text-safe zone)
    # The 22-yard pitch angled in perspective
    pitch_pts = np.array([
        [9.5, 1.2],
        [13.8, 1.2],
        [12.6, 7.8],
        [10.2, 7.8]
    ])
    pitch = Polygon(pitch_pts, closed=True, facecolor="#9A7B4F", edgecolor=C_GOLD, linewidth=1.5, alpha=0.9, zorder=3)
    ax.add_patch(pitch)

    # Crease markings
    ax.plot([9.6, 13.7], [2.2, 2.2], color="#FFFFFF", linewidth=2.5, alpha=0.85, zorder=4)
    ax.plot([10.3, 12.5], [6.8, 6.8], color="#FFFFFF", linewidth=2.0, alpha=0.85, zorder=4)
    
    # Stumps at batting crease
    for x_s in [11.2, 11.45, 11.7]:
        ax.plot([x_s, x_s], [2.2, 2.9], color="#FFD700", linewidth=3.5, zorder=5)
    ax.plot([11.15, 11.75], [2.9, 2.9], color="#FFD700", linewidth=2.0, zorder=5)

    # Structural stadium floodlight rays illuminating from top-right
    for alpha, width in [(0.06, 3.5), (0.04, 5.0), (0.02, 7.0)]:
        cone_pts = np.array([[15.5, 9.0], [9.0, 0.0], [15.0, 0.0]])
        cone = Polygon(cone_pts, closed=True, facecolor=C_PINK, alpha=alpha, zorder=2)
        ax.add_patch(cone)

    # Left-Side Text-Safe Zone indicator line (Ultra subtle boundary)
    ax.plot([6.2, 6.2], [1.5, 7.5], color=C_SURFACE, linewidth=1.2, linestyle='--', alpha=0.4, zorder=2)

    # Minimal editorial plate watermark / label in corner
    ax.text(15.2, 0.6, "SMS STADIUM • JAIPUR FORTRESS", color=C_GOLD, fontsize=9,
            fontfamily='sans-serif', fontweight='bold', ha='right', va='center', alpha=0.7, zorder=6)

    out_path = os.path.join(ASSETS_DIR, "hero_cover_plate.png")
    fig.savefig(out_path, dpi=DPI, facecolor=C_BG)
    plt.close(fig)
    print(f"Generated: {out_path}")

# -----------------------------------------------------------------------------
# ASSET 2: COMPARISON PLATE (2026 Leakage vs 2027 Plan B Choke)
# -----------------------------------------------------------------------------
def generate_comparison_plate():
    fig = plt.figure(figsize=(W_INCH, H_INCH), dpi=DPI, facecolor=C_BG)
    ax = fig.add_axes([0, 0, 1, 1])
    ax.set_facecolor(C_BG)
    ax.set_xlim(0, 16)
    ax.set_ylim(0, 9)
    ax.axis('off')

    # Split Composition: Left Side (Red Tension / 2026 Leak) vs Right Side (Emerald Control / Plan B)
    # Background split
    left_bg = Rectangle((0, 0), 8, 9, facecolor="#140D18", zorder=1)
    right_bg = Rectangle((8, 0), 8, 9, facecolor="#09181B", zorder=1)
    ax.add_patch(left_bg)
    ax.add_patch(right_bg)

    # Central divider line with gold node
    ax.plot([8, 8], [1.0, 8.0], color=C_SURFACE, linewidth=2, zorder=2)
    ax.plot([8, 8], [4.5, 4.5], marker='o', markersize=8, color=C_GOLD, zorder=3)

    # Left: The 10.29 RPO Leakage Waveform (Jagged, uncontrolled, red alert)
    x_l = np.linspace(1.2, 7.2, 60)
    y_l = 4.5 + np.sin(x_l * 3.5) * 1.2 + np.random.RandomState(42).normal(0, 0.25, 60)
    ax.plot(x_l, y_l, color=C_ALERT, linewidth=3.5, alpha=0.9, zorder=4)
    ax.fill_between(x_l, 2.5, y_l, color=C_ALERT, alpha=0.12, zorder=3)

    # Left Annotation: Stat Callout inside visual asset
    ax.text(2.0, 7.2, "10.29 RPO", color=C_ALERT, fontsize=32, fontfamily='sans-serif', fontweight='heavy', zorder=5)
    ax.text(2.0, 6.5, "OVERS 7-11 LEAKAGE (2026 DEFICIT)", color="#FCA5A5", fontsize=10, fontfamily='sans-serif', fontweight='bold', zorder=5)

    # Right: The 7.82 RPO Choke Waveform (Damped, compressed, controlled green)
    x_r = np.linspace(8.8, 14.8, 60)
    y_r = 4.5 + np.sin(x_r * 2.0) * 0.45  # Controlled, flattened amplitude
    ax.plot(x_r, y_r, color=C_SUCCESS, linewidth=3.5, alpha=0.9, zorder=4)
    ax.fill_between(x_r, 2.5, y_r, color=C_SUCCESS, alpha=0.12, zorder=3)

    # Right Annotation: Stat Callout inside visual asset
    ax.text(9.6, 7.2, "7.82 RPO", color=C_SUCCESS, fontsize=32, fontfamily='sans-serif', fontweight='heavy', zorder=5)
    ax.text(9.6, 6.5, "PLAN B DEFENSIVE LOCKDOWN (SUYASH + JADEJA)", color="#86EFAC", fontsize=10, fontfamily='sans-serif', fontweight='bold', zorder=5)

    # Bottom metric delta tag
    ax.text(8.0, 1.8, "-38.5% PROBABILITY OF CONCEDING 200+ RUNS", color=C_GOLD,
            fontsize=12, fontfamily='sans-serif', fontweight='heavy', ha='center', zorder=5)

    out_path = os.path.join(ASSETS_DIR, "bottleneck_comparison_plate.png")
    fig.savefig(out_path, dpi=DPI, facecolor=C_BG)
    plt.close(fig)
    print(f"Generated: {out_path}")

# -----------------------------------------------------------------------------
# ASSET 3: PITCH PHYSICS & TRAJECTORY TELEMETRY PLATE
# -----------------------------------------------------------------------------
def generate_pitch_physics_plate():
    fig = plt.figure(figsize=(W_INCH, H_INCH), dpi=DPI, facecolor=C_BG)
    ax = fig.add_axes([0, 0, 1, 1])
    ax.set_facecolor(C_BG)
    ax.set_xlim(0, 16)
    ax.set_ylim(0, 9)
    ax.axis('off')

    # Ground line
    ax.plot([1.0, 15.0], [2.2, 2.2], color=C_SURFACE, linewidth=2.5, zorder=2)
    ax.text(1.2, 1.8, "PITCH SURFACE (22 YARDS)", color=C_MUTED, fontsize=9, fontfamily='sans-serif', fontweight='bold', zorder=3)

    # Batting Crease Stumps
    ax.plot([14.2, 14.2], [2.2, 4.0], color=C_GOLD, linewidth=4.0, zorder=3)
    ax.plot([14.1, 14.3], [4.0, 4.0], color=C_GOLD, linewidth=2.0, zorder=3)

    # Bowler 1 Trajectory: Jofra Archer 151 kph Express Bouncer (High release 2.14m -> Steep bounce to throat)
    t_arch = np.linspace(2.0, 14.0, 100)
    # Pitch impact at x=8.5
    y_arch = np.where(t_arch < 8.5,
                      6.2 - ((t_arch - 2.0)/6.5)**1.2 * 4.0,
                      2.2 + ((t_arch - 8.5)/5.5)**0.9 * 3.2)
    ax.plot(t_arch, y_arch, color=C_PINK, linewidth=3.5, label="Jofra Archer (151.4 kph Throat Bouncer)", zorder=4)
    ax.plot(8.5, 2.2, marker='o', markersize=9, color=C_PINK, zorder=5)

    # Bowler 2 Trajectory: Matt Henry 138 kph Upright Seam (Top of Off Stump Channel)
    t_henry = np.linspace(2.0, 14.2, 100)
    # Pitch impact at x=10.2 (Good length)
    y_henry = np.where(t_henry < 10.2,
                       5.6 - ((t_henry - 2.0)/8.2)**1.1 * 3.4,
                       2.2 + ((t_henry - 10.2)/4.0)**1.0 * 1.6)
    ax.plot(t_henry, y_henry, color=C_GOLD, linewidth=3.5, label="Matt Henry (4.6° Outswing to Top of Off)", zorder=4)
    ax.plot(10.2, 2.2, marker='o', markersize=9, color=C_GOLD, zorder=5)

    # Bowler 3 Trajectory: Jasprit Bumrah 142 kph Dipping Yorker (Base of stumps)
    t_bum = np.linspace(2.0, 14.1, 100)
    y_bum = np.where(t_bum < 13.8,
                     5.2 - ((t_bum - 2.0)/11.8)**1.3 * 3.0,
                     2.2)
    ax.plot(t_bum, y_bum, color="#38BDF8", linewidth=3.5, linestyle='--', label="Jasprit Bumrah (Base of Off Yorker)", zorder=4)
    ax.plot(13.8, 2.2, marker='o', markersize=9, color="#38BDF8", zorder=5)

    # Annotations & Telemetry callouts
    ax.text(2.0, 7.8, "HAWK-EYE 3D TRAJECTORY TELEMETRY", color=C_WHITE, fontsize=18, fontfamily='sans-serif', fontweight='heavy', zorder=6)
    ax.text(2.0, 7.2, "Release Vectors • Pitch Impact Zones • Lateral Seam Deviation", color=C_MUTED, fontsize=11, fontfamily='sans-serif', zorder=6)

    # Pitch Zone markers on surface
    for x_zone, label in [(8.5, "Short (8.5m)"), (10.2, "Good Length (6.5m)"), (13.8, "Yorker (0.5m)")]:
        ax.plot([x_zone, x_zone], [2.1, 2.3], color=C_WHITE, linewidth=1.5, zorder=3)
        ax.text(x_zone, 1.6, label, color=C_MUTED, fontsize=8, fontfamily='sans-serif', ha='center', zorder=3)

    out_path = os.path.join(ASSETS_DIR, "pitch_telemetry_plate.png")
    fig.savefig(out_path, dpi=DPI, facecolor=C_BG)
    plt.close(fig)
    print(f"Generated: {out_path}")

# -----------------------------------------------------------------------------
# ASSET 4: CAPITAL ALLOCATION & AUCTION DISCIPLINE PLATE
# -----------------------------------------------------------------------------
def generate_capital_allocation_plate():
    fig = plt.figure(figsize=(W_INCH, H_INCH), dpi=DPI, facecolor=C_BG)
    ax = fig.add_axes([0, 0, 1, 1])
    ax.set_facecolor(C_BG)
    ax.set_xlim(0, 16)
    ax.set_ylim(0, 9)
    ax.axis('off')

    # Purse Bar Visual Architecture
    # Total Cap ₹157 Cr: Retained ₹108.95 Cr (69.4%), Plan B Spend ₹15.70 Cr (10.0%), Reserve Cushion ₹29.30 Cr (18.6%)
    bar_y = 4.2
    bar_h = 1.4

    # Retained Bar (Dark Navy Surface)
    r1 = FancyBboxPatch((1.5, bar_y), 8.5, bar_h, boxstyle="round,pad=0.04", facecolor=C_SURFACE, edgecolor=C_MUTED, linewidth=1.5, zorder=2)
    # Plan B Spend (Royal Pink Highlight)
    r2 = FancyBboxPatch((10.1, bar_y), 2.2, bar_h, boxstyle="round,pad=0.04", facecolor=C_PINK, edgecolor=C_WHITE, linewidth=2.0, zorder=3)
    # Strategic Buffer (Gold Highlight)
    r3 = FancyBboxPatch((12.4, bar_y), 2.1, bar_h, boxstyle="round,pad=0.04", facecolor="#263450", edgecolor=C_GOLD, linewidth=1.5, zorder=2)
    
    ax.add_patch(r1)
    ax.add_patch(r2)
    ax.add_patch(r3)

    # Text inside bars
    ax.text(5.75, bar_y + 0.7, "RETAINED CORE SQUAD (16 PLAYERS) • ₹108.95 CR", color=C_WHITE, fontsize=10, fontfamily='sans-serif', fontweight='bold', ha='center', va='center', zorder=4)
    ax.text(11.2, bar_y + 0.7, "PLAN B SPEND\n₹15.70 CR", color=C_WHITE, fontsize=9, fontfamily='sans-serif', fontweight='heavy', ha='center', va='center', zorder=4)
    ax.text(13.45, bar_y + 0.7, "BUFFER\n₹29.30 CR", color=C_GOLD, fontsize=9, fontfamily='sans-serif', fontweight='bold', ha='center', va='center', zorder=4)

    # Top Header
    ax.text(1.5, 7.5, "AUCTION CAPITAL ALLOCATION & PURSE DISCPLINE", color=C_WHITE, fontsize=20, fontfamily='sans-serif', fontweight='heavy', zorder=5)
    ax.text(1.5, 6.9, "Statutory Cap: ₹157.00 Cr | Available Mini-Auction Capital: ₹45.00 Cr", color=C_GOLD, fontsize=12, fontfamily='sans-serif', fontweight='bold', zorder=5)

    # Sub-targets callout cards below
    # Target 1: Henry
    c1 = FancyBboxPatch((1.5, 1.4), 6.2, 1.8, boxstyle="round,pad=0.05", facecolor=C_SURFACE, edgecolor=C_PINK, linewidth=1.5, zorder=2)
    ax.add_patch(c1)
    ax.text(2.0, 2.7, "TARGET 1: MATT HENRY (SEAM SPEARHEAD)", color=C_PINK, fontsize=11, fontfamily='sans-serif', fontweight='heavy', zorder=3)
    ax.text(2.0, 2.2, "Fair Value: ₹10.50 Cr | Walk-Away Ceiling: ₹12.50 Cr", color=C_GOLD, fontsize=10, fontfamily='sans-serif', fontweight='bold', zorder=3)
    ax.text(2.0, 1.7, "Solves Powerplay swing & controls opposition top order under 7.20 RPO.", color=C_MUTED, fontsize=8.5, fontfamily='sans-serif', zorder=3)

    # Target 2: Suyash
    c2 = FancyBboxPatch((8.3, 1.4), 6.2, 1.8, boxstyle="round,pad=0.05", facecolor=C_SURFACE, edgecolor=C_GOLD, linewidth=1.5, zorder=2)
    ax.add_patch(c2)
    ax.text(8.8, 2.7, "TARGET 2: SUYASH SHARMA (WRIST-SPIN CHOKE)", color=C_GOLD, fontsize=11, fontfamily='sans-serif', fontweight='heavy', zorder=3)
    ax.text(8.8, 2.2, "Fair Value: ₹5.20 Cr | Walk-Away Ceiling: ₹6.80 Cr", color=C_WHITE, fontsize=10, fontfamily='sans-serif', fontweight='bold', zorder=3)
    ax.text(8.8, 1.7, "Chokes Overs 7-11 drift with 2,480 RPM overspin googlies in tandem with Jadeja.", color=C_MUTED, fontsize=8.5, fontfamily='sans-serif', zorder=3)

    out_path = os.path.join(ASSETS_DIR, "capital_allocation_plate.png")
    fig.savefig(out_path, dpi=DPI, facecolor=C_BG)
    plt.close(fig)
    print(f"Generated: {out_path}")

# -----------------------------------------------------------------------------
# ASSET 5: CHAMPIONSHIP RESOLUTION CLOSING POSTER
# -----------------------------------------------------------------------------
def generate_closing_poster():
    fig = plt.figure(figsize=(W_INCH, H_INCH), dpi=DPI, facecolor=C_BG)
    ax = fig.add_axes([0, 0, 1, 1])
    ax.set_facecolor(C_BG)
    ax.set_xlim(0, 16)
    ax.set_ylim(0, 9)
    ax.axis('off')

    # Radial golden aura in center-right
    Y, X = np.ogrid[:2160, :3840]
    dist_from_focal = np.sqrt((X - 3840 * 0.70)**2 + (Y - 2160 * 0.55)**2)
    max_d = np.sqrt((3840 * 0.70)**2 + (2160 * 0.55)**2)
    gradient = 1.0 - (dist_from_focal / max_d) * 0.7
    gradient = np.clip(gradient, 0.15, 1.0)
    ax.imshow(gradient, extent=[0, 16, 0, 9], cmap="cividis", alpha=0.25, aspect='auto', zorder=1)

    # Stylized IPL Trophy Silhouette Geometry (Architectural minimalism)
    trophy_pts = np.array([
        [10.5, 2.2], [12.5, 2.2],
        [12.1, 3.2], [12.7, 5.5],
        [12.2, 6.8], [10.8, 6.8],
        [10.3, 5.5], [10.9, 3.2]
    ])
    trophy = Polygon(trophy_pts, closed=True, facecolor=C_GOLD, edgecolor="#FFE885", linewidth=2.0, alpha=0.85, zorder=3)
    ax.add_patch(trophy)

    # Base of trophy
    base = Rectangle((10.0, 1.8), 3.0, 0.4, facecolor=C_SURFACE, edgecolor=C_GOLD, linewidth=1.5, zorder=4)
    ax.add_patch(base)

    # Left-Side Big Stat Numbers (Editable style presentation)
    ax.text(2.0, 6.8, "68.4%", color=C_GOLD, fontsize=58, fontfamily='sans-serif', fontweight='heavy', zorder=5)
    ax.text(2.0, 5.9, "PLAYOFF QUALIFICATION PROBABILITY", color=C_WHITE, fontsize=13, fontfamily='sans-serif', fontweight='heavy', zorder=5)

    ax.text(2.0, 4.4, "16.8%", color=C_PINK, fontsize=42, fontfamily='sans-serif', fontweight='heavy', zorder=5)
    ax.text(2.0, 3.7, "IPL 2027 TITLE WIN PROBABILITY (2ND TOURNAMENT-WIDE)", color=C_MUTED, fontsize=11, fontfamily='sans-serif', fontweight='bold', zorder=5)

    ax.text(2.0, 2.2, "HALLA BOL • JAIPUR FORTRESS RATIFIED", color=C_GOLD, fontsize=12, fontfamily='sans-serif', fontweight='heavy', zorder=5)

    out_path = os.path.join(ASSETS_DIR, "championship_verdict_plate.png")
    fig.savefig(out_path, dpi=DPI, facecolor=C_BG)
    plt.close(fig)
    print(f"Generated: {out_path}")

if __name__ == "__main__":
    generate_cover_hero_plate()
    generate_comparison_plate()
    generate_pitch_physics_plate()
    generate_capital_allocation_plate()
    generate_closing_poster()
    print("All 5 Presentation-Grade Visual Plates Generated Successfully!")
