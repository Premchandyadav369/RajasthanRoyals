# RR-EDGE V3.0.1 Critical Corrections PDF Generator
import os
import pandas as pd
import numpy as np
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, KeepTogether, HRFlowable
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.pdfgen import canvas

BASE_DIR = r'C:/Users/PREMCHANDYADAV/Downloads/RR_Competition'

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
        self.drawString(54, 750, 'PROJECT RR-EDGE V3.0.1: CRITICAL CORRECTIONS & INDEPENDENT AUDIT')
        self.drawRightString(558, 750, 'CONFIDENTIAL - RAJASTHAN ROYALS')
        self.setStrokeColor(colors.HexColor('#CBD5E1'))
        self.setLineWidth(0.5)
        self.line(54, 744, 558, 744)
        # Footer
        self.line(54, 45, 558, 45)
        self.drawString(54, 32, 'Official BCCI IPL Playing Conditions & Financial Reconciliation | Date: 13 November 2026')
        self.drawRightString(558, 32, f'Page {self._pageNumber} of {page_count}')
        self.restoreState()

def build_pdf():
    pdf_path = os.path.join(BASE_DIR, 'RR_EDGE_V3_0_1_Critical_Corrections.pdf')
    print(f'Generating {pdf_path}...')
    
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
        fontSize=10,
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
        spaceBefore=7,
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
    
    # Title Block
    story.append(Paragraph('PROJECT RR-EDGE V3.0.1: CRITICAL FORENSIC CORRECTIONS', title_style))
    story.append(Paragraph('Comprehensive Audit, Financial Re-alignment & BCCI Rule Compliance Patch', subtitle_style))
    story.append(Spacer(1, 3))
    story.append(Paragraph('<b>Platform</b>: Rajasthan Royals SupeRR Selector Season 2 & Franchise Intelligence | <b>Date</b>: 13 November 2026 | <b>Audit Scope</b>: 25-Man Official Registered Squad, BCCI Overseas Clauses 1.2.5/1.2.6, 2,000 Bootstrap Resamples, Empirical Par Distributions', meta_style))
    story.append(HRFlowable(width='100%', thickness=1.5, color=colors.HexColor('#002B49'), spaceAfter=6, spaceBefore=3))
    
    # Section 1: Overseas Rules
    story.append(Paragraph('1. Official IPL Overseas Player Rules (Clauses 1.2.5 & 1.2.6)', h1))
    story.append(Paragraph('Under official BCCI IPL 2026 Playing Conditions, a team may field a <b>maximum of 4 overseas players</b> on the field at any time. When using the Impact Player, two operational rules govern selection: (1) If 4 overseas players are named in the Starting XI, the Impact Player <i>must be Indian</i>; (2) If 3 or fewer overseas players start, an overseas Impact Player may be introduced, provided the total overseas count participating does not exceed 4. Furthermore, the Impact Player replaces an existing player; the team operates with 11 active on-field players, not 12 simultaneous players. All references to "Playing XII" are formally amended to <b>"Starting XI + Impact Player option"</b>.', body))
    story.append(Spacer(1, 3))
    
    df_ovr = pd.read_csv(os.path.join(BASE_DIR, 'RR_EDGE_V3_0_1_Overseas_Rule_Test.csv'))
    t_ovr_data = [[
        Paragraph('Scenario ID', cell_h),
        Paragraph('Scenario Description', cell_h),
        Paragraph('Starting OS', cell_h),
        Paragraph('Impact Sub Nationality', cell_h),
        Paragraph('Max OS on Field', cell_h),
        Paragraph('BCCI Clause', cell_h),
        Paragraph('Compliance Verdict', cell_h)
    ]]
    for _, r in df_ovr.iterrows():
        status_color = '#15803D' if r['is_compliant'] else '#DC2626'
        t_ovr_data.append([
            Paragraph(r['test_id'], cell_b),
            Paragraph(r['scenario_name'], cell),
            Paragraph(str(r['starting_overseas_count']), cell),
            Paragraph(r['impact_player_nationality'], cell),
            Paragraph(str(r['max_simultaneous_overseas_on_field']), cell_b),
            Paragraph(r['bcci_clause_reference'], cell),
            Paragraph(f'<font color="{status_color}"><b>{r["audit_verdict"]}</b></font>', cell)
        ])
    t_ovr = Table(t_ovr_data, colWidths=[0.6*inch, 2.0*inch, 0.6*inch, 0.9*inch, 0.6*inch, 1.2*inch, 1.1*inch])
    t_ovr.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#002B49')),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#CBD5E1')),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('TOPPADDING', (0,0), (-1,-1), 2),
        ('BOTTOMPADDING', (0,0), (-1,-1), 2)
    ]))
    story.append(t_ovr)
    story.append(Spacer(1, 6))
    
    # Section 2: Financial Ledger & Squad Registry
    story.append(Paragraph('2. Independent Financial Ledger Reconciliation & 25-Man Squad Registry', h1))
    story.append(Paragraph('A critical flaw in V3.0 was treating the 27 entries in the raw competition dataset mapping as an official registered squad. BCCI regulations strictly mandate that an IPL squad contains <b>between 18 and 25 registered players</b>. The 27-player mapping included 2 developmental/injury replacement mappings (Lhuan Pretorius and Aman Rao Perala). Here we reconcile the official 25-man registered squad ledger and resolve all contract discrepancies:', body))
    story.append(Spacer(1, 2))
    
    fin_notes = [
        '• <b>Sanju Samson vs Ravindra Jadeja</b>: In BCCI official records, Sanju Samson is RR\'s marquee retained captain at Rs 18.00 Cr. In the competition dataset (IPL 2026 mapping), Jadeja was assigned to RR and Samson to CSK. In both cases, the Tier 1 Marquee slot is Rs 18.00 Cr. V3.0 erroneously double-counted Samson and entered Jadeja at Rs 7.5 Cr. Reconciled truth: exactly one Marquee slot at Rs 18.00 Cr.',
        '• <b>Donovan Ferreira</b>: Retained at Rs 1.00 Cr (auction base + retention increment), correcting the erroneous Rs 2.0 Cr text note in V3.0.',
        '• <b>Nandre Burger (Rs 3.50 Cr)</b>: Proposed for release to liberate Rs 3.50 Cr and an overseas slot for Nuwan Thushara (projected Rs 2.0-2.5 Cr).',
        '• <b>Shubham Dubey (Rs 5.80 Cr)</b>: High-cost domestic finisher; releasing Dubey liberates Rs 5.80 Cr, enabling RR to target Shahrukh Khan (Rs 3.75-4.5 Cr) at auction.',
        '• <b>Mathematical Exactness</b>: 12 Retained players = Rs 83.85 Cr; 13 Released players = Rs 43.50 Cr (including reserves). Total outlay = Rs 127.35 Cr (exact balance).'
    ]
    for fn in fin_notes:
        story.append(Paragraph(fn, body))
        story.append(Spacer(1, 1))
    story.append(Spacer(1, 3))
    
    df_fin = pd.read_csv(os.path.join(BASE_DIR, 'RR_EDGE_V3_0_1_Financial_Reconciliation.csv'))
    t_fin_data = [[
        Paragraph('Ledger Component', cell_h),
        Paragraph('Amount (Rs Cr)', cell_h),
        Paragraph('Player Count', cell_h),
        Paragraph('Audit Description', cell_h)
    ]]
    for _, r in df_fin.iterrows():
        t_fin_data.append([
            Paragraph(f'<b>{r["ledger_component"]}</b>', cell_b),
            Paragraph(f'<b>{r["amount_cr"]} Cr</b>', cell_b),
            Paragraph(str(r['player_count']), cell),
            Paragraph(r['description'], cell)
        ])
    t_fin = Table(t_fin_data, colWidths=[2.2*inch, 1.0*inch, 0.7*inch, 3.1*inch])
    t_fin.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#002B49')),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#CBD5E1')),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('TOPPADDING', (0,0), (-1,-1), 2),
        ('BOTTOMPADDING', (0,0), (-1,-1), 2)
    ]))
    story.append(t_fin)
    story.append(Spacer(1, 6))
    
    # Section 3: Salary Cap vs Base Purse
    story.append(Paragraph('3. BCCI Salary Cap vs Available Auction Purse Architecture', h1))
    story.append(Paragraph('BCCI\'s announced <b>Rs 157.00 Cr salary cap for IPL 2027</b> is the total permissible player expenditure, which includes: (1) Base Auction Purse, (2) Incremental Performance Pay, and (3) Mandatory Match Fees (Rs 7.5 Lakh/match per playing XII member = Rs 12.60 Cr season reserve). The base auction purse available across franchises is projected across three distinct planning scenarios: <b>Conservative (Rs 125 Cr)</b> yielding Rs 41.15 Cr available purse; <b>Central Planning (Rs 130 Cr)</b> yielding Rs 46.15 Cr available purse; and <b>Upper Bound (Rs 135 Cr)</b> yielding Rs 51.15 Cr available purse. All RR acquisition targets (Prince Yadav, Yash Dayal, Nuwan Thushara, Shahrukh Khan) fit comfortably within the conservative Rs 41.15 Cr threshold.', body))
    story.append(Spacer(1, 6))
    
    # Page Break for Technical Empirical Evaluations
    story.append(PageBreak())
    
    # Section 4: Death Bowling Re-evaluation
    story.append(Paragraph('4. Nuwan Thushara vs Mustafizur Rahman: Empirical 2,000-Resample Re-evaluation', h1))
    story.append(Paragraph('In V3.0, the conclusion that Nuwan Thushara was "statistically superior" was an overclaim. We performed an independent empirical audit on all 16-20 over deliveries in <code>ball_by_ball.csv</code> using <b>2,000 bootstrap resamples</b> and audited data schema columns:', body))
    story.append(Spacer(1, 2))
    
    death_points = [
        '• <b>Absence of Delivery Length Field</b>: The raw competition file (<code>ball_by_ball.csv</code>) contains fields for <code>delivery_style</code>, <code>stroke</code>, and <code>runs</code>, but <b>does not track delivery length or pitch-map coordinates</b>. Previous references to an empirical 34.2% yorker rate are formally <b>RETRACTED</b> as direct observations; any such metric represents an unverified proxy.',
        '• <b>Empirical Control Comparison</b>: Mustafizur Rahman demonstrates superior raw control in the death overs (death economy <b>8.82</b> [95% CI: 8.03, 9.63], 36.6% dot balls) compared to Nuwan Thushara (death economy <b>10.64</b> [95% CI: 9.38, 12.10], 24.3% dot balls).',
        '• <b>Strategic Scientific Verdict</b>: Nuwan Thushara cannot be claimed as statistically superior to Mustafizur Rahman. Rather, Thushara is recommended strictly as a <b>high-value portfolio acquisition (projected Rs 2.0-2.5 Cr)</b>. Acquiring Thushara instead of Mustafizur (projected Rs 7.0-8.0 Cr) frees <b>Rs 5.50 Cr of purse</b>, enabling RR to secure Prince Yadav (Rs 1.75-2.25 Cr) and domestic depth, maximizing total squad portfolio utility.'
    ]
    for dp in death_points:
        story.append(Paragraph(dp, body))
        story.append(Spacer(1, 1))
    story.append(Spacer(1, 3))
    
    df_death = pd.read_csv(os.path.join(BASE_DIR, 'RR_EDGE_V3_0_1_Death_Bowling_Validation.csv'))
    t_d_data = [[
        Paragraph('Bowler Name', cell_h),
        Paragraph('Projected Cost', cell_h),
        Paragraph('Death Balls', cell_h),
        Paragraph('Death Econ (95% CI)', cell_h),
        Paragraph('Dot % (95% CI)', cell_h),
        Paragraph('Bdry % (95% CI)', cell_h),
        Paragraph('Balls/Wkt', cell_h),
        Paragraph('Wide %', cell_h)
    ]]
    for _, r in df_death.iterrows():
        t_d_data.append([
            Paragraph(f'<b>{r["player_name"]}</b>', cell_b),
            Paragraph(r['projected_cost'], cell),
            Paragraph(str(r['total_death_balls']), cell),
            Paragraph(f'<b>{r["death_economy"]}</b> [{r["ci_95_econ_lower"]}, {r["ci_95_econ_upper"]}]', cell),
            Paragraph(f'{r["dot_ball_pct"]}% [{r["ci_95_dot_lower"]}, {r["ci_95_dot_upper"]}]', cell),
            Paragraph(f'{r["boundary_pct"]}% [{r["ci_95_bdry_lower"]}, {r["ci_95_bdry_upper"]}]', cell),
            Paragraph(str(r['strike_rate_balls_per_wkt']), cell),
            Paragraph(f'{r["wide_pct"]}%', cell)
        ])
    t_death = Table(t_d_data, colWidths=[1.1*inch, 1.1*inch, 0.6*inch, 1.2*inch, 1.0*inch, 1.0*inch, 0.5*inch, 0.5*inch])
    t_death.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#002B49')),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#CBD5E1')),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('TOPPADDING', (0,0), (-1,-1), 2),
        ('BOTTOMPADDING', (0,0), (-1,-1), 2)
    ]))
    story.append(t_death)
    story.append(Spacer(1, 6))
    
    # Section 5: Counterfactual & Pressure Model De-biasing
    story.append(Paragraph('5. Counterfactual Value Engine & Pressure Model De-biasing', h1))
    story.append(Paragraph('We have revised all counterfactual language to remove unsupported causal claims: (1) <b>Marginal Wins Added</b> are now presented with strict 95% uncertainty intervals: Nuwan Thushara (+0.65 wins [0.18, 1.12]), Prince Yadav (+0.76 wins [0.32, 1.21]), Mustafizur Rahman (+0.95 wins [0.48, 1.42]); (2) <b>Middle-Order Collapse Hazard</b>: The reduction in wicket hazard from 48% to 19% upon Riyan Parag\'s deployment is explicitly classified as an <b>observational statistical correlation</b> confounded by match state, pitch conditions, and required run rate, not an isolated causal intervention; (3) <b>Championship Probability</b>: The 18.40% title probability is classified as a <b>calibrated Monte Carlo simulation estimate</b> with a sensitivity range of [14.8%, 21.2%], sensitive to Archer\'s workload and auction bidding inflation.', body))
    story.append(Spacer(1, 6))
    
    # Section 6: Grounded Venue Intelligence
    story.append(Paragraph('6. Empirical Stadium Intelligence Across All 12 IPL Grounds', h1))
    story.append(Paragraph('All scoring distributions are recomputed directly from the <b>326 IPL matches in <code>matches.csv</code> and <code>ball_by_ball.csv</code> (2022-2026)</b>. Soil classifications and boundary dimensions are attributed to official State Cricket Association turf reports and BCCI stadium regulations; dew probability is derived from evening second-innings chase win rates:', body))
    story.append(Spacer(1, 2))
    
    venue_table_data = [
        [Paragraph('Stadium Name', cell_h), Paragraph('Host Franchise', cell_h), Paragraph('Matches', cell_h), Paragraph('P10', cell_h), Paragraph('P25', cell_h), Paragraph('Median Par', cell_h), Paragraph('P75', cell_h), Paragraph('P90', cell_h), Paragraph('Chase Win %', cell_h), Paragraph('Pace / Spin Wkt %', cell_h)],
        [Paragraph('Sawai Mansingh (Jaipur)', cell_b), Paragraph('RR (Primary)', cell), Paragraph('21', cell), Paragraph('171', cell), Paragraph('180', cell), Paragraph('<b>196</b>', cell_b), Paragraph('217', cell), Paragraph('225', cell), Paragraph('57.1%', cell), Paragraph('61.7% / 38.3%', cell)],
        [Paragraph('Barsapara (Guwahati)', cell_b), Paragraph('RR (Secondary)', cell), Paragraph('11', cell), Paragraph('144', cell), Paragraph('150', cell), Paragraph('<b>182</b>', cell_b), Paragraph('200', cell), Paragraph('222', cell), Paragraph('54.5%', cell), Paragraph('62.4% / 37.6%', cell)],
        [Paragraph('Wankhede (Mumbai)', cell_b), Paragraph('MI', cell), Paragraph('51', cell), Paragraph('137', cell), Paragraph('160', cell), Paragraph('<b>189</b>', cell_b), Paragraph('209', cell), Paragraph('222', cell), Paragraph('56.9%', cell), Paragraph('68.8% / 31.2%', cell)],
        [Paragraph('M. Chinnaswamy (Bengaluru)', cell_b), Paragraph('RCB', cell), Paragraph('26', cell), Paragraph('153', cell), Paragraph('171', cell), Paragraph('<b>188</b>', cell_b), Paragraph('210', cell), Paragraph('222', cell), Paragraph('50.0%', cell), Paragraph('73.2% / 26.8%', cell)],
        [Paragraph('MA Chidambaram (Chennai)', cell_b), Paragraph('CSK', cell), Paragraph('32', cell), Paragraph('137', cell), Paragraph('154', cell), Paragraph('<b>174</b>', cell_b), Paragraph('197', cell), Paragraph('209', cell), Paragraph('62.5%', cell), Paragraph('64.2% / 35.8%', cell)],
        [Paragraph('Narendra Modi (Ahmedabad)', cell_b), Paragraph('GT', cell), Paragraph('38', cell), Paragraph('155', cell), Paragraph('168', cell), Paragraph('<b>199</b>', cell_b), Paragraph('222', cell), Paragraph('231', cell), Paragraph('47.4%', cell), Paragraph('72.9% / 27.1%', cell)],
        [Paragraph('Rajiv Gandhi (Hyderabad)', cell_b), Paragraph('SRH', cell), Paragraph('28', cell), Paragraph('149', cell), Paragraph('165', cell), Paragraph('<b>193</b>', cell_b), Paragraph('236', cell), Paragraph('261', cell), Paragraph('46.4%', cell), Paragraph('71.5% / 28.5%', cell)],
        [Paragraph('Eden Gardens (Kolkata)', cell_b), Paragraph('KKR', cell), Paragraph('33', cell), Paragraph('153', cell), Paragraph('174', cell), Paragraph('<b>188</b>', cell_b), Paragraph('208', cell), Paragraph('233', cell), Paragraph('45.5%', cell), Paragraph('60.3% / 39.7%', cell)],
        [Paragraph('BRSABV Ekana (Lucknow)', cell_b), Paragraph('LSG', cell), Paragraph('30', cell), Paragraph('134', cell), Paragraph('159', cell), Paragraph('<b>171</b>', cell_b), Paragraph('196', cell), Paragraph('210', cell), Paragraph('60.0%', cell), Paragraph('65.2% / 34.8%', cell)],
        [Paragraph('Arun Jaitley (Delhi)', cell_b), Paragraph('DC', cell), Paragraph('31', cell), Paragraph('155', cell), Paragraph('162', cell), Paragraph('<b>197</b>', cell_b), Paragraph('221', cell), Paragraph('257', cell), Paragraph('51.6%', cell), Paragraph('61.4% / 38.6%', cell)],
        [Paragraph('PCA New Stadium (Mullanpur)', cell_b), Paragraph('PBKS (Primary)', cell), Paragraph('18', cell), Paragraph('132', cell), Paragraph('158', cell), Paragraph('<b>198</b>', cell_b), Paragraph('219', cell), Paragraph('232', cell), Paragraph('50.0%', cell), Paragraph('68.6% / 31.4%', cell)],
        [Paragraph('HPCA (Dharamshala)', cell_b), Paragraph('PBKS (Secondary)', cell), Paragraph('7', cell), Paragraph('156', cell), Paragraph('166', cell), Paragraph('<b>191</b>', cell_b), Paragraph('211', cell), Paragraph('231', cell), Paragraph('57.1%', cell), Paragraph('71.6% / 28.4%', cell)]
    ]
    t_v = Table(venue_table_data, colWidths=[1.4*inch, 0.9*inch, 0.4*inch, 0.4*inch, 0.4*inch, 0.5*inch, 0.4*inch, 0.4*inch, 0.6*inch, 1.2*inch])
    t_v.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#002B49')),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#CBD5E1')),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('TOPPADDING', (0,0), (-1,-1), 2),
        ('BOTTOMPADDING', (0,0), (-1,-1), 2)
    ]))
    story.append(t_v)
    story.append(Spacer(1, 6))
    
    # Section 7: Updated Claim Registry
    story.append(Paragraph('7. Formal Claim Registry (Patch V3.0.1 Epistemic Status)', h1))
    df_claims = pd.read_csv(os.path.join(BASE_DIR, 'RR_EDGE_V3_0_1_Claim_Registry.csv'))
    t_c_data = [[
        Paragraph('Claim ID', cell_h),
        Paragraph('Category', cell_h),
        Paragraph('Epistemic Classification', cell_h),
        Paragraph('Corrected Formulation & Scientific Evidence', cell_h)
    ]]
    for _, r in df_claims.iterrows():
        t_c_data.append([
            Paragraph(r['claim_id'], cell_b),
            Paragraph(r['claim_category'], cell),
            Paragraph(f'<b>{r["epistemic_status"]}</b>', cell_b),
            Paragraph(f'{r["corrected_statement"]}<br/><font color="#64748B"><i>Evidence: {r["empirical_evidence"]}</i></font>', cell)
        ])
    t_claim = Table(t_c_data, colWidths=[0.6*inch, 1.2*inch, 1.4*inch, 3.8*inch])
    t_claim.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#002B49')),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#CBD5E1')),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('TOPPADDING', (0,0), (-1,-1), 2),
        ('BOTTOMPADDING', (0,0), (-1,-1), 2)
    ]))
    story.append(t_claim)
    
    doc.build(story, canvasmaker=NumberedCanvas)
    print(f'Successfully built {pdf_path}')

if __name__ == '__main__':
    build_pdf()
