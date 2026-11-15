"""
Generation of Phase 17 PDF Reports & 1-Page Executive Summary Infographic
Generates:
1. RR_2027_Opponent_Analysis.pdf
2. RR_2027_Squad_Optimisation_Report.pdf
3. RR_EDGE_Executive_Summary.pdf
"""

import os
import pandas as pd
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, Image, HRFlowable
)
from reportlab.pdfgen import canvas

BASE_DIR = r"C:\Users\PREMCHANDYADAV\Downloads\RR_Competition"
CHARTS_DIR = os.path.join(BASE_DIR, "charts")

class NumberedCanvas(canvas.Canvas):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_header_footer(num_pages)
            super().showPage()
        super().save()

    def draw_header_footer(self, page_count):
        self.saveState()
        self.setFont("Helvetica", 8)
        self.setFillColor(colors.HexColor("#64748B"))
        
        if self._pageNumber > 1:
            self.drawString(54, 750, "PROJECT RR-EDGE | RAJASTHAN ROYALS IPL 2027 STRATEGY")
            self.drawRightString(558, 750, "CONFIDENTIAL & PROPRIETARY")
            self.setStrokeColor(colors.HexColor("#CBD5E1"))
            self.setLineWidth(0.5)
            self.line(54, 742, 558, 742)

        page_str = f"Page {self._pageNumber} of {page_count}"
        self.drawRightString(558, 36, page_str)
        self.drawString(54, 36, "AUCTION & SQUAD OPTIMIZATION ENGINE | SUPERR SELECTOR S2")
        self.setStrokeColor(colors.HexColor("#CBD5E1"))
        self.setLineWidth(0.5)
        self.line(54, 46, 558, 46)
        self.restoreState()


