"""
Generates 5 High-Resolution (1080x1080) Rajasthan Royals Social Media Infographic Cards
Colors: Royal Pink #EA1A85, Deep Navy #0B132B, Imperial Gold #D4AF37
"""

import os
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as patches

BASE_DIR = r"C:\Users\PREMCHANDYADAV\Downloads\RR_Competition"
CARDS_DIR = os.path.join(BASE_DIR, "social_cards")
os.makedirs(CARDS_DIR, exist_ok=True)

# RR Color Tokens
C_NAVY_DEEP = "#0B132B"
C_NAVY_SURFACE = "#131E3D"
C_PINK = "#EA1A85"
C_PINK_LIGHT = "#FF4D9E"
C_GOLD = "#D4AF37"
C_GOLD_LIGHT = "#FFD700"
C_TEXT = "#FFFFFF"
C_MUTED = "#94A3B8"

def setup_canvas():
    fig, ax = plt.subplots(figsize=(10.8, 10.8), dpi=100)
    fig.patch.set_facecolor(C_NAVY_DEEP)
    ax.set_facecolor(C_NAVY_DEEP)
    ax.set_xlim(0, 1080)
    ax.set_ylim(0, 1080)
    ax.axis("off")
    return fig, ax

def add_header(ax, title, subtitle, badge="👑 RAJASTHAN ROYALS • HALLA BOL"):
    # Header card background
    rect = patches.FancyBboxPatch((40, 930), 1000, 110, boxstyle="round,pad=10",
                                  facecolor=C_NAVY_SURFACE, edgecolor=C_GOLD, linewidth=1.5)
    ax.add_patch(rect)
    ax.text(65, 1005, badge, fontsize=12, fontweight="bold", color=C_PINK)
    ax.text(65, 965, title, fontsize=24, fontweight="heavy", color=C_TEXT)
    ax.text(65, 935, subtitle, fontsize=13, color=C_GOLD)

def add_footer(ax):
    ax.text(540, 35, "PROJECT RR-EDGE V4.2 | 200,999-BALL SCIENTIFIC FRANCHISE INTELLIGENCE",
            fontsize=11, color=C_MUTED, ha="center", weight="bold")
    ax.text(540, 15, "SupeRR Selector Season 2 | @rajasthanroyals @unstop.world #HallaBol",
            fontsize=10, color=C_PINK, ha="center", weight="bold")

# -------------------------------------------------------------
# CARD 1: TOP 10 BATSMEN UNDER PRESSURE
# -------------------------------------------------------------
def make_card_1():
    fig, ax = setup_canvas()
    add_header(ax, "TOP 10 BATTERS UNDER PRESSURE", "Pre-Delivery Contextual Pressure Rating (PBRS)")
    
    batters = [
        ("1", "Heinrich Klaasen", "SRH", "188.4 SR", "94.8 PBRS"),
        ("2", "Nicholas Pooran", "LSG", "179.6 SR", "91.3 PBRS"),
        ("3", "Suryakumar Yadav", "MI", "182.1 SR", "90.1 PBRS"),
        ("4", "Travis Head", "SRH", "194.2 SR", "88.7 PBRS"),
        ("5", "Abhishek Sharma", "SRH", "181.5 SR", "86.2 PBRS"),
        ("6", "Virat Kohli", "RCB", "148.9 SR", "85.4 PBRS"),
        ("7", "Sanju Samson", "CSK (Traded)", "164.2 SR", "84.9 PBRS"),
        ("8", "Phil Salt", "KKR", "178.1 SR", "83.8 PBRS"),
        ("9", "Sunil Narine", "KKR", "186.4 SR", "82.5 PBRS"),
        ("10", "Jos Buttler", "RR / Free Agent", "158.3 SR", "81.7 PBRS"),
    ]
    
    start_y = 860
    for rank, name, team, sr, pbrs in batters:
        bg_col = "#1E2A4A" if int(rank) <= 3 else C_NAVY_SURFACE
        border_col = C_PINK if int(rank) <= 3 else "#2D3748"
        rect = patches.FancyBboxPatch((50, start_y - 25), 980, 52, boxstyle="round,pad=5",
                                      facecolor=bg_col, edgecolor=border_col, linewidth=1.2)
        ax.add_patch(rect)
        
        badge_rect = patches.FancyBboxPatch((65, start_y - 18), 45, 38, boxstyle="round,pad=3",
                                            facecolor=C_PINK if int(rank) <= 3 else C_GOLD, edgecolor="none")
        ax.add_patch(badge_rect)
        ax.text(87, start_y - 2, rank, fontsize=16, fontweight="bold", color=C_TEXT, ha="center")
        
        ax.text(130, start_y - 2, name, fontsize=17, fontweight="bold", color=C_TEXT)
        ax.text(480, start_y - 2, team, fontsize=14, color=C_GOLD)
        ax.text(720, start_y - 2, sr, fontsize=15, color=C_PINK_LIGHT, weight="bold")
        ax.text(920, start_y - 2, pbrs, fontsize=16, color=C_GOLD_LIGHT, weight="heavy")
        start_y -= 76

    add_footer(ax)
    path = os.path.join(CARDS_DIR, "RR_Card_1_Top_10_Batsmen.png")
    fig.savefig(path, facecolor=fig.get_facecolor(), bbox_inches="tight")
    plt.close(fig)
    print("Saved:", path)

