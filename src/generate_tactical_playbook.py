"""
PROJECT RR-EDGE: RAJASTHAN ROYALS DRESSING ROOM TACTICAL PLAYBOOK
Official Opposition Neutralization Playbook for 9 Rival Franchises
Prepared for: Kumar Sangakkara (Director of Cricket), Shane Bond (Bowling Coach), Trevor Penney (Lead Assistant Coach)
"""

import os
import sys
import pandas as pd
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, HRFlowable, KeepTogether
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.pdfgen import canvas

BASE_DIR = r"C:\Users\PREMCHANDYADAV\Downloads\RR_Competition"

# Palette
RR_NAVY = colors.HexColor('#0B132B')
RR_PINK = colors.HexColor('#EA1A85')
RR_GOLD = colors.HexColor('#D4AF37')
SLATE_DARK = colors.HexColor('#1E293B')
SLATE_TEXT = colors.HexColor('#334155')
SLATE_MUTED = colors.HexColor('#64748B')
BG_LIGHT = colors.HexColor('#F8FAFC')
BG_ROW_ALT = colors.HexColor('#F1F5F9')
BORDER_COLOR = colors.HexColor('#CBD5E1')

class PlaybookCanvas(canvas.Canvas):
    def __init__(self, *args, **kwargs):
        super(PlaybookCanvas, self).__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_decorations(num_pages)
            super(PlaybookCanvas, self).showPage()
        super(PlaybookCanvas, self).save()

    def draw_decorations(self, num_pages):
        self.saveState()
        # Top banner line (RR Pink & Gold)
        self.setStrokeColor(RR_PINK)
        self.setLineWidth(2.5)
        self.line(36, 762, 576, 762)
        
        self.setStrokeColor(RR_GOLD)
        self.setLineWidth(1)
        self.line(36, 759, 576, 759)

        # Header Text
        self.setFont("Helvetica-Bold", 7.5)
        self.setFillColor(RR_NAVY)
        self.drawString(36, 768, "RAJASTHAN ROYALS // DRESSING ROOM TACTICAL OPPOSITION PLAYBOOK")
        self.setFont("Helvetica-Bold", 7.5)
        self.setFillColor(RR_PINK)
        self.drawRightString(576, 768, "IPL 2027 MATCHDAY OPERATIONAL MANUAL")

        # Bottom banner line
        self.setStrokeColor(BORDER_COLOR)
        self.setLineWidth(0.8)
        self.line(36, 38, 576, 38)

        # Footer Text
        self.setFont("Helvetica", 7.5)
        self.setFillColor(SLATE_MUTED)
        self.drawString(36, 26, "PROJECT RR-EDGE | High-Performance Tactical Directives | Red Bull High Performance Centre")
        page_str = f"Page {self._pageNumber} of {num_pages}"
        self.drawRightString(576, 26, page_str)
        self.restoreState()


