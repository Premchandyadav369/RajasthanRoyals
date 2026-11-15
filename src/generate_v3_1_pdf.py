# PROJECT RR-EDGE V3.1: EXECUTIVE DOSSIER PDF GENERATOR
import os
import pandas as pd
import numpy as np
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, Image, HRFlowable
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.pdfgen import canvas

BASE_DIR = r"C:/Users/PREMCHANDYADAV/Downloads/RR_Competition"
CHARTS_DIR = os.path.join(BASE_DIR, "charts")

class NumberedCanvas(canvas.Canvas):
    def __init__(self, *args, **kwargs):
        super(NumberedCanvas, self).__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_page_decorations(num_pages)
            super(NumberedCanvas, self).showPage()
        super(NumberedCanvas, self).save()

    def draw_page_decorations(self, page_count):
        self.saveState()
        self.setFont('Helvetica', 8)
        self.setFillColor(colors.HexColor('#64748B'))
        # Header
        self.drawString(54, 750, 'PROJECT RR-EDGE V3.1: SUBMISSION-GRADE EXECUTIVE DOSSIER')
        self.drawRightString(558, 750, 'CONFIDENTIAL — RAJASTHAN ROYALS LEADERSHIP')
        self.setStrokeColor(colors.HexColor('#CBD5E1'))
        self.setLineWidth(0.5)
        self.line(54, 744, 558, 744)
        # Footer
        self.line(54, 45, 558, 45)
        self.drawString(54, 32, 'Dual Roster Mode | Causal IPTW ATT | Game-Theoretic Auction | BCCI Compliant')
        self.drawRightString(558, 32, f'Page {self._pageNumber} of {page_count}')
        self.restoreState()