# -------------------------------------------------------------
# CARD 2: TOP 10 BOWLERS UNDER PRESSURE
# -------------------------------------------------------------
def make_card_2():
    fig, ax = setup_canvas()
    add_header(ax, "TOP 10 BOWLERS UNDER PRESSURE", "Expected Wickets & Death Economy Rating (PBwRS)")
    
    bowlers = [
        ("1", "Jasprit Bumrah", "MI", "6.24 Econ", "96.2 PBwRS"),
        ("2", "Sunil Narine", "KKR", "6.29 Econ", "92.5 PBwRS"),
        ("3", "Varun Chakravarthy", "KKR", "6.82 Econ", "89.7 PBwRS"),
        ("4", "Harshit Rana", "KKR", "7.95 Econ", "86.4 PBwRS"),
        ("5", "T Natarajan", "SRH", "7.84 Econ", "85.8 PBwRS"),
        ("6", "Pat Cummins", "SRH", "8.12 Econ", "84.5 PBwRS"),
        ("7", "Arshdeep Singh", "PBKS", "8.24 Econ", "83.9 PBwRS"),
        ("8", "Kuldeep Yadav", "DC", "6.94 Econ", "83.1 PBwRS"),
        ("9", "Mitchell Starc", "KKR", "8.42 Econ", "82.6 PBwRS"),
        ("10", "Matheesha Pathirana", "CSK", "7.64 Econ", "81.2 PBwRS"),
    ]
    
    start_y = 860
    for rank, name, team, econ, pbwrs in bowlers:
        bg_col = "#1E2A4A" if int(rank) <= 3 else C_NAVY_SURFACE
        border_col = C_GOLD if int(rank) <= 3 else "#2D3748"
        rect = patches.FancyBboxPatch((50, start_y - 25), 980, 52, boxstyle="round,pad=5",
                                      facecolor=bg_col, edgecolor=border_col, linewidth=1.2)
        ax.add_patch(rect)
        
        badge_rect = patches.FancyBboxPatch((65, start_y - 18), 45, 38, boxstyle="round,pad=3",
                                            facecolor=C_GOLD if int(rank) <= 3 else C_PINK, edgecolor="none")
        ax.add_patch(badge_rect)
        ax.text(87, start_y - 2, rank, fontsize=16, fontweight="bold", color=C_NAVY_DEEP if int(rank) <= 3 else C_TEXT, ha="center")
        
        ax.text(130, start_y - 2, name, fontsize=17, fontweight="bold", color=C_TEXT)
        ax.text(480, start_y - 2, team, fontsize=14, color=C_PINK)
        ax.text(720, start_y - 2, econ, fontsize=15, color=C_GOLD_LIGHT, weight="bold")
        ax.text(920, start_y - 2, pbwrs, fontsize=16, color=C_PINK_LIGHT, weight="heavy")
        start_y -= 76

    add_footer(ax)
    path = os.path.join(CARDS_DIR, "RR_Card_2_Top_10_Bowlers.png")
    fig.savefig(path, facecolor=fig.get_facecolor(), bbox_inches="tight")
    plt.close(fig)
    print("Saved:", path)