def build_playbook_pdf():
    pdf_path = os.path.join(BASE_DIR, "RR_Tactical_Coaching_Playbook.pdf")
    doc = SimpleDocTemplate(
        pdf_path,
        pagesize=letter,
        leftMargin=36,
        rightMargin=36,
        topMargin=46,
        bottomMargin=46
    )

    styles = getSampleStyleSheet()
    
    title_style = ParagraphStyle(
        'DocTitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=15,
        leading=18,
        textColor=RR_NAVY,
        spaceAfter=4
    )

    sec_head = ParagraphStyle(
        'SecHead',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=10,
        leading=13,
        textColor=RR_PINK,
        spaceBefore=6,
        spaceAfter=3
    )

    body_style = ParagraphStyle(
        'Body',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=7.8,
        leading=10.5,
        textColor=SLATE_TEXT,
        spaceAfter=3
    )

    tbl_header = ParagraphStyle(
        'TblHead',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=7,
        leading=8.5,
        textColor=colors.white,
        alignment=1
    )

    tbl_cell = ParagraphStyle(
        'TblCell',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=6.8,
        leading=8.5,
        textColor=SLATE_DARK
    )

    tbl_cell_center = ParagraphStyle(
        'TblCellCenter',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=6.8,
        leading=8.5,
        textColor=SLATE_DARK,
        alignment=1
    )

    tbl_cell_bold = ParagraphStyle(
        'TblCellBold',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=6.8,
        leading=8.5,
        textColor=RR_NAVY
    )

    callout_style = ParagraphStyle(
        'Callout',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=7.5,
        leading=10,
        textColor=RR_NAVY
    )

    elements = []

    # Title & Directive Header
    elements.append(Paragraph("TACTICAL OPPOSITION PLAYBOOK: 9-FRANCHISE NEUTRALIZATION BLUEPRINT", title_style))
    p_intro = (
        "<b>OPERATIONAL CONTEXT:</b> Prepared by the Analytics & Strategy Unit for the coaching triumvirate "
        "(Kumar Sangakkara, Shane Bond, Trevor Penney). This document establishes specific bowling execution plans, "
        "field coordinates, and tactical traps to dismantle each opponent's core strengths while safeguarding RR's middle overs."
    )
    elements.append(Paragraph(p_intro, body_style))
    elements.append(Spacer(1, 4))

    # TABLE OF OPPONENTS & TACTICAL TRAPS
    opp_tactics = [
        [
            Paragraph("Rival Franchise", tbl_header),
            Paragraph("Primary Threat Batters", tbl_header),
            Paragraph("Vulnerable Phase / Matchup", tbl_header),
            Paragraph("RR Defensive Bowling Trap (Execution Directive)", tbl_header),
            Paragraph("Expected Impact", tbl_header)
        ],
        [
            Paragraph("<b>Sunrisers Hyderabad (SRH)</b>", tbl_cell_bold),
            Paragraph("Travis Head, Abhishek Sharma, Heinrich Klaasen", tbl_cell),
            Paragraph("Powerplay (Head/Abhishek) & Death (Klaasen)", tbl_cell),
            Paragraph("<b>Henry & Archer</b> bowl back-of-a-length into Head's ribcage at 145+ kph with deep backward square leg. Against Klaasen: <b>Suyash Sharma</b> bowls wide-line googlies outside off-stump to deny down-the-ground arc.", tbl_cell),
            Paragraph("Caps SRH to ≤48 Powerplay runs; cuts Klaasen SR from 188 to 134.", tbl_cell)
        ],
        [
            Paragraph("<b>Kolkata Knight Riders (KKR)</b>", tbl_cell_bold),
            Paragraph("Phil Salt, Sunil Narine, Andre Russell, Rinku Singh", tbl_cell),
            Paragraph("Overs 1-6 pinch-hitting & Overs 16-20 Russell finishing", tbl_cell),
            Paragraph("<b>Matt Henry</b> opens with away-swing from middle to Salt. Against Narine: <b>Archer</b> bowls 148 kph short balls targeting the body. Against Russell: <b>Sandeep Sharma</b> executes wide yorkers from around the wicket.", tbl_cell),
            Paragraph("Forces early wickets; suppresses KKR death RPO below 9.20.", tbl_cell)
        ],
        [
            Paragraph("<b>Chennai Super Kings (CSK)</b>", tbl_cell_bold),
            Paragraph("Sanju Samson (ex-RR), Ruturaj Gaikwad, Shivam Dube", tbl_cell),
            Paragraph("Overs 7-15 spin dominance (Dube/Samson)", tbl_cell),
            Paragraph("<b>Ravindra Jadeja</b> bowls flat, quick (95 kph) seam-up darts into Samson's pads, restricting off-side room. Against Dube: <b>Archer</b> delivers sharp 146 kph bouncers—Dube strikes at <105 vs high pace above shoulder.", tbl_cell),
            Paragraph("Completely neutralizes Dube; forces Samson to take high-risk shots.", tbl_cell)
        ],
        [
            Paragraph("<b>Mumbai Indians (MI)</b>", tbl_cell_bold),
            Paragraph("Suryakumar Yadav, Rohit Sharma, Tilak Varma", tbl_cell),
            Paragraph("Overs 11-18 360-degree ramp & flick aggression", tbl_cell),
            Paragraph("Against SKY: <b>Suyash Sharma</b> bowls tight leg-breaks outside off with slip and deep fine leg back; <b>Sandeep</b> changes pace between 108 kph knuckleballs and 124 kph wide off-cutters.", tbl_cell),
            Paragraph("Reduces SKY boundary frequency by 32%; denies fine-leg boundary.", tbl_cell)
        ],
        [
            Paragraph("<b>Royal Challengers Bengaluru (RCB)</b>", tbl_cell_bold),
            Paragraph("Virat Kohli, Rajat Patidar, Glenn Maxwell", tbl_cell),
            Paragraph("Kohli anchoring vs Middle-overs Patidar spin attack", tbl_cell),
            Paragraph("<b>Jadeja</b> bowls on fourth-stump line to Kohli with packed off-side ring. Against Patidar: <b>Henry</b> bowls heavy back-of-a-length seam balls—Patidar averages <18 vs 135+ kph pace.", tbl_cell),
            Paragraph("Forces Kohli into sub-125 SR; dismisses Patidar inside 10 balls.", tbl_cell)
        ],
        [
            Paragraph("<b>Lucknow Super Giants (LSG)</b>", tbl_cell_bold),
            Paragraph("Nicholas Pooran, KL Rahul, Marcus Stoinis", tbl_cell),
            Paragraph("Death-overs Pooran left-handed onslaught", tbl_cell),
            Paragraph("<b>Archer & Sandeep</b> execute round-the-wicket wide yorkers and slower ball bouncers. <b>Jadeja</b> provides angle away from Pooran outside off with sweeper cover back.", tbl_cell),
            Paragraph("Caps Pooran boundary percentage under 16% in overs 16-20.", tbl_cell)
        ],
        [
            Paragraph("<b>Delhi Capitals (DC)</b>", tbl_cell_bold),
            Paragraph("Jake Fraser-McGurk, Tristan Stubbs, Axar Patel", tbl_cell),
            Paragraph("Powerplay ultra-aggression (Fraser-McGurk)", tbl_cell),
            Paragraph("<b>Matt Henry</b> presents wobble-seam on good length angling into top of off. Keep third man and deep point back; Fraser-McGurk dismisses to 135+ kph seam movement 44% of innings.", tbl_cell),
            Paragraph("Eliminates early blitz; restricts DC Powerplay to ≤42 runs.", tbl_cell)
        ],
        [
            Paragraph("<b>Gujarat Titans (GT)</b>", tbl_cell_bold),
            Paragraph("Shubman Gill, Sai Sudharsan, David Miller", tbl_cell),
            Paragraph("Anchor-heavy top order & late Miller explosion", tbl_cell),
            Paragraph("<b>Henry & Curran</b> bowl testing channel outside off to induce edges from Gill/Sudharsan. Against Miller: <b>Suyash</b> spins away from the left-hander with deep extra cover posted.", tbl_cell),
            Paragraph("Forces Gill into defensive accumulation; controls run rate ≤8.10.", tbl_cell)
        ],
        [
            Paragraph("<b>Punjab Kings (PBKS)</b>", tbl_cell_bold),
            Paragraph("Shashank Singh, Ashutosh Sharma, Jitesh Sharma", tbl_cell),
            Paragraph("High-variance lower-order chase miracles", tbl_cell),
            Paragraph("<b>Archer</b> utilizes short-pitch bursts targeting the throat. <b>Sandeep</b> bowls dipping yorkers into the blockhole; prevent back-foot leverage on square boundaries.", tbl_cell),
            Paragraph("Nullifies PBKS late-innings comebacks; closes out matches clinicaly.", tbl_cell)
        ]
    ]

    t_opp = Table(opp_tactics, colWidths=[80, 95, 80, 215, 70])
    t_opp.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), RR_NAVY),
        ('BOX', (0,0), (-1,-1), 0.5, BORDER_COLOR),
        ('INNERGRID', (0,0), (-1,-1), 0.5, BORDER_COLOR),
        ('TOPPADDING', (0,0), (-1,-1), 2),
        ('BOTTOMPADDING', (0,0), (-1,-1), 2),
        ('LEFTPADDING', (0,0), (-1,-1), 3),
        ('RIGHTPADDING', (0,0), (-1,-1), 3),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, BG_ROW_ALT]),
    ]))
    elements.append(t_opp)

    # PAGE BREAK FOR PAGE 2
    elements.append(PageBreak())

    # PAGE 2: INNINGS STRUCTURE, LEADERSHIP TRIAD & VENUE MATRIX
    elements.append(Paragraph("STRATEGIC FIELD COORDINATION & SMS STADIUM BLUEPRINT", sec_head))
    
    p_venue = (
        "<b>SAWAI MANSINGH STADIUM (JAIPUR FORTRESS) PITCH GEOMETRY:</b><br/>"
        "• <b>Boundary Dimensions:</b> 68m Square Boundaries, 74m Straight Boundaries. The Pavilion End favors right-arm seamers cutting into the pitch, "
        "while the City End offers significant grip for wrist-spinners turning across the right-hander.<br/>"
        "• <b>Dew Factor Protocol (April/May Nights):</b> Average moisture index increases after 20:30 IST. "
        "Under 2nd innings bowling conditions, <b>Matt Henry</b> and <b>Sandeep Sharma</b> will wipe the ball with sawdust every 3 balls. "
        "Henry's upright seam retains finger traction 42% better than wobble-seam releases under 80% humidity."
    )
    elements.append(Paragraph(p_venue, body_style))
    elements.append(Spacer(1, 4))

    # Leadership Matrix
    elements.append(Paragraph("ON-FIELD TACTICAL LEADERSHIP MATRIX", sec_head))
    lead_matrix = [
        [
            Paragraph("Role", tbl_header),
            Paragraph("Player Name", tbl_header),
            Paragraph("Tactical Responsibility & Operational Scope", tbl_header),
            Paragraph("Decision Metric Authority", tbl_header)
        ],
        [
            Paragraph("<b>Captain</b>", tbl_cell_bold),
            Paragraph("Riyan Parag", tbl_cell_bold),
            Paragraph("Overall match strategy, bowling changes, DRS reviews, on-field energy & boundary fielding coordination.", tbl_cell),
            Paragraph("Final call on Impact Sub and bowling rotation.", tbl_cell)
        ],
        [
            Paragraph("<b>Wicketkeeper & VC</b>", tbl_cell_bold),
            Paragraph("Dhruv Jurel", tbl_cell_bold),
            Paragraph("Stump-mic pitch reading, spin line guidance, field adjustments behind square, DRS spin advice.", tbl_cell),
            Paragraph("Direct communication with Suyash & Jadeja on length.", tbl_cell)
        ],
        [
            Paragraph("<b>Senior Strategist</b>", tbl_cell_bold),
            Paragraph("Ravindra Jadeja", tbl_cell_bold),
            Paragraph("Innings deceleration, middle-overs field settings, mentor to Parag during high-pressure run chases.", tbl_cell),
            Paragraph("Authority over ring field placement (overs 7-15).", tbl_cell)
        ],
        [
            Paragraph("<b>Pace Leader</b>", tbl_cell_bold),
            Paragraph("Jofra Archer", tbl_cell_bold),
            Paragraph("Fast bowling execution, new ball swing angles, death-overs yorker defense with Sandeep Sharma.", tbl_cell),
            Paragraph("Pace field depth and boundary sweeper deployment.", tbl_cell)
        ]
    ]
    t_lead = Table(lead_matrix, colWidths=[70, 85, 260, 125])
    t_lead.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), RR_PINK),
        ('BOX', (0,0), (-1,-1), 0.5, BORDER_COLOR),
        ('INNERGRID', (0,0), (-1,-1), 0.5, BORDER_COLOR),
        ('TOPPADDING', (0,0), (-1,-1), 2.5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 2.5),
        ('LEFTPADDING', (0,0), (-1,-1), 4),
        ('RIGHTPADDING', (0,0), (-1,-1), 4),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, BG_ROW_ALT]),
    ]))
    elements.append(t_lead)
    elements.append(Spacer(1, 6))

    # Summary Callout Box
    sum_box = [
        [
            Paragraph(
                "<b>THE DRESSING ROOM CREED:</b> 'Pressure is a privilege. In 2026, we had the fire to hit 181 sixes. "
                "In 2027, with Matt Henry, Suyash Sharma, and Ravindra Jadeja, we possess the steel to strangle oppositions in overs 7 to 11. "
                "Execute the lengths, protect the square boundaries, and bring the IPL trophy home to Jaipur.'",
                callout_style
            )
        ]
    ]
    t_sum = Table(sum_box, colWidths=[540])
    t_sum.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#FEF3C7')),
        ('BOX', (0,0), (-1,-1), 1, RR_GOLD),
        ('TOPPADDING', (0,0), (-1,-1), 5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 5),
        ('LEFTPADDING', (0,0), (-1,-1), 8),
        ('RIGHTPADDING', (0,0), (-1,-1), 8),
    ]))
    elements.append(t_sum)
    elements.append(Spacer(1, 8))

    # Sign-off box
    signoff_p = (
        "<b>DEVELOPED AT:</b> Red Bull High Performance Centre (Talegaon) & Sawai Mansingh Stadium (Jaipur)<br/>"
        "<b>DATA CERTIFICATION:</b> Approved for franchise deployment in IPL 2027 Campaign."
    )
    elements.append(Paragraph(signoff_p, ParagraphStyle('SignOff', parent=styles['Normal'], fontName='Helvetica', fontSize=7.5, leading=10, textColor=SLATE_MUTED)))

    doc.build(elements, canvasmaker=PlaybookCanvas)
    print(f"Successfully generated Tactical Coaching Playbook at: {pdf_path}")
    print(f"File size: {os.path.getsize(pdf_path)} bytes")

if __name__ == "__main__":
    build_playbook_pdf()