def build_opponent_analysis_pdf():
    pdf_path = os.path.join(BASE_DIR, "RR_2027_Opponent_Analysis.pdf")
    print(f"Building {pdf_path}...")
    doc = SimpleDocTemplate(pdf_path, pagesize=letter, leftMargin=54, rightMargin=54, topMargin=54, bottomMargin=54)
    styles = getSampleStyleSheet()

    title_style = ParagraphStyle('OppTitle', parent=styles['Heading1'], fontName='Helvetica-Bold', fontSize=18, leading=22, textColor=colors.HexColor("#0077B6"), spaceAfter=6)
    subtitle_style = ParagraphStyle('OppSub', parent=styles['Normal'], fontName='Helvetica', fontSize=10, leading=14, textColor=colors.HexColor("#FF007F"), spaceAfter=12)
    h1_style = ParagraphStyle('OppH1', parent=styles['Heading2'], fontName='Helvetica-Bold', fontSize=12, leading=16, textColor=colors.HexColor("#1E293B"), spaceBefore=10, spaceAfter=4, keepWithNext=True)
    body_style = ParagraphStyle('OppBody', parent=styles['Normal'], fontName='Helvetica', fontSize=8, leading=11.5, textColor=colors.HexColor("#334155"), spaceAfter=5)
    bullet_style = ParagraphStyle('OppBullet', parent=body_style, leftIndent=12, firstLineIndent=-8, spaceAfter=3)
    
    cell_style = ParagraphStyle('OCell', parent=styles['Normal'], fontName='Helvetica', fontSize=7, leading=9)
    cell_bold = ParagraphStyle('OCellB', parent=cell_style, fontName='Helvetica-Bold')
    cell_hdr = ParagraphStyle('OCellH', parent=cell_style, fontName='Helvetica-Bold', textColor=colors.white)

    story = []
    story.append(Paragraph("PROJECT RR-EDGE: IPL 2027 OPPONENT TACTICAL INTELLIGENCE", title_style))
    story.append(Paragraph("<b>Comprehensive Threat Diagnostics, Phase Vulnerabilities & Matchup Solutions for All 9 Rivals</b>", subtitle_style))
    story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor("#0077B6"), spaceBefore=2, spaceAfter=10))

    story.append(Paragraph("1. Competitive Context Post-November 2026 Blockbuster Trades", h1_style))
    exec_text = (
        "Following the confirmed trades locked ahead of the November 17, 2026 retention deadline, the competitive hierarchy has shifted dramatically. "
        "<b>Sunrisers Hyderabad</b> emerged as major trade winners, completely overhauling their death bowling by acquiring T. Natarajan (₹5 Cr), "
        "Khaleel Ahmed (₹4.8 Cr), and Nathan Ellis (₹2 Cr) alongside Pat Cummins. <b>Mumbai Indians</b> paired Arshdeep Singh (₹18 Cr trade) with Jasprit Bumrah. "
        "<b>Punjab Kings</b> landed Hardik Pandya (₹18 Cr), while <b>Lucknow Super Giants</b> acquired Kuldeep Yadav (₹13.5 Cr). "
        "RR cannot simply match firepower—they must deploy exact phase matchups."
    )
    story.append(Paragraph(exec_text, body_style))

    # Opponent table
    opp_df = pd.read_csv(os.path.join(BASE_DIR, "RR_Opponent_Threat_Matrix.csv"))
    
    t_data = [
        [Paragraph("Opponent", cell_hdr), Paragraph("Threat Level", cell_hdr), Paragraph("Powerplay Threat", cell_hdr), Paragraph("Middle Overs (7-11)", cell_hdr), Paragraph("Death Threat", cell_hdr), Paragraph("RR Bowling Counter-Strategy", cell_hdr)]
    ]
    for _, r in opp_df.iterrows():
        t_data.append([
            Paragraph(r['opponent'][:18], cell_bold),
            Paragraph(r['threat_level'], cell_style),
            Paragraph(r['powerplay_profile'][:40], cell_style),
            Paragraph(r['middle_overs_7_11'][:40], cell_style),
            Paragraph(r['death_overs_16_20'][:40], cell_style),
            Paragraph(r['rr_bowling_counter'][:70], cell_style)
        ])
        
    t_opp = Table(t_data, colWidths=[80, 65, 80, 80, 80, 119])
    t_opp.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#0077B6")),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor("#CBD5E1")),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor("#F8FAFC")]),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('TOPPADDING', (0, 0), (-1, -1), 3),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 3)
    ]))
    story.append(t_opp)

    story.append(PageBreak())
    story.append(Paragraph("2. Tactical Opposition Matchup Matrix (Critical Pairings)", h1_style))
    story.append(Paragraph("Ball-by-ball empirical matchups to neutralize the league's most lethal batters:", body_style))

    matchup_df = pd.read_csv(os.path.join(BASE_DIR, "RR_Opposition_Matchup_Matrix.csv"))
    m_data = [
        [Paragraph("Opponent", cell_hdr), Paragraph("Threat Batter", cell_hdr), Paragraph("RR Primary Bowler", cell_hdr), Paragraph("Target Phase", cell_hdr), Paragraph("Tactical Execution Plan", cell_hdr)]
    ]
    for _, m in matchup_df.head(15).iterrows():
        m_data.append([
            Paragraph(m['opponent'], cell_bold),
            Paragraph(m['threat_batter'], cell_bold),
            Paragraph(m['rr_primary_bowler'], cell_style),
            Paragraph(m['phase'], cell_style),
            Paragraph(m['tactical_plan'], cell_style)
        ])
    t_m = Table(m_data, colWidths=[60, 90, 100, 85, 169])
    t_m.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#FF007F")),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor("#CBD5E1")),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor("#F8FAFC")]),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('TOPPADDING', (0, 0), (-1, -1), 3),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 3)
    ]))
    story.append(t_m)

    doc.build(story, canvasmaker=NumberedCanvas)
    print(f" -> {pdf_path} successfully generated.")


