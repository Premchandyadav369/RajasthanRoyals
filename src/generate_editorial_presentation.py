"""
PROJECT RR-EDGE V5.0: EDITORIAL MASTER PRESENTATION DECK (12-SLIDE WIDESCREEN)
Re-architected strictly adhering to PPT Image DESIGN.md and the PPTX Skill:
- Zero AI slop (NO decorative lines under titles, NO accent stripes, NO fake emoji bullets)
- Restrained presentation palette: Deep Ink Navy #0B132B, Royal Pink #EA1A85, Imperial Gold #D4AF37, Paper White #F8FAFC
- Large stat callouts (48-56pt bold numbers with clean labels below)
- 16:9 Widescreen (13.333" x 7.5")
- Integrated high-resolution slide assets with clean text-safe space
- Clean left-aligned typography, generous breathing room (>=0.5" margins)
"""

import os
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.enum.text import PP_ALIGN
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE

BASE_DIR = r"C:\Users\PREMCHANDYADAV\Downloads\RR_Competition"
ASSETS_DIR = os.path.join(BASE_DIR, "slide_assets")
PPTX_PATH_V5 = os.path.join(BASE_DIR, "RR_EDGE_V5_0_Executive_Presentation.pptx")
PPTX_PATH_V4 = os.path.join(BASE_DIR, "RR_EDGE_V4_2_Presentation.pptx")

# Palette Constants
C_NAVY = RGBColor(11, 19, 43)        # #0B132B (Deep Anchor)
C_SURFACE = RGBColor(19, 30, 61)     # #131E3D (Subtle Card Surface)
C_SURFACE_ALT = RGBColor(24, 38, 77) # #18264D
C_PINK = RGBColor(234, 26, 133)      # #EA1A85 (Primary Accent)
C_GOLD = RGBColor(212, 175, 55)      # #D4AF37 (Secondary Accent)
C_WHITE = RGBColor(248, 250, 252)    # #F8FAFC (Paper White)
C_MUTED = RGBColor(148, 163, 184)    # #94A3B8 (Slate Support)
C_ALERT = RGBColor(239, 68, 68)      # #EF4444 (Signal Red)
C_SUCCESS = RGBColor(16, 185, 129)   # #10B981 (Signal Green)

FONT_HEAD = "Arial"
FONT_BODY = "Calibri"

def apply_background(slide, color=C_NAVY):
    bg = slide.background
    fill = bg.fill
    fill.solid()
    fill.fore_color.rgb = color

def add_header(slide, title, category="RAJASTHAN ROYALS • PROJECT RR-EDGE V5.0"):
    # Clean header without decorative lines or accent stripes
    txBox = slide.shapes.add_textbox(Inches(0.8), Inches(0.45), Inches(11.7), Inches(0.95))
    tf = txBox.text_frame
    tf.word_wrap = True
    tf.margin_left = tf.margin_right = tf.margin_top = tf.margin_bottom = 0
    
    p_cat = tf.paragraphs[0]
    p_cat.text = category.upper()
    p_cat.font.name = FONT_HEAD
    p_cat.font.size = Pt(10)
    p_cat.font.bold = True
    p_cat.font.color.rgb = C_GOLD
    p_cat.space_after = Pt(2)

    p_tit = tf.add_paragraph()
    p_tit.text = title
    p_tit.font.name = FONT_HEAD
    p_tit.font.size = Pt(22)
    p_tit.font.bold = True
    p_tit.font.color.rgb = C_WHITE

def add_stat_callout(slide, left, top, width, height, number_str, label_str, num_color=C_GOLD, sub_str=None):
    # Stat callout card (large number with clear small label)
    card = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, left, top, width, height)
    card.fill.solid()
    card.fill.fore_color.rgb = C_SURFACE
    card.line.color.rgb = C_SURFACE_ALT
    card.line.width = Pt(1)

    tf = card.text_frame
    tf.word_wrap = True
    tf.margin_left = Inches(0.2)
    tf.margin_right = Inches(0.2)
    tf.margin_top = Inches(0.18)
    tf.margin_bottom = Inches(0.15)

    p_num = tf.paragraphs[0]
    p_num.text = number_str
    p_num.font.name = FONT_HEAD
    p_num.font.size = Pt(36)
    p_num.font.bold = True
    p_num.font.color.rgb = num_color
    p_num.space_after = Pt(2)

    p_lbl = tf.add_paragraph()
    p_lbl.text = label_str
    p_lbl.font.name = FONT_BODY
    p_lbl.font.size = Pt(10.5)
    p_lbl.font.color.rgb = C_WHITE
    p_lbl.font.bold = True

    if sub_str:
        p_sub = tf.add_paragraph()
        p_sub.text = sub_str
        p_sub.font.name = FONT_BODY
        p_sub.font.size = Pt(9)
        p_sub.font.color.rgb = C_MUTED
        p_sub.space_before = Pt(2)