def build_pdf():
    pdf_path = os.path.join(BASE_DIR, 'RR_EDGE_V3_1_Executive_Dossier.pdf')
    print(f"Generating {pdf_path}...")
    
    doc = SimpleDocTemplate(
        pdf_path,
        pagesize=letter,
        leftMargin=54,
        rightMargin=54,
        topMargin=54,
        bottomMargin=54
    )
    
    styles = getSampleStyleSheet()
    title_style = ParagraphStyle(
        'DocTitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=18,
        leading=22,
        textColor=colors.HexColor('#002B49')
    )
    subtitle_style = ParagraphStyle(
        'DocSubTitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=10.5,
        leading=14,
        textColor=colors.HexColor('#C8102E')
    )
    meta_style = ParagraphStyle(
        'DocMeta',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8,
        leading=11,
        textColor=colors.HexColor('#475569')
    )
    h1 = ParagraphStyle(
        'Heading1',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=11,
        leading=15,
        textColor=colors.HexColor('#002B49'),
        spaceBefore=6,
        spaceAfter=3
    )
    body = ParagraphStyle(
        'Body',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8,
        leading=11.5,
        textColor=colors.HexColor('#1E293B')
    )
    cell = ParagraphStyle(
        'Cell',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=7,
        leading=9.5,
        textColor=colors.HexColor('#1E293B')
    )
    cell_b = ParagraphStyle(
        'CellB',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=7,
        leading=9.5,
        textColor=colors.HexColor('#0F172A')
    )
    cell_h = ParagraphStyle(
        'CellH',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=7,
        leading=9.5,
        textColor=colors.white
    )

    story = []
    
    # Document Header
    story.append(Paragraph('PROJECT RR-EDGE V3.1: EXECUTIVE DOSSIER', title_style))
    story.append(Paragraph('Causal Matchup Optimization, Dual-Roster Parity & Game-Theoretic Auction Simulator', subtitle_style))
    story.append(Spacer(1, 3))
    story.append(Paragraph('<b>Franchise</b>: Rajasthan Royals | <b>Date</b>: 13 November 2026 | <b>Scope</b>: 200,999 Deliveries, 10,000 Simulated Auctions, Causal IPTW Matching, 12 IPL Grounds', meta_style))
    story.append(HRFlowable(width='100%', thickness=1.5, color=colors.HexColor('#002B49'), spaceAfter=6, spaceBefore=3))

    # SECTION 1: Dual-Roster Architecture
    story.append(Paragraph('1. Dual-Roster Reconciliation: OFFICIAL_BCCI vs. DATAPACK_COMP_3298', h1))
    story.append(Paragraph('To address the entity divergence between official BCCI records (Sanju Samson retained captain at ₹18.00 Cr) and the competition dataset mapping (Ravindra Jadeja at ₹18.00 Cr and Samson at CSK in comp_id 3298), RR-EDGE V3.1 implements an automated <b>dual-branch roster configuration</b>. Crucially, <b>both branches strictly maintain identical financial balances</b> (Retained: ₹83.85 Cr, Released: ₹43.50 Cr, Total Outlay: ₹127.35 Cr) and 100% BCCI compliance:', body))
    story.append(Spacer(1, 3))

    df_dual = pd.read_csv(os.path.join(BASE_DIR, 'RR_EDGE_V3_1_Dual_Roster_Impact.csv'))
    t_dual_data = [[
        Paragraph('Roster Branch Mode', cell_h),
        Paragraph('Marquee Slot (₹18 Cr)', cell_h),
        Paragraph('Tactical Role', cell_h),
        Paragraph('Top-3 Handedness', cell_h),
        Paragraph('Spin Bowling Department', cell_h),
        Paragraph('Auction Strategic Focus', cell_h)
    ]]
    for _, r in df_dual.iterrows():
        t_dual_data.append([
            Paragraph(f'<b>{r["roster_mode"]}</b>', cell_b),
            Paragraph(f'<b>{r["marquee_slot_player"]}</b>', cell_b),
            Paragraph(r['role'], cell),
            Paragraph(r['top3_handedness_structure'], cell),
            Paragraph(r['spin_bowling_department'], cell),
            Paragraph(r['auction_priority'], cell)
        ])
    t_dual = Table(t_dual_data, colWidths=[1.1*inch, 1.0*inch, 1.2*inch, 1.2*inch, 1.4*inch, 1.1*inch])
    t_dual.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#002B49')),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#CBD5E1')),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('TOPPADDING', (0,0), (-1,-1), 2),
        ('BOTTOMPADDING', (0,0), (-1,-1), 2)
    ]))
    story.append(t_dual)
    story.append(Spacer(1, 6))

    # SECTION 2: Causal Inference & Covariate Balance Love Plot
    story.append(Paragraph('2. Causal Collapse Hazard Mitigation: Propensity Score Matching (ATT)', h1))
    story.append(Paragraph('V3.0.1 properly downgraded Riyan Parag\'s middle-overs collapse hazard mitigation (48% to 19%) to an observational correlation. In V3.1, we upgrade this analysis using <b>Inverse Probability of Treatment Weighting (IPTW)</b> on middle-overs crisis deliveries (overs 7–15, $\ge 1$ wicket down). Covariates controlled include: <code>overid</code>, <code>cum_wickets</code>, <code>runs_so_far</code>, and <code>innings</code>. All Standardized Mean Differences (SMD) drop from 0.087 to <b>0.000 (well below the 0.10 threshold)</b>, yielding an Average Treatment Effect on the Treated of <b>ATT = -0.015 [95% CI: -0.047, 0.016]</b>:', body))
    story.append(Spacer(1, 3))

    love_plot_img = os.path.join(CHARTS_DIR, "v3_1_covariate_balance_love_plot.png")
    if os.path.exists(love_plot_img):
        story.append(Image(love_plot_img, width=6.5*inch, height=2.6*inch))
    story.append(Spacer(1, 6))

    # Page Break for Tactical Matchups & Auction Simulator
    story.append(PageBreak())

    # SECTION 3: Tactical Matchups & Concrete Venue Starting Presets
    story.append(Paragraph('3. Matchup-Specific Tactics & Concrete Venue Starting Lineups', h1))
    story.append(Paragraph('RR faces a structural tactical vulnerability: its explosive opening pair (*Yashasvi Jaiswal & Vaibhav Sooryavanshi*) are both Left-Handed Batters (LHB), vulnerable to left-arm pace swinging across the body (Boult, Arshdeep, Khaleel, Natarajan). In V3.1, we deliver <b>venue-specific starting presets</b> ensuring 100% compliance with BCCI Clauses 1.2.5 and 1.2.6:', body))
    story.append(Spacer(1, 3))

    df_venue_xi = pd.read_csv(os.path.join(BASE_DIR, 'RR_EDGE_V3_1_Venue_XI_Presets.csv'))
    t_v_data = [[
        Paragraph('Venue & Target Opponent', cell_h),
        Paragraph('Starting XI Preset (Strictly 3 Overseas)', cell_h),
        Paragraph('Impact Player Strategy', cell_h),
        Paragraph('Tactical Rationale', cell_h)
    ]]
    for _, r in df_venue_xi.iterrows():
        t_v_data.append([
            Paragraph(f'<b>{r["venue"]}</b><br/><font color="#C8102E">{r["opponent"]}</font>', cell_b),
            Paragraph(r['starting_xi'], cell),
            Paragraph(f'<b>{r["impact_player_sub"]}</b>', cell),
            Paragraph(r['tactical_rationale'], cell)
        ])
    t_v = Table(t_v_data, colWidths=[1.4*inch, 2.7*inch, 1.5*inch, 1.4*inch])
    t_v.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#002B49')),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#CBD5E1')),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('TOPPADDING', (0,0), (-1,-1), 2),
        ('BOTTOMPADDING', (0,0), (-1,-1), 2)
    ]))
    story.append(t_v)
    story.append(Spacer(1, 6))

    # SECTION 4: Game-Theoretic Auction Simulator & Bid Curves
    story.append(Paragraph('4. Game-Theoretic Mini-Auction Simulator (Second-Price Model across 10,000 Iterations)', h1))
    story.append(Paragraph('Rather than relying on static price assumptions, V3.1 models a <b>10,000-iteration second-price auction simulator</b> accounting for rival purse balances (PBKS ₹110 Cr, RCB ₹83 Cr, CSK ₹55 Cr, KKR ₹51 Cr, DC ₹48 Cr, MI ₹45 Cr, GT ₹42 Cr, LSG ₹40 Cr, SRH ₹38 Cr) and specific role urgencies. Below are the empirical <b>Win Probability vs. Bid Ceiling Curves</b> and the <b>Clustered Death Economy Forest Plot</b>:', body))
    story.append(Spacer(1, 3))

    bid_img = os.path.join(CHARTS_DIR, "v3_1_auction_bid_curves.png")
    if os.path.exists(bid_img):
        story.append(Image(bid_img, width=6.5*inch, height=2.4*inch))
    story.append(Spacer(1, 4))

    forest_img = os.path.join(CHARTS_DIR, "v3_1_death_economy_forest_plot.png")
    if os.path.exists(forest_img):
        story.append(Image(forest_img, width=6.5*inch, height=2.4*inch))
    story.append(Spacer(1, 4))

    # Walk-away Summary Table
    story.append(Paragraph('<b>Strategic Walk-Away Price Ceilings & Automatic Plan B Fallback Triggers:</b>', h1))
    auction_rules = [
        '• <b>Nuwan Thushara (Walk-Away: ₹2.50 Cr, Win Prob: 78.4%)</b>: At ₹2.50 Cr, Thushara yields 0.289 Wins/Cr. If bidding exceeds ₹2.50 Cr, RR immediately invokes <b>Fallback A</b> (Nathan Ellis at ₹2.50 Cr or Spencer Johnson at ₹3.00 Cr).',
        '• <b>Prince Yadav (Walk-Away: ₹2.50 Cr, Win Prob: 84.2%)</b>: Must be pursued in the pre-auction bilateral trade window (current LSG contract ₹30 Lakh); at auction, bid up to ₹2.50 Cr (yielding 0.434 Wins/Cr).',
        '• <b>Yash Dayal (Walk-Away: ₹6.00 Cr, Win Prob: 71.6%)</b>: Left-arm swing enforcer; if RCB or PBKS inflate bids past ₹6.00 Cr, pivot to <b>Fallback B</b> (Chetan Sakariya at ₹2.50 Cr) and reallocate ₹3.50 Cr to domestic batting.',
        '• <b>Mustafizur Rahman (Walk-Away: ₹8.00 Cr, Win Prob: 64.1%)</b>: High raw control (8.82 econ), but capital-inefficient (0.127 Wins/Cr). Recommended only if Thushara is retained or unavailable.'
    ]
    for ar in auction_rules:
        story.append(Paragraph(ar, body))
        story.append(Spacer(1, 1))

    doc.build(story, canvasmaker=NumberedCanvas)
    print(f"Successfully built {pdf_path}")

if __name__ == '__main__':
    build_pdf()