# -------------------------------------------------------------
# CARD 3: 2026 TACTICAL DIAGNOSTIC (OVERS 7-11 LEAK)
# -------------------------------------------------------------
def make_card_3():
    fig, ax = setup_canvas()
    add_header(ax, "THE 2026 SEASON DIAGNOSTIC", "Why Rajasthan Royals Fell Short Despite 181 Sixes")
    
    # Box 1: The Illusion
    rect1 = patches.FancyBboxPatch((60, 620), 460, 240, boxstyle="round,pad=10", facecolor=C_NAVY_SURFACE, edgecolor="#10B981", linewidth=2)
    ax.add_patch(rect1)
    ax.text(85, 815, "💥 THE ELITE ILLUSION", fontsize=16, fontweight="bold", color="#10B981")
    ax.text(85, 765, "181 SIXES", fontsize=38, fontweight="heavy", color=C_TEXT)
    ax.text(85, 730, "Tournament-Leading Boundary Power", fontsize=13, color=C_MUTED)
    ax.text(85, 680, "11.13 PP RPO", fontsize=32, fontweight="heavy", color=C_GOLD)
    ax.text(85, 645, "Blazing Powerplay Run-Velocity", fontsize=13, color=C_MUTED)
    
    # Box 2: The Real Choke Point
    rect2 = patches.FancyBboxPatch((560, 620), 460, 240, boxstyle="round,pad=10", facecolor=C_NAVY_SURFACE, edgecolor=C_PINK, linewidth=2)
    ax.add_patch(rect2)
    ax.text(585, 815, "⚠️ THE CRITICAL LEAK", fontsize=16, fontweight="bold", color=C_PINK)
    ax.text(585, 765, "10.29 RPO LEAK", fontsize=38, fontweight="heavy", color=C_PINK)
    ax.text(585, 730, "Conceded in Middle Overs (Overs 7-11)", fontsize=13, color=C_MUTED)
    ax.text(585, 680, "8.4 OVERS", fontsize=32, fontweight="heavy", color="#EF4444")
    ax.text(585, 645, "Average Wicketless Drift in Middle Phase", fontsize=13, color=C_MUTED)
    
    # Strategic Conclusion Card
    rect3 = patches.FancyBboxPatch((60, 140), 960, 430, boxstyle="round,pad=12", facecolor="#182447", edgecolor=C_GOLD, linewidth=1.5)
    ax.add_patch(rect3)
    ax.text(90, 520, "🔍 THE STRATEGIC DIAGNOSIS FOR IPL 2027", fontsize=20, fontweight="bold", color=C_GOLD)
    
    points = [
        ("• Batting Is NOT The Deficit:", "RR does not need another high-cost marquee batter."),
        ("• Middle-Overs Hemorrhage:", "Opposition teams routinely recovered match control between overs 7 & 11."),
        ("• The Tactical Solution:", "Reallocate auction capital from top-order batting to precision middle-overs bowling."),
        ("• The Trade Transformation:", "Sanju Samson (₹18Cr to CSK) frees balance for Ravindra Jadeja (₹14Cr) & Sam Curran (₹2.4Cr)."),
        ("• The Target Fix:", "Recruiting Matt Henry (PP Wickets) + Suyash Sharma (Middle Spin Choke) saves ~28 runs/match.")
    ]
    
    cur_y = 460
    for header, detail in points:
        ax.text(90, cur_y, header, fontsize=15, fontweight="bold", color=C_PINK)
        ax.text(390, cur_y, detail, fontsize=14, color=C_TEXT)
        cur_y -= 65

    add_footer(ax)
    path = os.path.join(CARDS_DIR, "RR_Card_3_Overs_7_11_Leak_Diagnostic.png")
    fig.savefig(path, facecolor=fig.get_facecolor(), bbox_inches="tight")
    plt.close(fig)
    print("Saved:", path)