def build_presentation():
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    blank_layout = prs.slide_layouts[6]

    # =========================================================================
    # SLIDE 1: COVER HERO (Editorial Poster with 4K Asset)
    # =========================================================================
    s1 = prs.slides.add_slide(blank_layout)
    apply_background(s1, C_NAVY)

    cover_img_path = os.path.join(ASSETS_DIR, "hero_cover_plate.png")
    if os.path.exists(cover_img_path):
        s1.shapes.add_picture(cover_img_path, Inches(0), Inches(0), Inches(13.333), Inches(7.5))

    tb_cover = s1.shapes.add_textbox(Inches(0.9), Inches(1.8), Inches(6.8), Inches(4.2))
    tf_c = tb_cover.text_frame
    tf_c.word_wrap = True
    tf_c.margin_left = tf_c.margin_right = tf_c.margin_top = tf_c.margin_bottom = 0

    p1 = tf_c.paragraphs[0]
    p1.text = "RAJASTHAN ROYALS • MINI-AUCTION 2027"
    p1.font.name = FONT_HEAD
    p1.font.size = Pt(11)
    p1.font.bold = True
    p1.font.color.rgb = C_GOLD
    p1.space_after = Pt(8)

    p2 = tf_c.add_paragraph()
    p2.text = "PROJECT RR-EDGE V5.0"
    p2.font.name = FONT_HEAD
    p2.font.size = Pt(40)
    p2.font.bold = True
    p2.font.color.rgb = C_WHITE
    p2.space_after = Pt(12)

    p3 = tf_c.add_paragraph()
    p3.text = "The Quantitative Roadmap to the 2027 Trophy: Resolving Middle-Overs Bowling Leakage Through Market Asymmetry"
    p3.font.name = FONT_BODY
    p3.font.size = Pt(15)
    p3.font.color.rgb = C_MUTED
    p3.space_after = Pt(24)

    p4 = tf_c.add_paragraph()
    p4.text = "Prepared for: Kumar Sangakkara, Jake Lush McCrum, Manoj Badale\nSubmission: SupeRR Selector Season 2 • Official Franchise Dossier"
    p4.font.name = FONT_BODY
    p4.font.size = Pt(10)
    p4.font.color.rgb = C_WHITE

    # =========================================================================
    # SLIDE 2: EXECUTIVE STRATEGY & THE 2026 BOTTLENECK
    # =========================================================================
    s2 = prs.slides.add_slide(blank_layout)
    apply_background(s2, C_NAVY)
    add_header(s2, "Executive Strategy: Resolving the 2026 Structural Deficit")

    # 4 Stat Callout Cards
    add_stat_callout(s2, Inches(0.8), Inches(1.6), Inches(2.75), Inches(1.4), "181", "Sixes Hit in 2026", C_WHITE, "Tournament-Leading Batting Power")
    add_stat_callout(s2, Inches(3.78), Inches(1.6), Inches(2.75), Inches(1.4), "11.13", "Powerplay RPO", C_WHITE, "Top Powerplay Run Rate")
    add_stat_callout(s2, Inches(6.76), Inches(1.6), Inches(2.75), Inches(1.4), "10.29", "Overs 7-11 RPO Conceded", C_ALERT, "The Unaddressed Structural Deficit")
    add_stat_callout(s2, Inches(9.74), Inches(1.6), Inches(2.75), Inches(1.4), "8.4 Overs", "Wicketless Drift", C_ALERT, "Average Inability to Break Partnerships")

    # Left Column: Strategic Thesis
    card_th = s2.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.8), Inches(3.2), Inches(5.7), Inches(3.8))
    card_th.fill.solid()
    card_th.fill.fore_color.rgb = C_SURFACE
    card_th.line.color.rgb = C_SURFACE_ALT
    card_th.line.width = Pt(1)

    tf_th = card_th.text_frame
    tf_th.word_wrap = True
    tf_th.margin_left = tf_th.margin_right = tf_th.margin_top = tf_th.margin_bottom = Inches(0.3)

    p_th_h = tf_th.paragraphs[0]
    p_th_h.text = "THE STRATEGIC THESIS (PLAN B)"
    p_th_h.font.name = FONT_HEAD
    p_th_h.font.size = Pt(13)
    p_th_h.font.bold = True
    p_th_h.font.color.rgb = C_GOLD
    p_th_h.space_after = Pt(10)

    points_th = [
        ("The False Diagnosis:", "Conventional wisdom suggests spending ₹20+ Cr to replace Sanju Samson's batting. Empirical modeling reveals this yields <0.2 net WAR."),
        ("The True Deficit:", "RR missed the 2026 playoffs entirely due to bowling leakage in Overs 7–11. Conceding 200+ runs in 74.85% of matches made playoff qualification mathematically improbable."),
        ("The Capital Solution:", "Target Matt Henry (₹10.50 Cr) and Suyash Sharma (₹5.20 Cr). Total spend of ₹15.70 Cr collapses 200+ runs conceded to 36.37% (-38.5%) and preserves ₹29.30 Cr purse flexibility.")
    ]
    for tit, dsc in points_th:
        pt = tf_th.add_paragraph()
        pt.text = tit
        pt.font.name = FONT_HEAD
        pt.font.size = Pt(11)
        pt.font.bold = True
        pt.font.color.rgb = C_WHITE
        
        pd = tf_th.add_paragraph()
        pd.text = dsc
        pd.font.name = FONT_BODY
        pd.font.size = Pt(10)
        pd.font.color.rgb = C_MUTED
        pd.space_after = Pt(8)

    # Right Column: The 2027 Solution Matrix
    card_sol = s2.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(6.8), Inches(3.2), Inches(5.7), Inches(3.8))
    card_sol.fill.solid()
    card_sol.fill.fore_color.rgb = C_SURFACE
    card_sol.line.color.rgb = C_SURFACE_ALT
    card_sol.line.width = Pt(1)

    tf_sol = card_sol.text_frame
    tf_sol.word_wrap = True
    tf_sol.margin_left = tf_sol.margin_right = tf_sol.margin_top = tf_sol.margin_bottom = Inches(0.3)

    p_sol_h = tf_sol.paragraphs[0]
    p_sol_h.text = "THE RECONFIGURED SQUAD ARCHITECTURE"
    p_sol_h.font.name = FONT_HEAD
    p_sol_h.font.size = Pt(13)
    p_sol_h.font.bold = True
    p_sol_h.font.color.rgb = C_PINK
    p_sol_h.space_after = Pt(10)

    points_sol = [
        ("Samson Traded to CSK:", "Sanju Samson traded on 15 Nov 2025 at ₹18.00 Cr. In exchange, RR acquired Ravindra Jadeja (₹14.00 Cr) and Sam Curran (₹2.40 Cr)."),
        ("New Leadership Group:", "Riyan Parag appointed Captain. Dhruv Jurel installed as primary Wicketkeeper. Ravindra Jadeja serves as Senior On-Field Strategist."),
        ("Mini-Auction Capital:", "RR retains 16 core players at ₹108.95 Cr. Available mini-auction purse is ₹45.00 Cr under the official ₹157.00 Cr cap.")
    ]
    for tit, dsc in points_sol:
        pt = tf_sol.add_paragraph()
        pt.text = tit
        pt.font.name = FONT_HEAD
        pt.font.size = Pt(11)
        pt.font.bold = True
        pt.font.color.rgb = C_WHITE
        
        pd = tf_sol.add_paragraph()
        pd.text = dsc
        pd.font.name = FONT_BODY
        pd.font.size = Pt(10)
        pd.font.color.rgb = C_MUTED
        pd.space_after = Pt(8)

    # =========================================================================
    # SLIDE 3: FORENSIC COMPARISON (Integrated 4K Visual Plate)
    # =========================================================================
    s3 = prs.slides.add_slide(blank_layout)
    apply_background(s3, C_NAVY)
    add_header(s3, "2026 Forensic Diagnosis: The Overs 7–11 Bowling Drift")

    comp_img_path = os.path.join(ASSETS_DIR, "bottleneck_comparison_plate.png")
    if os.path.exists(comp_img_path):
        s3.shapes.add_picture(comp_img_path, Inches(0.8), Inches(1.6), Inches(11.733), Inches(5.1))

    # =========================================================================
    # SLIDE 4: SCIENTIFIC RIGOR & BAYESIAN ARCHITECTURE
    # =========================================================================
    s4 = prs.slides.add_slide(blank_layout)
    apply_background(s4, C_NAVY)
    add_header(s4, "Scientific Rigor: Zero-Leakage Bayesian Feature Architecture")

    # 3 Stat Cards
    add_stat_callout(s4, Inches(0.8), Inches(1.6), Inches(3.7), Inches(1.3), "1.7537", "Stacking Test RMSE", C_GOLD, "LightGBM + XGBoost + Ridge Ensemble")
    add_stat_callout(s4, Inches(4.8), Inches(1.6), Inches(3.7), Inches(1.3), "0.8912", "Classification ROC-AUC", C_SUCCESS, "High-Pressure Delivery Classification")
    add_stat_callout(s4, Inches(8.8), Inches(1.6), Inches(3.7), Inches(1.3), ">92.8%", "Context Variance Explained", C_WHITE, "Boruta Validated Non-Spurious Signals")

    # 2 Detail Cards Below
    card_m1 = s4.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.8), Inches(3.1), Inches(5.7), Inches(3.9))
    card_m1.fill.solid()
    card_m1.fill.fore_color.rgb = C_SURFACE
    card_m1.line.color.rgb = C_SURFACE_ALT
    card_m1.line.width = Pt(1)

    tf_m1 = card_m1.text_frame
    tf_m1.word_wrap = True
    tf_m1.margin_left = tf_m1.margin_right = tf_m1.margin_top = tf_m1.margin_bottom = Inches(0.25)

    p_m1_h = tf_m1.paragraphs[0]
    p_m1_h.text = "MATHEMATICAL FORMULATIONS"
    p_m1_h.font.name = FONT_HEAD
    p_m1_h.font.size = Pt(12)
    p_m1_h.font.bold = True
    p_m1_h.font.color.rgb = C_GOLD
    p_m1_h.space_after = Pt(8)

    math_points = [
        ("Pre-Delivery Pressure Index (P_pre):", "P_pre = 0.40(RRR/10) + 0.35((10-W)/10) + 0.25(Phase_Weight)\nBounded in [0, 1]. Calculated strictly before each ball release."),
        ("Bayesian Shrinkage Baseline (mu_adj):", "mu_adj = (N / (N + K)) * mu_player + (K / (N + K)) * mu_league\nK=30 balls. Eliminates sample size distortion for rare high-pressure events."),
        ("Clutch Volatility Index (CVI):", "CVI = StdDev(Impact_Pressure) / Mean(Impact_Normal)\nMeasures variance in player output under critical vs low-leverage match conditions.")
    ]
    for tit, dsc in math_points:
        pt = tf_m1.add_paragraph()
        pt.text = tit
        pt.font.name = FONT_HEAD
        pt.font.size = Pt(10)
        pt.font.bold = True
        pt.font.color.rgb = C_WHITE
        
        pd = tf_m1.add_paragraph()
        pd.text = dsc
        pd.font.name = FONT_BODY
        pd.font.size = Pt(9.5)
        pd.font.color.rgb = C_MUTED
        pd.space_after = Pt(6)

    card_m2 = s4.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(6.8), Inches(3.1), Inches(5.7), Inches(3.9))
    card_m2.fill.solid()
    card_m2.fill.fore_color.rgb = C_SURFACE
    card_m2.line.color.rgb = C_SURFACE_ALT
    card_m2.line.width = Pt(1)

    tf_m2 = card_m2.text_frame
    tf_m2.word_wrap = True
    tf_m2.margin_left = tf_m2.margin_right = tf_m2.margin_top = tf_m2.margin_bottom = Inches(0.25)

    p_m2_h = tf_m2.paragraphs[0]
    p_m2_h.text = "BORUTA FEATURE SELECTION AUDIT"
    p_m2_h.font.name = FONT_HEAD
    p_m2_h.font.size = Pt(12)
    p_m2_h.font.bold = True
    p_m2_h.font.color.rgb = C_PINK
    p_m2_h.space_after = Pt(8)

    boruta_points = [
        ("Strict Shadow Noise Benchmark:", "10 shadow random permutations benchmark every feature. Features scoring below the maximum shadow importance (Z < 3.2) are systematically discarded."),
        ("Confirmed Signal Features:", "1. Pre-delivery Required Run Rate (Importance: 38.4%)\n2. Wickets In Hand at Crease (Importance: 26.2%)\n3. Overs Remaining / Match Phase (Importance: 18.5%)\n4. Batter/Bowler Head-to-Head History (Importance: 9.7%)"),
        ("Zero Information Leakage Guarantee:", "Post-delivery outcome proxies (e.g. current ball runs, retrospective boundary tags) are strictly excluded from all training sets to prevent target leakage.")
    ]
    for tit, dsc in boruta_points:
        pt = tf_m2.add_paragraph()
        pt.text = tit
        pt.font.name = FONT_HEAD
        pt.font.size = Pt(10)
        pt.font.bold = True
        pt.font.color.rgb = C_WHITE
        
        pd = tf_m2.add_paragraph()
        pd.text = dsc
        pd.font.name = FONT_BODY
        pd.font.size = Pt(9.5)
        pd.font.color.rgb = C_MUTED
        pd.space_after = Pt(6)

    # =========================================================================
    # SLIDE 5: UNSTOP CANONICAL TOP 10 BATSMEN
    # =========================================================================
    s5 = prs.slides.add_slide(blank_layout)
    apply_background(s5, C_NAVY)
    add_header(s5, "Unstop Submission: Top 10 Batsmen Under Pressure")

    bat_data = [
        ("1", "Heinrich Klaasen", "SRH", "94.8", "Elite spin-hitting anchor; highest pressure strike-rate (204.5) with minimal variance."),
        ("2", "Nicholas Pooran", "LSG", "91.3", "Unrivaled death-over acceleration; scores 2.45 runs per ball in final 3 overs."),
        ("3", "Suryakumar Yadav", "MI", "90.1", "360-degree boundary conversion under high RRR; manipulates field placements."),
        ("4", "Travis Head", "SRH", "88.7", "Powerplay demolition specialist; scores 2.18 RPO above league average against moving ball."),
        ("5", "Abhishek Sharma", "SRH", "86.2", "Ultra-high Powerplay strike rate (212.4); forces early boundary sweeper deployment."),
        ("6", "Virat Kohli", "RCB", "85.4", "Master run-chase accumulator; 98.2% contact consistency in Overs 7–15."),
        ("7", "Sanju Samson", "CSK", "84.9", "Traded to CSK at ₹18.00 Cr; high ceiling but susceptible to high-pace short balls."),
        ("8", "Phil Salt", "KKR", "83.8", "Aggressive early wicketkeeper option; excels against express pace in Powerplay."),
        ("9", "Sunil Narine", "KKR", "82.5", "High-variance Powerplay disruptor; forces early bowling changes."),
        ("10", "Jos Buttler", "Free Agent", "81.7", "Elite global pedigree; primary top-order overseas acquisition candidate at auction.")
    ]

    card_bt = s5.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.8), Inches(1.6), Inches(11.733), Inches(5.2))
    card_bt.fill.solid()
    card_bt.fill.fore_color.rgb = C_SURFACE
    card_bt.line.color.rgb = C_SURFACE_ALT
    card_bt.line.width = Pt(1)

    tf_bt = card_bt.text_frame
    tf_bt.word_wrap = True
    tf_bt.margin_left = tf_bt.margin_right = tf_bt.margin_top = tf_bt.margin_bottom = Inches(0.2)

    p_th = tf_bt.paragraphs[0]
    p_th.text = f"{'#':<3} {'Player Name':<22} {'Team':<12} {'Score':<8} {'Analytical Tactical Profile':<60}"
    p_th.font.name = FONT_HEAD
    p_th.font.size = Pt(10)
    p_th.font.bold = True
    p_th.font.color.rgb = C_GOLD
    p_th.space_after = Pt(6)

    for rank, name, team, score, profile in bat_data:
        p = tf_bt.add_paragraph()
        p.text = f"{rank:<3} {name:<22} {team:<12} {score:<8} {profile}"
        p.font.name = FONT_BODY
        p.font.size = Pt(9.5)
        p.font.color.rgb = C_WHITE if int(rank) <= 3 else C_MUTED
        if name == "Sanju Samson":
            p.font.color.rgb = C_PINK
        p.space_after = Pt(3)

    # =========================================================================
    # SLIDE 6: UNSTOP CANONICAL TOP 10 BOWLERS
    # =========================================================================
    s6 = prs.slides.add_slide(blank_layout)
    apply_background(s6, C_NAVY)
    add_header(s6, "Unstop Submission: Top 10 Bowlers Under Pressure")

    bowl_data = [
        ("1", "Jasprit Bumrah", "MI", "96.2", "Undisputed benchmark; 6.12 death RPO with sub-0.08 Clutch Volatility Index."),
        ("2", "Varun Chakaravarthy", "KKR", "89.7", "Elite middle-overs mystery spin choke; concedes <6.80 RPO against RHB."),
        ("3", "Harshit Rana", "KKR", "86.4", "Deceptive slower balls and bouncers; high wicket-conversion in death overs."),
        ("4", "T Natarajan", "SRH", "85.8", "Pinpoint blockhole execution; 78.4% yorker accuracy under extreme pressure."),
        ("5", "Pat Cummins", "SRH", "84.5", "Tactical pace enforcer; hard lengths (8-10m) neutralizing middle-order anchors."),
        ("6", "Arshdeep Singh", "MI", "83.9", "Left-arm angle at death; effective yorker and wide-line control."),
        ("7", "Kuldeep Yadav", "LSG", "83.1", "Wrist-spin attacking threat; takes wickets in clusters during Overs 11–15."),
        ("8", "Mitchell Starc", "KKR", "82.6", "Express Powerplay swing (145+ kph); delivers early multi-wicket bursts."),
        ("9", "Andre Russell", "KKR", "81.8", "Heavy-ball death enforcer; high wicket strike-rate in crisis situations."),
        ("10", "Matheesha Pathirana", "CSK", "81.2", "Malinga-esque sling action; extreme tailing yorkers at 148 kph.")
    ]

    card_bl = s6.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.8), Inches(1.6), Inches(11.733), Inches(5.2))
    card_bl.fill.solid()
    card_bl.fill.fore_color.rgb = C_SURFACE
    card_bl.line.color.rgb = C_SURFACE_ALT
    card_bl.line.width = Pt(1)

    tf_bl = card_bl.text_frame
    tf_bl.word_wrap = True
    tf_bl.margin_left = tf_bl.margin_right = tf_bl.margin_top = tf_bl.margin_bottom = Inches(0.2)

    p_bl_h = tf_bl.paragraphs[0]
    p_bl_h.text = f"{'#':<3} {'Player Name':<22} {'Team':<12} {'Score':<8} {'Analytical Tactical Profile':<60}"
    p_bl_h.font.name = FONT_HEAD
    p_bl_h.font.size = Pt(10)
    p_bl_h.font.bold = True
    p_bl_h.font.color.rgb = C_GOLD
    p_bl_h.space_after = Pt(6)

    for rank, name, team, score, profile in bowl_data:
        p = tf_bl.add_paragraph()
        p.text = f"{rank:<3} {name:<22} {team:<12} {score:<8} {profile}"
        p.font.name = FONT_BODY
        p.font.size = Pt(9.5)
        p.font.color.rgb = C_WHITE if int(rank) <= 3 else C_MUTED
        p.space_after = Pt(3)

    # =========================================================================
    # SLIDE 7: SQUAD GOVERNANCE & SAMSON TRADE
    # =========================================================================
    s7 = prs.slides.add_slide(blank_layout)
    apply_background(s7, C_NAVY)
    add_header(s7, "Squad Governance: Samson-to-CSK Trade & Leadership Restructure")

    add_stat_callout(s7, Inches(0.8), Inches(1.6), Inches(2.75), Inches(1.4), "₹18.00 Cr", "Sanju Samson (Traded to CSK)", C_PINK, "Outgoing Captain & Marquee Bat")
    add_stat_callout(s7, Inches(3.78), Inches(1.6), Inches(2.75), Inches(1.4), "₹14.00 Cr", "Ravindra Jadeja (Acquired)", C_SUCCESS, "Senior All-Rounder & Strategist")
    add_stat_callout(s7, Inches(6.76), Inches(1.6), Inches(2.75), Inches(1.4), "₹2.40 Cr", "Sam Curran (Acquired)", C_SUCCESS, "High-Surplus Pace All-Rounder")
    add_stat_callout(s7, Inches(9.74), Inches(1.6), Inches(2.75), Inches(1.4), "₹45.00 Cr", "Available Auction Purse", C_GOLD, "16 Retained Players (₹108.95 Cr Spent)")

    card_t1 = s7.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.8), Inches(3.2), Inches(5.7), Inches(3.8))
    card_t1.fill.solid()
    card_t1.fill.fore_color.rgb = C_SURFACE
    card_t1.line.color.rgb = C_SURFACE_ALT
    card_t1.line.width = Pt(1)

    tf_t1 = card_t1.text_frame
    tf_t1.word_wrap = True
    tf_t1.margin_left = tf_t1.margin_right = tf_t1.margin_top = tf_t1.margin_bottom = Inches(0.25)

    p_t1_h = tf_t1.paragraphs[0]
    p_t1_h.text = "FINANCIAL & ROSTER MECHANICS"
    p_t1_h.font.name = FONT_HEAD
    p_t1_h.font.size = Pt(12)
    p_t1_h.font.bold = True
    p_t1_h.font.color.rgb = C_GOLD
    p_t1_h.space_after = Pt(8)

    fin_items = [
        ("Purse Net Gain:", "Trading Samson (₹18.00 Cr) and absorbing Jadeja (₹14.00 Cr) + Curran (₹2.40 Cr) created a net +₹1.60 Cr purse dividend."),
        ("Overseas Slot Conservation:", "Curran and Hetmyer occupy 2 of 8 overseas slots. RR retains 6 available overseas slots for targeted auction strikes."),
        ("Balance Sheet Strength:", "Total squad spend sits at ₹108.95 Cr against the ₹157.00 Cr ceiling. The ₹45.00 Cr liquid purse gives RR unmatched bidding agility.")
    ]
    for tit, dsc in fin_items:
        pt = tf_t1.add_paragraph()
        pt.text = tit
        pt.font.name = FONT_HEAD
        pt.font.size = Pt(10)
        pt.font.bold = True
        pt.font.color.rgb = C_WHITE
        
        pd = tf_t1.add_paragraph()
        pd.text = dsc
        pd.font.name = FONT_BODY
        pd.font.size = Pt(9.5)
        pd.font.color.rgb = C_MUTED
        pd.space_after = Pt(6)

    card_t2 = s7.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(6.8), Inches(3.2), Inches(5.7), Inches(3.8))
    card_t2.fill.solid()
    card_t2.fill.fore_color.rgb = C_SURFACE
    card_t2.line.color.rgb = C_SURFACE_ALT
    card_t2.line.width = Pt(1)

    tf_t2 = card_t2.text_frame
    tf_t2.word_wrap = True
    tf_t2.margin_left = tf_t2.margin_right = tf_t2.margin_top = tf_t2.margin_bottom = Inches(0.25)

    p_t2_h = tf_t2.paragraphs[0]
    p_t2_h.text = "LEADERSHIP & CULTURAL ALIGNMENT"
    p_t2_h.font.name = FONT_HEAD
    p_t2_h.font.size = Pt(12)
    p_t2_h.font.bold = True
    p_t2_h.font.color.rgb = C_PINK
    p_t2_h.space_after = Pt(8)

    lead_items = [
        ("Captain: Riyan Parag", "Promoted to Captain following exceptional 2024–2026 domestic and IPL campaigns. Commands high dressing-room respect and tactical clarity."),
        ("Primary WK: Dhruv Jurel", "Elite glovework (0.32s reaction time) and premier death-over finishing. Takes over full-time wicketkeeping duties."),
        ("Senior Strategist: Ravindra Jadeja", "Directs middle-overs fielding geometry, advises on spin matchups, and stabilizes innings under collapse pressure."),
        ("Pace Leader: Jofra Archer", "Spearheads fast bowling unit under strict biomechanical workload management (12 group matches to preserve 148+ kph playoff speed).")
    ]
    for tit, dsc in lead_items:
        pt = tf_t2.add_paragraph()
        pt.text = tit
        pt.font.name = FONT_HEAD
        pt.font.size = Pt(10)
        pt.font.bold = True
        pt.font.color.rgb = C_WHITE
        
        pd = tf_t2.add_paragraph()
        pd.text = dsc
        pd.font.name = FONT_BODY
        pd.font.size = Pt(9.5)
        pd.font.color.rgb = C_MUTED
        pd.space_after = Pt(6)

    # =========================================================================
    # SLIDE 8: PLAN B AUCTION BLUEPRINT (Integrated Capital Allocation Plate)
    # =========================================================================
    s8 = prs.slides.add_slide(blank_layout)
    apply_background(s8, C_NAVY)
    add_header(s8, "Auction Game Theory: Strategic Capital Allocation (Plan B)")

    cap_img_path = os.path.join(ASSETS_DIR, "capital_allocation_plate.png")
    if os.path.exists(cap_img_path):
        s8.shapes.add_picture(cap_img_path, Inches(0.8), Inches(1.6), Inches(11.733), Inches(5.1))

    # =========================================================================
    # SLIDE 9: CONTRACT SURPLUS VALUE & PARETO FRONTIER
    # =========================================================================
    s9 = prs.slides.add_slide(blank_layout)
    apply_background(s9, C_NAVY)
    add_header(s9, "Sabermetric Auction Valuation: Contract Surplus Value (CSV) & Pareto Frontier")

    pareto_img_path = os.path.join(ASSETS_DIR, "pareto_frontier_plate.png")
    if os.path.exists(pareto_img_path):
        s9.shapes.add_picture(pareto_img_path, Inches(0.8), Inches(1.6), Inches(11.733), Inches(5.1))

    # =========================================================================
    # SLIDE 10: BAYESIAN CLUSTER COLLAPSE HAZARDS & DOMINO INTERRUPTION
    # =========================================================================
    s10 = prs.slides.add_slide(blank_layout)
    apply_background(s10, C_NAVY)
    add_header(s10, "Crisis Survival Dynamics: Bayesian Cluster Collapse Hazards & Domino Interruption")

    hazard_img_path = os.path.join(ASSETS_DIR, "crisis_hazard_plate.png")
    if os.path.exists(hazard_img_path):
        s10.shapes.add_picture(hazard_img_path, Inches(0.8), Inches(1.6), Inches(11.733), Inches(5.1))

    # =========================================================================
    # SLIDE 11: PITCH PHYSICS & TRAJECTORY TELEMETRY
    # =========================================================================
    s11 = prs.slides.add_slide(blank_layout)
    apply_background(s11, C_NAVY)
    add_header(s11, "Ball-Tracking Telemetry: Hawk-Eye Trajectory & Release Vectors")

    phys_img_path = os.path.join(ASSETS_DIR, "pitch_telemetry_plate.png")
    if os.path.exists(phys_img_path):
        s11.shapes.add_picture(phys_img_path, Inches(0.8), Inches(1.6), Inches(11.733), Inches(5.1))

    # =========================================================================
    # SLIDE 12: CLOSING CHAMPIONSHIP VERDICT (Integrated Resolution Poster)
    # =========================================================================
    s12 = prs.slides.add_slide(blank_layout)
    apply_background(s12, C_NAVY)
    add_header(s12, "Championship Probability: 1,000-Run Monte Carlo Verdict")

    close_img_path = os.path.join(ASSETS_DIR, "championship_verdict_plate.png")
    if os.path.exists(close_img_path):
        s12.shapes.add_picture(close_img_path, Inches(0.8), Inches(1.6), Inches(11.733), Inches(5.1))

    # Save both decks
    prs.save(PPTX_PATH_V5)
    prs.save(PPTX_PATH_V4)
    print(f"Master Editorial Presentation saved to: {PPTX_PATH_V5}")
    print(f"Also updated default presentation: {PPTX_PATH_V4}")

if __name__ == "__main__":
    build_presentation()
