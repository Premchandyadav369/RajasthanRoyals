"""
Generates an Executive 10-Slide Widescreen PowerPoint Presentation (16:9)
Project RR-EDGE V4.2: Rajasthan Royals Franchise Decision Intelligence Suite
Styled with RR Official Palette: Royal Pink #EA1A85, Deep Navy #0B132B, Imperial Gold #D4AF37
"""

import os
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.enum.text import PP_ALIGN
from pptx.dml.color import RGBColor

BASE_DIR = r"C:\Users\PREMCHANDYADAV\Downloads\RR_Competition"
PPTX_PATH = os.path.join(BASE_DIR, "RR_EDGE_V4_2_Presentation.pptx")

# Color Constants
C_NAVY = RGBColor(11, 19, 43)        # #0B132B
C_SURFACE = RGBColor(19, 30, 61)     # #131E3D
C_PINK = RGBColor(234, 26, 133)      # #EA1A85
C_GOLD = RGBColor(212, 175, 55)      # #D4AF37
C_WHITE = RGBColor(255, 255, 255)
C_MUTED = RGBColor(148, 163, 184)    # #94A3B8

def create_deck():
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    blank_layout = prs.slide_layouts[6]

    def set_slide_background(slide, color=C_NAVY):
        bg = slide.background
        fill = bg.fill
        fill.solid()
        fill.fore_color.rgb = color

    def add_slide_header(slide, title, category="PROJECT RR-EDGE V4.2 | RAJASTHAN ROYALS"):
        txBox = slide.shapes.add_textbox(Inches(0.8), Inches(0.4), Inches(11.7), Inches(1.1))
        tf = txBox.text_frame
        tf.word_wrap = True
        
        p_cat = tf.paragraphs[0]
        p_cat.text = category.upper()
        p_cat.font.size = Pt(11)
        p_cat.font.bold = True
        p_cat.font.color.rgb = C_PINK
        
        p_title = tf.add_paragraph()
        p_title.text = title.upper()
        p_title.font.size = Pt(24)
        p_title.font.bold = True
        p_title.font.color.rgb = C_WHITE

    # -------------------------------------------------------------
    # SLIDE 1: TITLE SLIDE
    # -------------------------------------------------------------
    s1 = prs.slides.add_slide(blank_layout)
    set_slide_background(s1, C_NAVY)
    
    tb1 = s1.shapes.add_textbox(Inches(1.0), Inches(1.8), Inches(11.3), Inches(4.0))
    tf1 = tb1.text_frame
    tf1.word_wrap = True
    
    p = tf1.paragraphs[0]
    p.text = "👑 RAJASTHAN ROYALS • HALLA BOL"
    p.font.size = Pt(16)
    p.font.bold = True
    p.font.color.rgb = C_GOLD
    p.space_after = Pt(14)
    
    p2 = tf1.add_paragraph()
    p2.text = "PROJECT RR-EDGE V4.2"
    p2.font.size = Pt(44)
    p2.font.bold = True
    p2.font.color.rgb = C_PINK
    
    p3 = tf1.add_paragraph()
    p3.text = "IPL 2027 Franchise Decision Intelligence & Auction Blueprint"
    p3.font.size = Pt(22)
    p3.font.color.rgb = C_WHITE
    p3.space_after = Pt(28)
    
    p4 = tf1.add_paragraph()
    p4.text = "SupeRR Selector Season 2 | 200,999 Deliveries Evaluated | Pre-Delivery Bayesian Engine"
    p4.font.size = Pt(14)
    p4.font.color.rgb = C_MUTED

    # -------------------------------------------------------------
    # SLIDE 2: EXECUTIVE SUMMARY & CORE CHALLENGE
    # -------------------------------------------------------------
    s2 = prs.slides.add_slide(blank_layout)
    set_slide_background(s2, C_NAVY)
    add_slide_header(s2, "Executive Summary: The Championship Mandate")
    
    tb2 = s2.shapes.add_textbox(Inches(0.8), Inches(1.6), Inches(11.7), Inches(5.2))
    tf2 = tb2.text_frame
    tf2.word_wrap = True
    
    points_s2 = [
        ("The Strategic Core", "Rajasthan Royals hit a tournament-high 181 sixes in IPL 2026 and posted an 11.13 Powerplay run-rate, yet fell short in Qualifier 2. The deficit was entirely in bowling phase defense."),
        ("The Forensic Truth", "Between overs 7 and 11, RR leaked 10.29 runs per over (second-worst in the IPL) with an average wicketless drift of 8.4 overs. Opponents consistently erased RR's early advantage."),
        ("The Trade Reality", "Sanju Samson's trade to CSK at ₹18.00 Cr and the return of Ravindra Jadeja (₹14.00 Cr) and Sam Curran (₹2.40 Cr) sets the foundation for a rebalanced tactical structure with Dhruv Jurel as wicketkeeper and Riyan Parag as captain."),
        ("The Plan B Solution", "By unlocking ₹45.00 Cr from non-core contracts, RR targets Matt Henry (PP wickets) and Suyash Sharma (middle spin choke), elevating tournament playoff probability from 52.2% to 68.4%.")
    ]
    for head, body in points_s2:
        p_h = tf2.add_paragraph()
        p_h.text = f"• {head}: "
        p_h.font.bold = True
        p_h.font.size = Pt(15)
        p_h.font.color.rgb = C_GOLD
        
        p_b = tf2.add_paragraph()
        p_b.text = f"   {body}"
        p_b.font.size = Pt(13)
        p_b.font.color.rgb = C_WHITE
        p_b.space_after = Pt(10)

    # -------------------------------------------------------------
    # SLIDE 3: 2026 SEASON DIAGNOSTIC (OVERS 7-11 LEAK)
    # -------------------------------------------------------------
    s3 = prs.slides.add_slide(blank_layout)
    set_slide_background(s3, C_NAVY)
    add_slide_header(s3, "2026 Diagnostic: The Phase Choke Point")
    
    # Left Box
    tb3_l = s3.shapes.add_textbox(Inches(0.8), Inches(1.8), Inches(5.6), Inches(4.8))
    tf3_l = tb3_l.text_frame
    tf3_l.word_wrap = True
    p = tf3_l.paragraphs[0]
    p.text = "BATTERY OF STRENGTHS (VANITY METRICS)"
    p.font.size = Pt(14)
    p.font.bold = True
    p.font.color.rgb = C_GOLD
    p.space_after = Pt(12)
    
    strengths = [
        ("181 Sixes", "Tournament #1 boundary-hitting power"),
        ("11.13 PP RPO", "All 16 matches (11.72 RPO in 8 wins)"),
        ("Yashasvi Jaiswal", "Orange Cap contender with 162.4 pace SR"),
        ("Jofra Archer", "Spearheaded attack with 25 tournament wickets")
    ]
    for m, d in strengths:
        pm = tf3_l.add_paragraph()
        pm.text = f"✔ {m}: {d}"
        pm.font.size = Pt(13)
        pm.font.color.rgb = C_WHITE
        pm.space_after = Pt(8)
        
    # Right Box
    tb3_r = s3.shapes.add_textbox(Inches(6.8), Inches(1.8), Inches(5.6), Inches(4.8))
    tf3_r = tb3_r.text_frame
    tf3_r.word_wrap = True
    p = tf3_r.paragraphs[0]
    p.text = "THE FATAL LEAK (ACTUAL DEFICIT)"
    p.font.size = Pt(14)
    p.font.bold = True
    p.font.color.rgb = C_PINK
    p.space_after = Pt(12)
    
    leaks = [
        ("10.29 RPO Leaked", "Conceded in overs 7–11 across all matches"),
        ("8.4 Overs Drift", "Longest middle-overs wicketless spell in top 4"),
        ("Spin Squeeze Failure", "9.71 league middle economy surrendered leverage"),
        ("Over-Reliance on Top 3", "Lower order collapsed under pressure in Q2")
    ]
    for m, d in leaks:
        pm = tf3_r.add_paragraph()
        pm.text = f"✘ {m}: {d}"
        pm.font.size = Pt(13)
        pm.font.color.rgb = C_WHITE
        pm.space_after = Pt(8)

    # -------------------------------------------------------------
    # SLIDE 4: 200,999-BALL SCIENTIFIC METHODOLOGY
    # -------------------------------------------------------------
    s4 = prs.slides.add_slide(blank_layout)
    set_slide_background(s4, C_NAVY)
    add_slide_header(s4, "Scientific Methodology: Zero-Leakage Bayesian Modeling")
    
    tb4 = s4.shapes.add_textbox(Inches(0.8), Inches(1.6), Inches(11.7), Inches(5.2))
    tf4 = tb4.text_frame
    tf4.word_wrap = True
    
    methods = [
        ("1. Zero-Target Leakage Guarantee", "Every delivery is evaluated strictly using pre-delivery match state (RRR, balls remaining, wickets in hand, target score, knockout multiplier). No post-delivery outcomes bias the context."),
        ("2. Empirical Competition Calibration", "League difficulty calibrated against IPL as the 1.000 benchmark (T20 World Cup: 0.965, T20I: 0.920, Domestic: 0.850) across 883 matches."),
        ("3. LightGBM Expected Metrics (xR & xW)", "Expected Runs and Expected Wickets models trained across 200,999 balls to establish replacement baselines for every phase of play."),
        ("4. Bayesian Shrinkage Prior", "Outlier performances with low sample sizes (e.g. Ashutosh Sharma, Shubham Dubey) are shrunk toward the population mean to prevent over-bidding on high-variance players."),
        ("5. Monte Carlo Schedule Engine", "1,000 full IPL seasons simulated incorporating venue micro-climates, dew factors, and player availability distributions.")
    ]
    for h, b in methods:
        p_h = tf4.add_paragraph()
        p_h.text = f"{h}: "
        p_h.font.bold = True
        p_h.font.size = Pt(14)
        p_h.font.color.rgb = C_GOLD
        
        p_b = tf4.add_paragraph()
        p_b.text = f"   {b}"
        p_b.font.size = Pt(12)
        p_b.font.color.rgb = C_WHITE
        p_b.space_after = Pt(6)

    # -------------------------------------------------------------
    # SLIDE 5: TOP 10 BATSMEN UNDER PRESSURE
    # -------------------------------------------------------------
    s5 = prs.slides.add_slide(blank_layout)
    set_slide_background(s5, C_NAVY)
    add_slide_header(s5, "Primary Competition Rankings: Top 10 Batsmen")
    
    rows, cols = 11, 4
    table_shape = s5.shapes.add_table(rows, cols, Inches(0.8), Inches(1.6), Inches(11.7), Inches(5.2))
    table = table_shape.table
    
    headers = ["Rank & Player Name", "Franchise Context", "Pressure Metric", "Tactical Profile"]
    for i, h in enumerate(headers):
        cell = table.cell(0, i)
        cell.text = h
        cell.fill.solid()
        cell.fill.fore_color.rgb = C_SURFACE
        p = cell.text_frame.paragraphs[0]
        p.font.bold = True
        p.font.size = Pt(12)
        p.font.color.rgb = C_GOLD

    top_bats = [
        ("1. Heinrich Klaasen", "SRH", "171.4 SR | 100.0 PBRS", "Global benchmark spin & pace execution"),
        ("2. Nicholas Pooran", "LSG", "178.2 SR | 97.4 PBRS", "Middle-overs match-impact accelerator"),
        ("3. Suryakumar Yadav", "MI", "178.3 SR | 95.8 PBRS", "360-degree all-phase pressure anchor"),
        ("4. Travis Head", "SRH", "191.6 SR | 94.1 PBRS", "Extreme Powerplay boundary enforcer"),
        ("5. Abhishek Sharma", "SRH", "182.4 SR | 92.5 PBRS", "High-frequency Powerplay aggressor"),
        ("6. Virat Kohli", "RCB", "148.5 SR | 91.2 PBRS", "Anchor with 64.2% chase win rate"),
        ("7. Sanju Samson", "CSK (Traded)", "177.7 SR | 89.8 PBRS", "Top-order acceleration under pressure"),
        ("8. Phil Salt", "KKR", "182.0 SR | 88.6 PBRS", "Explosive Powerplay wicket-taker pressure"),
        ("9. Sunil Narine", "KKR", "180.5 SR | 87.5 PBRS", "High-variance disruptive pinch opener"),
        ("10. Jos Buttler", "Free Agent", "197.8 SR | 86.9 PBRS", "Proven playoff match-winning finisher")
    ]
    for r_idx, row_data in enumerate(top_bats):
        for c_idx, val in enumerate(row_data):
            cell = table.cell(r_idx + 1, c_idx)
            cell.text = val
            cell.fill.solid()
            cell.fill.fore_color.rgb = RGBColor(15, 23, 42)
            p = cell.text_frame.paragraphs[0]
            p.font.size = Pt(11)
            p.font.color.rgb = C_WHITE if c_idx != 2 else C_PINK

    # -------------------------------------------------------------
    # SLIDE 6: TOP 10 BOWLERS UNDER PRESSURE
    # -------------------------------------------------------------
    s6 = prs.slides.add_slide(blank_layout)
    set_slide_background(s6, C_NAVY)
    add_slide_header(s6, "Primary Competition Rankings: Top 10 Bowlers")
    
    table_shape_b = s6.shapes.add_table(rows, cols, Inches(0.8), Inches(1.6), Inches(11.7), Inches(5.2))
    table_b = table_shape_b.table
    
    headers_b = ["Rank & Bowler Name", "Franchise Context", "Economy & PBwRS", "Tactical Execution"]
    for i, h in enumerate(headers_b):
        cell = table_b.cell(0, i)
        cell.text = h
        cell.fill.solid()
        cell.fill.fore_color.rgb = C_SURFACE
        p = cell.text_frame.paragraphs[0]
        p.font.bold = True
        p.font.size = Pt(12)
        p.font.color.rgb = C_GOLD

    top_bowls = [
        ("1. Jasprit Bumrah", "MI", "6.48 Death Econ | 100.0 PBwRS", "Gold standard death & yorker execution"),
        ("2. Varun Chakaravarthy", "KKR", "6.95 Mid Econ | 96.8 PBwRS", "Mystery spin middle-overs choke master"),
        ("3. Harshit Rana", "KKR", "8.20 Death Econ | 94.5 PBwRS", "Heavy ball & slower cutter specialist"),
        ("4. T Natarajan", "SRH (Traded)", "8.35 Death Econ | 93.2 PBwRS", "41.2% yorker frequency under pressure"),
        ("5. Pat Cummins", "SRH", "8.40 Death Econ | 91.8 PBwRS", "High-leverage enforcer pace & tactics"),
        ("6. Arshdeep Singh", "MI (Traded)", "8.55 Death Econ | 90.5 PBwRS", "Left-arm swing and wide yorker control"),
        ("7. Kuldeep Yadav", "LSG (Traded)", "7.15 Mid Econ | 89.2 PBwRS", "Left-arm wrist spin partnership breaker"),
        ("8. Mitchell Starc", "KKR", "8.65 Death Econ | 88.0 PBwRS", "145+ kph playoff high-stakes spearhead"),
        ("9. Andre Russell", "KKR", "8.75 Death Econ | 87.1 PBwRS", "Bodyline bouncer & death over-enforcer"),
        ("10. Matheesha Pathirana", "CSK", "8.22 Death Econ | 86.4 PBwRS", "Sling action trajectory dip & yorkers")
    ]
    for r_idx, row_data in enumerate(top_bowls):
        for c_idx, val in enumerate(row_data):
            cell = table_b.cell(r_idx + 1, c_idx)
            cell.text = val
            cell.fill.solid()
            cell.fill.fore_color.rgb = RGBColor(15, 23, 42)
            p = cell.text_frame.paragraphs[0]
            p.font.size = Pt(11)
            p.font.color.rgb = C_WHITE if c_idx != 2 else C_GOLD

    # -------------------------------------------------------------
    # SLIDE 7: REAL-TIME ROSTER & THE HISTORIC TRADE
    # -------------------------------------------------------------
    s7 = prs.slides.add_slide(blank_layout)
    set_slide_background(s7, C_NAVY)
    add_slide_header(s7, "Real-Time Roster Structure & The Historic Trade")
    
    tb7 = s7.shapes.add_textbox(Inches(0.8), Inches(1.6), Inches(11.7), Inches(5.2))
    tf7 = tb7.text_frame
    tf7.word_wrap = True
    
    trade_points = [
        ("The Sanju Samson Trade to CSK", "On 15 Nov 2025, Sanju Samson was officially traded to Chennai Super Kings at his existing ₹18.00 Cr contract, becoming CSK's marquee pillar."),
        ("The Homecoming of Ravindra Jadeja", "In exchange, Ravindra Jadeja returned to Rajasthan Royals at a revised league fee of ₹14.00 Cr, bringing elite SLA control and lower-order stability."),
        ("Sam Curran Acquired in Swap", "English all-rounder Sam Curran was traded alongside Jadeja to RR for ₹2.40 Cr, providing vital left-arm pace depth."),
        ("Franchise Leadership Reorganization", "Riyan Parag is appointed official Franchise Captain, with Ravindra Jadeja serving as senior on-field leader."),
        ("Dhruv Jurel Locked as Wicketkeeper", "Dhruv Jurel (₹14.00 Cr Retained) takes over as RR's undisputed #1 wicketkeeper-batter (backed by Donovan Ferreira).")
    ]
    for h, b in trade_points:
        p_h = tf7.add_paragraph()
        p_h.text = f"✔ {h}: "
        p_h.font.bold = True
        p_h.font.size = Pt(14)
        p_h.font.color.rgb = C_PINK
        
        p_b = tf7.add_paragraph()
        p_b.text = f"   {b}"
        p_b.font.size = Pt(12)
        p_b.font.color.rgb = C_WHITE
        p_b.space_after = Pt(8)

    # -------------------------------------------------------------
    # SLIDE 8: PLAN B AUCTION BLUEPRINT & TARGETS
    # -------------------------------------------------------------
    s8 = prs.slides.add_slide(blank_layout)
    set_slide_background(s8, C_NAVY)
    add_slide_header(s8, "Plan B Auction Blueprint: Strategic Capital Deployment")
    
    tb8 = s8.shapes.add_textbox(Inches(0.8), Inches(1.6), Inches(11.7), Inches(5.2))
    tf8 = tb8.text_frame
    tf8.word_wrap = True
    
    p = tf8.paragraphs[0]
    p.text = "STATUTORY SALARY CAP: ₹157.00 Cr | RETAINED SPEND: ₹108.95 Cr | AUCTION PURSE: ₹45.00 Cr"
    p.font.size = Pt(13)
    p.font.bold = True
    p.font.color.rgb = C_GOLD
    p.space_after = Pt(14)
    
    targets_s8 = [
        ("TARGET 1: Matt Henry (Overseas Seam Spearhead)", "Fair Value: ₹10.50 Cr | Ceiling: ₹12.50 Cr", "6.65 PP economy with world-class outswing. Takes frontline Powerplay wickets to shield the middle overs."),
        ("TARGET 2: Suyash Sharma (Indian Mystery Wrist-Spin)", "Fair Value: ₹5.20 Cr | Ceiling: ₹6.80 Cr", "7.15 Middle economy. Operates in tandem with Ravi Bishnoi to choke overs 7–11 and create false shots."),
        ("BACKUP 1: Gerald Coetzee (Express Overseas Pacer)", "Fair Value: ₹6.80 Cr | Ceiling: ₹8.00 Cr", "148+ kph hit-the-deck pace to rotate with Jofra Archer across heavy travel schedules."),
        ("BACKUP 2: Allah Ghazanfar (Overseas Mystery Spinner)", "Fair Value: ₹4.50 Cr | Ceiling: ₹5.50 Cr", "High-variance wicket threat in gripping away conditions (e.g. Chepauk, Ekana).")
    ]
    for t_title, t_fin, t_desc in targets_s8:
        p_t = tf8.add_paragraph()
        p_t.text = f"🎯 {t_title}"
        p_t.font.bold = True
        p_t.font.size = Pt(14)
        p_t.font.color.rgb = C_WHITE
        
        p_f = tf8.add_paragraph()
        p_f.text = f"   {t_fin} — {t_desc}"
        p_f.font.size = Pt(12)
        p_f.font.color.rgb = C_MUTED
        p_f.space_after = Pt(10)

    # -------------------------------------------------------------
    # SLIDE 9: TACTICAL DECISION MODELS
    # -------------------------------------------------------------
    s9 = prs.slides.add_slide(blank_layout)
    set_slide_background(s9, C_NAVY)
    add_slide_header(s9, "Tactical Decision Models: Dynamic Overs & Entry Points")
    
    tb9 = s9.shapes.add_textbox(Inches(0.8), Inches(1.6), Inches(11.7), Inches(5.2))
    tf9 = tb9.text_frame
    tf9.word_wrap = True
    
    tactics = [
        ("Optimal 20-Over Bowling Plan (149.15 Expected Runs Conceded)", "Powerplay (Overs 1–6): Henry (1, 3, 5), Archer (2), Sandeep (4, 6)\nMiddle Squeeze (Overs 7–15): Bishnoi (7, 9, 11, 13), Suyash (8, 10, 12, 14), Henry (15)\nDeath Lockdown (Overs 16–20): Sandeep (16, 18), Archer (17, 19, 20)\n-> Saves 27.85 runs per match compared to 2026 baseline."),
        ("The Shimron Hetmyer Squeeze Constraint", "Deploying Hetmyer before Over 14 against active wrist-spin causes a 41.2% spike in dismissal hazard (SR 118.2). Plan B strictly reserves Hetmyer for Overs 14.2–20.0 against high-pace death bowling where his SR surges to 188.6."),
        ("Innings Stabilization Hierarchy", "Dhruv Jurel (86.4) and Ravindra Jadeja (84.1) lead the squad in innings stabilization under rapid-wicket collapse scenarios, rotating strike with low dot percentages.")
    ]
    for h, b in tactics:
        p_h = tf9.add_paragraph()
        p_h.text = f"⚙ {h}"
        p_h.font.bold = True
        p_h.font.size = Pt(14)
        p_h.font.color.rgb = C_GOLD
        
        p_b = tf9.add_paragraph()
        p_b.text = f"   {b}"
        p_b.font.size = Pt(12)
        p_b.font.color.rgb = C_WHITE
        p_b.space_after = Pt(12)

    # -------------------------------------------------------------
    # SLIDE 10: MONTE CARLO SIMULATION & CONCLUSION
    # -------------------------------------------------------------
    s10 = prs.slides.add_slide(blank_layout)
    set_slide_background(s10, C_NAVY)
    add_slide_header(s10, "Monte Carlo Validation & Tournament Conclusion")
    
    tb10 = s10.shapes.add_textbox(Inches(0.8), Inches(1.6), Inches(11.7), Inches(5.2))
    tf10 = tb10.text_frame
    tf10.word_wrap = True
    
    conclusions = [
        ("Playoff Qualification Probability: 68.4%", "1,000-run Monte Carlo tournament simulation confirms Plan B improves RR's playoff qualification probability by +16.2% over status-quo retention (52.2%)."),
        ("IPL Title Win Probability: 16.8%", "Second-highest in the competition behind SRH (18.2%), representing true championship contention."),
        ("Expected 14-Match Win Count: 9.1 Wins", "Median: 9 wins, 90th percentile: 11 wins. Reaches the critical 18-point threshold for a top-2 league finish."),
        ("Franchise Governance Compliance", "Strictly adheres to BCCI regulations: 3 Overseas in Starting XI, 8 Overseas total squad, ₹157.00 Cr salary cap compliance, verified zero pre-delivery data leakage."),
        ("Conclusion", "RR-EDGE V4.2 replaces speculation with empirical certainty. By fixing overs 7–11 through disciplined purse reallocation, Rajasthan Royals can lift the IPL 2027 trophy. Halla Bol!")
    ]
    for h, b in conclusions:
        p_h = tf10.add_paragraph()
        p_h.text = f"🏆 {h}"
        p_h.font.bold = True
        p_h.font.size = Pt(14)
        p_h.font.color.rgb = C_PINK
        
        p_b = tf10.add_paragraph()
        p_b.text = f"   {b}"
        p_b.font.size = Pt(12)
        p_b.font.color.rgb = C_WHITE
        p_b.space_after = Pt(8)

    prs.save(PPTX_PATH)
    print(f"Presentation saved successfully to: {PPTX_PATH}")

if __name__ == "__main__":
    create_deck()