def build_squad_optimization_pdf():
    pdf_path = os.path.join(BASE_DIR, "RR_2027_Squad_Optimisation_Report.pdf")
    print(f"Building {pdf_path}...")
    doc = SimpleDocTemplate(pdf_path, pagesize=letter, leftMargin=54, rightMargin=54, topMargin=54, bottomMargin=54)
    styles = getSampleStyleSheet()

    title_style = ParagraphStyle('SquadTitle', parent=styles['Heading1'], fontName='Helvetica-Bold', fontSize=18, leading=22, textColor=colors.HexColor("#0B132B"), spaceAfter=6)
    subtitle_style = ParagraphStyle('SquadSub', parent=styles['Normal'], fontName='Helvetica', fontSize=10, leading=14, textColor=colors.HexColor("#FF007F"), spaceAfter=12)
    h1_style = ParagraphStyle('SquadH1', parent=styles['Heading2'], fontName='Helvetica-Bold', fontSize=12, leading=16, textColor=colors.HexColor("#1E293B"), spaceBefore=10, spaceAfter=4, keepWithNext=True)
    body_style = ParagraphStyle('SquadBody', parent=styles['Normal'], fontName='Helvetica', fontSize=8.5, leading=12, textColor=colors.HexColor("#334155"), spaceAfter=5)
    
    cell_style = ParagraphStyle('SCell', parent=styles['Normal'], fontName='Helvetica', fontSize=7.5, leading=9.5)
    cell_bold = ParagraphStyle('SCellB', parent=cell_style, fontName='Helvetica-Bold')
    cell_hdr = ParagraphStyle('SCellH', parent=cell_style, fontName='Helvetica-Bold', textColor=colors.white)

    story = []
    story.append(Paragraph("PROJECT RR-EDGE: RAJASTHAN ROYALS SQUAD OPTIMIZATION", title_style))
    story.append(Paragraph("<b>1,000 Monte Carlo Simulations, Purse Restructuring & Pitch-Specific XIs</b>", subtitle_style))
    story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor("#0B132B"), spaceBefore=2, spaceAfter=10))

    story.append(Paragraph("1. Pre-Auction Purse Restructuring (~₹38.0 Cr Available)", h1_style))
    story.append(Paragraph(
        "By releasing underperforming contracts ahead of November 17, 2026—Shimron Hetmyer (₹11 Cr), Ravi Bishnoi (₹7.2 Cr), "
        "Tushar Deshpande (₹6.5 Cr), Sandeep Sharma (₹4 Cr), Sam Curran (₹2.4 Cr), Adam Milne (₹2.4 Cr), and Kwena Maphaka (₹1.5 Cr)—alongside "
        "the ₹6 Cr salary cap expansion (₹151 Cr to ₹157 Cr), Rajasthan Royals secure an elite <b>~₹38.0 Crore auction purse</b>.",
        body_style
    ))

    # Embed Radar Chart
    radar_chart = os.path.join(CHARTS_DIR, "figure3_squad_radar.png")
    if os.path.exists(radar_chart):
        story.append(Spacer(1, 4))
        story.append(Image(radar_chart, width=320, height=320))
        story.append(Spacer(1, 4))

    story.append(Paragraph("2. Official Master Playing XI (Balanced Championship XI)", h1_style))
    xi_df = pd.read_csv(os.path.join(BASE_DIR, "RR_2027_Optimal_XI.csv"))
    xi_data = [
        [Paragraph("Pos", cell_hdr), Paragraph("Player Name", cell_hdr), Paragraph("Nationality", cell_hdr), Paragraph("Role", cell_hdr), Paragraph("Tactical Duty", cell_hdr)]
    ]
    for _, r in xi_df.iterrows():
        xi_data.append([
            Paragraph(str(int(r['position'])), cell_bold),
            Paragraph(r['player_name'], cell_bold),
            Paragraph(r['nationality'], cell_style),
            Paragraph(r['role'], cell_style),
            Paragraph(r['tactical_duty'], cell_style)
        ])
    t_xi = Table(xi_data, colWidths=[25, 110, 65, 120, 184])
    t_xi.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#0B132B")),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor("#CBD5E1")),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor("#F8FAFC")]),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('TOPPADDING', (0, 0), (-1, -1), 3),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 3)
    ]))
    story.append(t_xi)

    story.append(PageBreak())
    story.append(Paragraph("3. Monte Carlo Auction Budget Allocation (Optimal Scenario)", h1_style))
    
    # Embed Pie Chart
    pie_chart = os.path.join(CHARTS_DIR, "figure4_monte_carlo_budget.png")
    if os.path.exists(pie_chart):
        story.append(Image(pie_chart, width=380, height=270))
        story.append(Spacer(1, 6))

    story.append(Paragraph("4. Pitch-Specific & Opponent-Tailored Playing XIs", h1_style))
    story.append(Paragraph(
        "• <b>Spin-Choke XI (Chepauk / Lucknow / Turning Tracks)</b>: Sub out Akash Deep; bring in <b>Vignesh Puthur / 3rd Spinner</b> to deploy 12 overs of spin choke (Jadeja, Punja, Puthur).<br/>"
        "• <b>Pace-Express XI (Wankhede / High-Bounce Tracks)</b>: Sub out Yash Raj Punja; deploy <b>Nandre Burger / Yudhvir Singh</b> to form a 4-prong pace attack with Archer, Pathirana, and Akash Deep.<br/>"
        "• <b>Chasing High Total XI (190+ Target)</b>: Deploy <b>Ashutosh Sharma / Shubham Dubey</b> as Impact Sub to deepen the batting to No. 8.",
        body_style
    ))

    doc.build(story, canvasmaker=NumberedCanvas)
    print(f" -> {pdf_path} successfully generated.")