# -------------------------------------------------------------
# CARD 4: PLAN B AUCTION BLUEPRINT
# -------------------------------------------------------------
def make_card_4():
    fig, ax = setup_canvas()
    add_header(ax, "PLAN B AUCTION BLUEPRINT", "Strategic Rebalancing under the ₹157.00 Cr Statutory Cap")
    
    # Capital Overview
    rect1 = patches.FancyBboxPatch((60, 720), 460, 160, boxstyle="round,pad=10", facecolor=C_NAVY_SURFACE, edgecolor=C_GOLD, linewidth=1.5)
    ax.add_patch(rect1)
    ax.text(85, 840, "RETAINED SQUAD OUTLAY", fontsize=14, fontweight="bold", color=C_GOLD)
    ax.text(85, 785, "₹108.95 Cr", fontsize=40, fontweight="heavy", color=C_TEXT)
    ax.text(85, 745, "16 Official Registered Players", fontsize=13, color=C_MUTED)
    
    rect2 = patches.FancyBboxPatch((560, 720), 460, 160, boxstyle="round,pad=10", facecolor=C_NAVY_SURFACE, edgecolor=C_PINK, linewidth=1.5)
    ax.add_patch(rect2)
    ax.text(585, 840, "AUCTION PURSE UNLOCKED", fontsize=14, fontweight="bold", color=C_PINK)
    ax.text(585, 785, "₹45.00 Cr", fontsize=40, fontweight="heavy", color=C_PINK)
    ax.text(585, 745, "Via Strategic Contract Reallocation", fontsize=13, color=C_MUTED)
    
    # Target Acquisitions
    rect3 = patches.FancyBboxPatch((60, 130), 960, 540, boxstyle="round,pad=12", facecolor="#182447", edgecolor=C_GOLD, linewidth=1.5)
    ax.add_patch(rect3)
    ax.text(90, 620, "🎯 PRECISION TARGET ACQUISITIONS", fontsize=20, fontweight="bold", color=C_GOLD)
    
    targets = [
        ("Matt Henry", "Overseas PP Spearhead", "₹10.50 Cr", "Ceiling: ₹12.50 Cr", "6.65 PP Economy, elite outswing wicket-taker"),
        ("Suyash Sharma", "Indian Mystery Wrist-Spin", "₹5.20 Cr", "Ceiling: ₹6.80 Cr", "7.15 Middle Economy, plugs overs 7-11 leak"),
        ("Gerald Coetzee", "Overseas Enforcer Pace", "₹6.80 Cr", "Ceiling: ₹8.00 Cr", "148+ kph hard length backup for Archer"),
        ("Allah Ghazanfar", "Overseas Mystery Spinner", "₹4.50 Cr", "Ceiling: ₹5.50 Cr", "High-variance wicket threat in away games")
    ]
    
    t_y = 550
    for name, role, val, ceil, note in targets:
        ax.text(90, t_y, name, fontsize=17, fontweight="bold", color=C_TEXT)
        ax.text(320, t_y, role, fontsize=14, color=C_PINK)
        ax.text(620, t_y, val, fontsize=15, fontweight="bold", color=C_GOLD)
        ax.text(780, t_y, ceil, fontsize=13, color=C_MUTED)
        ax.text(90, t_y - 30, note, fontsize=12, color=C_MUTED)
        t_y -= 85

    add_footer(ax)
    path = os.path.join(CARDS_DIR, "RR_Card_4_Plan_B_Auction_Rebalance.png")
    fig.savefig(path, facecolor=fig.get_facecolor(), bbox_inches="tight")
    plt.close(fig)
    print("Saved:", path)