def build_executive_summary_onepager():
    pdf_path = os.path.join(BASE_DIR, "RR_EDGE_Executive_Summary.pdf")
    print(f"Building {pdf_path}...")
    doc = SimpleDocTemplate(pdf_path, pagesize=letter, leftMargin=36, rightMargin=36, topMargin=36, bottomMargin=36)
    styles = getSampleStyleSheet()

    title_style = ParagraphStyle('ExecTitle', parent=styles['Heading1'], fontName='Helvetica-Bold', fontSize=17, leading=20, textColor=colors.HexColor("#0077B6"), spaceAfter=2)
    sub_style = ParagraphStyle('ExecSub', parent=styles['Normal'], fontName='Helvetica-Bold', fontSize=9, leading=12, textColor=colors.HexColor("#FF007F"), spaceAfter=6)
    h2_style = ParagraphStyle('ExecH2', parent=styles['Heading2'], fontName='Helvetica-Bold', fontSize=10, leading=13, textColor=colors.HexColor("#1E293B"), spaceBefore=6, spaceAfter=3)
    body_style = ParagraphStyle('ExecBody', parent=styles['Normal'], fontName='Helvetica', fontSize=7.5, leading=10, textColor=colors.HexColor("#334155"), spaceAfter=4)
    
    cell_style = ParagraphStyle('ECell', parent=styles['Normal'], fontName='Helvetica', fontSize=6.8, leading=8.5)
    cell_bold = ParagraphStyle('ECellB', parent=cell_style, fontName='Helvetica-Bold')
    cell_hdr = ParagraphStyle('ECellH', parent=cell_style, fontName='Helvetica-Bold', textColor=colors.white)

    story = []
    story.append(Paragraph("PROJECT RR-EDGE: 1-PAGE EXECUTIVE CHEAT-SHEET", title_style))
    story.append(Paragraph("Rajasthan Royals SupeRR Selector S2 | Official Dropdown Selection & Strategy Card", sub_style))
    story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor("#FF007F"), spaceBefore=1, spaceAfter=6))

    # Core Findings Summary
    core_text = (
        "<b>Mission</b>: Identify the 10 most reliable batters and bowlers under pressure from the proprietary 2022–2026 data pack (200,999 deliveries, 883 matches). "
        "<b>Methodology</b>: Pre-delivery pressure index (zero target leakage), LightGBM Expected Runs (xR) and Wickets (xW), Empirical Bayesian shrinkage ($K=40$), and 500-cluster bootstrap CIs."
    )
    story.append(Paragraph(core_text, body_style))

    # Side-by-side Top 10 Batters & Bowlers
    bat_top = pd.read_csv(os.path.join(BASE_DIR, "RR_EDGE_Batter_Rankings.csv")).head(10)
    bowl_top = pd.read_csv(os.path.join(BASE_DIR, "RR_EDGE_Bowler_Rankings.csv")).head(10)

    combined_table_data = [
        [
            Paragraph("Rank", cell_hdr),
            Paragraph("Top 10 Batters (PBRS)", cell_hdr),
            Paragraph("ID", cell_hdr),
            Paragraph("Press SR", cell_hdr),
            Paragraph("Delta", cell_hdr),
            Paragraph("Score", cell_hdr),
            Paragraph("Top 10 Bowlers (PBwRS)", cell_hdr),
            Paragraph("ID", cell_hdr),
            Paragraph("Press Econ", cell_hdr),
            Paragraph("Death Econ", cell_hdr),
            Paragraph("Score", cell_hdr)
        ]
    ]

    for i in range(10):
        b = bat_top.iloc[i]
        bw = bowl_top.iloc[i]
        combined_table_data.append([
            Paragraph(f"<b>#{i+1}</b>", cell_bold),
            Paragraph(f"<b>{b['player_name']}</b> ({b['country'][:3]})", cell_style),
            Paragraph(str(int(b['player_id'])), cell_style),
            Paragraph(f"{b['press_sr']:.1f}", cell_style),
            Paragraph(f"+{b['pressure_delta_sr']:.1f}", cell_bold),
            Paragraph(f"<b>{b['PBRS']:.1f}</b>", cell_bold),
            Paragraph(f"<b>{bw['player_name']}</b> ({bw['country'][:3]})", cell_style),
            Paragraph(str(int(bw['player_id'])), cell_style),
            Paragraph(f"{bw['press_econ']:.2f}", cell_style),
            Paragraph(f"{bw['death_econ']:.2f}", cell_bold),
            Paragraph(f"<b>{bw['PBwRS']:.1f}</b>", cell_bold)
        ])

    t_comb = Table(combined_table_data, colWidths=[24, 98, 26, 38, 32, 34, 102, 26, 42, 42, 34])
    t_comb.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (5, 0), colors.HexColor("#0077B6")),
        ('BACKGROUND', (6, 0), (-1, 0), colors.HexColor("#FF007F")),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor("#CBD5E1")),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor("#F8FAFC")]),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('TOPPADDING', (0, 0), (-1, -1), 2.5),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 2.5)
    ]))
    story.append(t_comb)

    story.append(Spacer(1, 4))
    story.append(Paragraph("RR IPL 2027 Strategic Blueprint: The Master Playing XI & ₹38 Cr Purse Solution", h2_style))
    strat_text = (
        "<b>RR Diagnostic (IPL 2026)</b>: Best powerplay run rate (11.67) and 181 sixes, but leaked 9.92 RPO overall and 9.71 in overs 7–11. "
        "<b>Solution</b>: Protect untouchable Indian batting core (Sooryavanshi, Jaiswal, Jurel, Parag). Release Hetmyer, Bishnoi, Deshpande, Sandeep (~₹38 Cr purse freed). "
        "<b>Targeted Acquisitions</b>: 1) Matheesha Pathirana (₹12-13 Cr, Death Yorker Slinger), 2) Cameron Green (₹10-11 Cr, No. 5 Spin Enforcer), "
        "3) Akash Deep / Mohsin Khan (₹5-6 Cr, Indian Seamer), 4) Ashutosh Sharma (₹4-5 Cr, Clutch Finisher)."
    )
    story.append(Paragraph(strat_text, body_style))

    # Master XI inline summary
    xi_summary = [
        [Paragraph("No.", cell_hdr), Paragraph("Player", cell_hdr), Paragraph("Role", cell_hdr), Paragraph("No.", cell_hdr), Paragraph("Player", cell_hdr), Paragraph("Role", cell_hdr)],
        [Paragraph("1", cell_bold), Paragraph("Yashasvi Jaiswal", cell_bold), Paragraph("Open LHB", cell_style), Paragraph("7", cell_bold), Paragraph("Ravindra Jadeja", cell_bold), Paragraph("All-Rounder SLA", cell_style)],
        [Paragraph("2", cell_bold), Paragraph("Vaibhav Sooryavanshi", cell_bold), Paragraph("Orange Cap Open", cell_style), Paragraph("8", cell_bold), Paragraph("Jofra Archer", cell_bold), Paragraph("Strike Pacer (25 wk)", cell_style)],
        [Paragraph("3", cell_bold), Paragraph("Dhruv Jurel (wk)", cell_bold), Paragraph("No. 3 / WK", cell_style), Paragraph("9", cell_bold), Paragraph("Matheesha Pathirana", cell_bold), Paragraph("Death Yorker Pacer", cell_style)],
        [Paragraph("4", cell_bold), Paragraph("Riyan Parag (c)", cell_bold), Paragraph("Middle Anchor", cell_style), Paragraph("10", cell_bold), Paragraph("Akash Deep / Mohsin", cell_bold), Paragraph("Indian Frontline Seamer", cell_style)],
        [Paragraph("5", cell_bold), Paragraph("Cameron Green", cell_bold), Paragraph("No. 5 Spin Enforcer", cell_style), Paragraph("11", cell_bold), Paragraph("Yash Raj Punja", cell_bold), Paragraph("Frontline Control Spinner", cell_style)],
        [Paragraph("6", cell_bold), Paragraph("Donovan Ferreira", cell_bold), Paragraph("Death Finisher (179 SR)", cell_style), Paragraph("Sub", cell_bold), Paragraph("Ashutosh Sharma / Brijesh", cell_bold), Paragraph("Impact Player (Chase/Bowl)", cell_style)]
    ]
    t_xi_sum = Table(xi_summary, colWidths=[20, 115, 115, 20, 115, 115])
    t_xi_sum.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#0B132B")),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor("#CBD5E1")),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor("#F8FAFC")]),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('TOPPADDING', (0, 0), (-1, -1), 2),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 2)
    ]))
    story.append(t_xi_sum)

    doc.build(story)
    print(f" -> {pdf_path} successfully generated.")


if __name__ == "__main__":
    build_opponent_analysis_pdf()
    build_squad_optimization_pdf()
    build_executive_summary_onepager()