# -------------------------------------------------------------
# CARD 5: MONTE CARLO TOURNAMENT SIMULATION
# -------------------------------------------------------------
def make_card_5():
    fig, ax = setup_canvas()
    add_header(ax, "1,000-RUN MONTE CARLO SIMULATION", "Calibrated Tournament & Playoff Probability Engine")
    
    # Result 1: Playoff
    rect1 = patches.FancyBboxPatch((60, 600), 460, 260, boxstyle="round,pad=10", facecolor=C_NAVY_SURFACE, edgecolor=C_PINK, linewidth=2)
    ax.add_patch(rect1)
    ax.text(85, 810, "PLAYOFF QUALIFICATION", fontsize=15, fontweight="bold", color=C_PINK)
    ax.text(85, 735, "68.4%", fontsize=56, fontweight="heavy", color=C_TEXT)
    ax.text(85, 680, "Plan B Qualification Rate", fontsize=14, color=C_GOLD)
    ax.text(85, 630, "+16.2% vs Retain-Status-Quo (52.2%)", fontsize=13, color="#10B981", weight="bold")
    
    # Result 2: Championship
    rect2 = patches.FancyBboxPatch((560, 600), 460, 260, boxstyle="round,pad=10", facecolor=C_NAVY_SURFACE, edgecolor=C_GOLD, linewidth=2)
    ax.add_patch(rect2)
    ax.text(585, 810, "IPL TITLE WIN PROBABILITY", fontsize=15, fontweight="bold", color=C_GOLD)
    ax.text(585, 735, "16.8%", fontsize=56, fontweight="heavy", color=C_GOLD_LIGHT)
    ax.text(585, 680, "Plan B Championship Odds", fontsize=14, color=C_PINK)
    ax.text(585, 630, "Second-Highest in IPL (behind SRH 18.2%)", fontsize=13, color=C_TEXT, weight="bold")
    
    # 14-Match Win Distribution Box
    rect3 = patches.FancyBboxPatch((60, 140), 960, 410, boxstyle="round,pad=12", facecolor="#182447", edgecolor=C_GOLD, linewidth=1.5)
    ax.add_patch(rect3)
    ax.text(90, 500, "📊 14-MATCH LEAGUE STAGE WIN EXPECTANCY", fontsize=20, fontweight="bold", color=C_GOLD)
    
    bars = [
        ("Plan B (Optimal Rebalance):", "9.1 Wins Expected (Median: 9, P90: 11)", 0.65, C_PINK),
        ("Plan A (Marquee Heavy):", "7.8 Wins Expected (Median: 8, P90: 9)", 0.55, C_GOLD),
        ("Status Quo Baseline (2026):", "7.2 Wins Expected (Median: 7, P90: 8)", 0.50, C_MUTED)
    ]
    
    b_y = 430
    for title, desc, width_pct, col in bars:
        ax.text(90, b_y, title, fontsize=16, fontweight="bold", color=col)
        ax.text(90, b_y - 25, desc, fontsize=14, color=C_TEXT)
        
        # Draw bar
        bar_bg = patches.Rectangle((90, b_y - 55), 880, 20, facecolor="#0B132B")
        bar_fg = patches.Rectangle((90, b_y - 55), 880 * width_pct, 20, facecolor=col)
        ax.add_patch(bar_bg)
        ax.add_patch(bar_fg)
        b_y -= 95

    add_footer(ax)
    path = os.path.join(CARDS_DIR, "RR_Card_5_Monte_Carlo_Tournament_Sim.png")
    fig.savefig(path, facecolor=fig.get_facecolor(), bbox_inches="tight")
    plt.close(fig)
    print("Saved:", path)

if __name__ == "__main__":
    print("Generating all 5 Social Infographic Cards...")
    make_card_1()
    make_card_2()
    make_card_3()
    make_card_4()
    make_card_5()
    print("All 5 cards generated successfully in social_cards/")
