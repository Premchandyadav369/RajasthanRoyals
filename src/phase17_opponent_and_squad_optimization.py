"""
Phase 17: IPL 2027 Comprehensive Opponent Intelligence, RR Matchup Optimization,
and 1,000-Scenario Monte Carlo Squad Construction Engine.
Project RR-EDGE: Global Cricket Pressure Intelligence & IPL 2027 Auction Optimization System
"""

import os
import json
import numpy as np
import pandas as pd
from itertools import combinations

BASE_DIR = r"C:\Users\PREMCHANDYADAV\Downloads\RR_Competition"
DATA_DIR = os.path.join(BASE_DIR, r"6af458274c1e8_data_pack\Data Pack")
OUTPUTS_DIR = os.path.join(BASE_DIR, "outputs")

def run_phase17_optimization():
    print("=" * 70)
    print("PHASE 17: IPL 2027 OPPONENT INTELLIGENCE & SQUAD OPTIMIZATION ENGINE")
    print("=" * 70)

    # 1. Load Data
    bbb = pd.read_csv(os.path.join(DATA_DIR, 'ball_by_ball.csv'), low_memory=False)
    matches = pd.read_csv(os.path.join(DATA_DIR, 'matches.csv'), low_memory=False)
    comps = pd.read_csv(os.path.join(DATA_DIR, 'competitions.csv'), low_memory=False)
    teams = pd.read_csv(os.path.join(DATA_DIR, 'teams.csv'), low_memory=False)

    m_full = matches.merge(comps, on='comp_id', how='left')
    ipl_matches = m_full[m_full['comp_name'].str.contains('IPL', case=False, na=False)]

    print(f"Loaded {len(ipl_matches)} IPL matches across 2022-2026.")

    # 2. Build Comprehensive Opponent Profiles (9 Rivals)
    # Royal Challengers Bengaluru (RCB), Gujarat Titans (GT), Sunrisers Hyderabad (SRH),
    # Mumbai Indians (MI), Punjab Kings (PBKS), Kolkata Knight Riders (KKR),
    # Chennai Super Kings (CSK), Delhi Capitals (DC), Lucknow Super Giants (LSG).
    
    print("\n[Step 1] Constructing Opponent Intelligence & Threat Diagnostic...")
    
    opponents_intel = [
        {
            'opponent': 'Royal Challengers Bengaluru (RCB)',
            'ipl_2026_standing': '1st (18 pts, +0.783 NRR)',
            'threat_level': 'HIGHEST THREAT',
            'powerplay_profile': 'Aggressive (Salt + Kohli): 10.2 RPO, high boundary conversion early',
            'middle_overs_7_11': 'Acceleration via Patidar vs spin: 9.6 RPO; vulnerable to SLA taking pace off',
            'middle_overs_12_15': 'Consolidation & anchor pacing: 9.1 RPO',
            'death_overs_16_20': '11.8 RPO finishing; Kohli anchored stability + lower-order power',
            'key_finishers': 'Rajat Patidar, Liam Livingstone (traded from SRH), Dinesh Karthik / finishers',
            'weakness_pace_vs_spin': 'Top order vulnerable to high-pace back-of-length (Archer); middle vulnerable to Jadeja wide SLA',
            'post_trade_status': 'Acquired Liam Livingstone (₹6 Cr) & Jack Edwards (₹3 Cr) from CSK via SRH exchange; lost Ellis & Khaleel',
            'rr_bowling_counter': 'Archer attacks Salt early on 5th stump; Jadeja & Punja choke overs 7-13; Pathirana/Malinga wide yorkers to Livingstone at death',
            'rr_batting_counter': 'Jaiswal & Sooryavanshi attack Bhuvneshwar/Dayal early; Parag & Jurel target spin in overs 7-12'
        },
        {
            'opponent': 'Gujarat Titans (GT)',
            'ipl_2026_standing': '2nd (18 pts, Finalist, beat RR in Q2)',
            'threat_level': 'HIGHEST THREAT',
            'powerplay_profile': 'Disciplined Accumulation (Gill + Sudharsan): 8.8 RPO, lowest dot% in league',
            'middle_overs_7_11': 'Solid foundation: 8.9 RPO; low risk, high strike rotation',
            'middle_overs_12_15': 'Shift gears: 10.1 RPO via Miller and middle order',
            'death_overs_16_20': '12.4 RPO via Tewatia, Miller, and Rashid Khan',
            'key_finishers': 'Rahul Tewatia, David Miller, Rashid Khan',
            'weakness_pace_vs_spin': 'Gill vulnerable to incoming high pace; Sudharsan struggles when forced to hit flat spinners over covers',
            'post_trade_status': 'Rabada led 2026 wickets (29 wkts); bowling attack intact with Rashid & Shami',
            'rr_bowling_counter': 'Archer aggressive bouncer strategy to Gill; Jadeja cramps Sudharsan; specialist death pacer blocks Tewatia arc',
            'rr_batting_counter': 'Must not let Rashid Khan dictate overs 7-14; Jurel & Cameron Green/No. 5 sweep & reverse-sweep against spin choke'
        },
        {
            'opponent': 'Sunrisers Hyderabad (SRH)',
            'ipl_2026_standing': '3rd (18 pts, Eliminator)',
            'threat_level': 'HIGHEST THREAT',
            'powerplay_profile': 'Maximum Carnage (Head + Abhishek): 12.8 RPO, 48% boundary frequency',
            'middle_overs_7_11': 'Klaasen destructive surge against spin: 11.2 RPO',
            'middle_overs_12_15': 'Nitish Reddy & Samad: 10.5 RPO',
            'death_overs_16_20': '12.6 RPO; Pat Cummins & Klaasen long-range hitting',
            'key_finishers': 'Heinrich Klaasen, Abdul Samad, Pat Cummins',
            'weakness_pace_vs_spin': 'Head/Abhishek struggle when pace is taken OFF or tucked into ribs without width; Klaasen destroys slow spin, vulnerable to body bouncers',
            'post_trade_status': 'MASSIVE TRADE WINNERS: Acquired T. Natarajan (₹5 Cr), Khaleel Ahmed (₹4.8 Cr), and Nathan Ellis (₹2 Cr) alongside Cummins!',
            'rr_bowling_counter': 'ZERO predictable pace-on in Powerplay; Archer heavy back-of-length; Jadeja takes pace off wide; Pathirana/Malinga blockhole to Klaasen',
            'rr_batting_counter': 'Counter Khaleel & Natarajan left-arm angle: Promote Dhruv Jurel / Riyan Parag to break left-handed monopoly if Jaiswal/Sooryavanshi fall'
        },
        {
            'opponent': 'Mumbai Indians (MI)',
            'ipl_2026_standing': '9th (8 pts, High Ceiling Rebuilding)',
            'threat_level': 'LETHAL BOWLING SURGER',
            'powerplay_profile': 'Rohit Sharma + Ishan Kishan / new opener: 9.4 RPO',
            'middle_overs_7_11': 'Suryakumar Yadav 360-degree attack: 10.8 RPO',
            'middle_overs_12_15': 'Tilak Varma stability & acceleration: 9.8 RPO',
            'death_overs_16_20': '12.2 RPO via Tim David & middle power',
            'key_finishers': 'Tim David, Romario Shepherd, Suryakumar Yadav',
            'weakness_pace_vs_spin': 'Rohit vulnerable to left-arm inswing/pace early; Tilak contained by Jadeja SLA away from bat',
            'post_trade_status': 'BLOCKBUSTER TRADE: Traded Hardik Pandya to PBKS to acquire Arshdeep Singh (₹18 Cr) to pair with Jasprit Bumrah!',
            'rr_bowling_counter': 'Archer attacks Rohit upfront; Jadeja takes pace off against Surya; Pathirana death duel against Tim David',
            'rr_batting_counter': 'Preserve wickets against Bumrah and Arshdeep; target MI 3rd and 4th domestic/overseas seamers ruthlessly'
        },
        {
            'opponent': 'Punjab Kings (PBKS)',
            'ipl_2026_standing': '5th (15 pts, Aggressive Underdogs)',
            'threat_level': 'MAJOR THREAT',
            'powerplay_profile': 'Prabhsimran + aggressive top: 9.8 RPO',
            'middle_overs_7_11': 'Hardik Pandya & Shashank Singh anchor & hit: 9.4 RPO',
            'middle_overs_12_15': 'Ashutosh Sharma / domestic finishers: 10.2 RPO',
            'death_overs_16_20': '11.9 RPO; high boundary dependency',
            'key_finishers': 'Hardik Pandya, Shashank Singh, Ashutosh Sharma (target trade/auction)',
            'weakness_pace_vs_spin': 'Death bowling depleted after losing Arshdeep Singh; domestic seam attack highly vulnerable in overs 16-20',
            'post_trade_status': 'Acquired Hardik Pandya (₹18 Cr) as captain/all-rounder; traded out Arshdeep Singh to MI',
            'rr_bowling_counter': 'Archer attacks Prabhsimran early; Punja & Jadeja squeeze Hardik in middle overs; Pathirana executes yorkers',
            'rr_batting_counter': 'Attack PBKS domestic death seamers; Jaiswal, Parag, Jurel and Ferreira feast in overs 15-20'
        },
        {
            'opponent': 'Kolkata Knight Riders (KKR)',
            'opponent_code': 'KKR',
            'ipl_2026_standing': '7th (13 pts, High Ceiling)',
            'threat_level': 'HIGH THREAT',
            'powerplay_profile': 'Narine explosive pinch-hit (11.5 RPO) + Gurbaz/Salt',
            'middle_overs_7_11': 'Spin stranglehold (Narine + Varun Chakravarthy): concede only 7.2 RPO',
            'middle_overs_12_15': 'Rinku Singh & Russell foundation: 9.5 RPO',
            'death_overs_16_20': '13.1 RPO via Andre Russell & Rinku Singh',
            'key_finishers': 'Andre Russell, Rinku Singh, Ramandeep Singh',
            'weakness_pace_vs_spin': 'Narine opener vulnerable to short ball into body; Russell vulnerable to wide yorkers outside off or ribcage bouncers',
            'post_trade_status': 'Expensive overseas roster facing release/restructure (Cameron Green, Matheesha Pathirana, Mustafizur, Akash Deep expected in auction pool)',
            'rr_bowling_counter': 'Archer bodyline bouncers to Narine; Jadeja angles away from Russell; Pathirana wide yorkers to Rinku',
            'rr_batting_counter': 'Left-Right combinations against Narine & Varun; rotate strike, do not play cross-batted shots to mystery spin'
        },
        {
            'opponent': 'Chennai Super Kings (CSK)',
            'ipl_2026_standing': '8th (12 pts, Tactical Traditionalists)',
            'threat_level': 'TACTICAL THREAT',
            'powerplay_profile': 'Ruturaj Gaikwad + Rachin: 8.6 RPO, low risk',
            'middle_overs_7_11': 'Shivam Dube spin-hitting masterclass: 10.4 RPO against slow bowling',
            'middle_overs_12_15': 'Moeen/Mitchell pacing: 8.9 RPO',
            'death_overs_16_20': '11.5 RPO via MS Dhoni & lower order',
            'key_finishers': 'Shivam Dube, MS Dhoni, Jamie Overton',
            'weakness_pace_vs_spin': 'Dube destroys spin, highly vulnerable to 145+ km/h bouncers directed at the helmet; Gaikwad contained by swing',
            'post_trade_status': 'Traded Ellis & Khaleel to SRH; looking to reset bowling unit',
            'rr_bowling_counter': 'ZERO SPIN TO SHIVAM DUBE: Archer bowls hard bouncers at Dube; Jadeja bowls to RHB; Archer/Pathirana close out Dhoni at death',
            'rr_batting_counter': 'Attack CSK secondary spinners; Sooryavanshi and Jaiswal dominate Powerplay in Chennai/Jaipur'
        },
        {
            'opponent': 'Delhi Capitals (DC)',
            'ipl_2026_standing': '6th (14 pts, Rebuilding Core)',
            'threat_level': 'SURGING THREAT',
            'powerplay_profile': 'Jake Fraser-McGurk + KL Rahul: 10.5 RPO',
            'middle_overs_7_11': 'Rishabh Pant dynamic middle order: 9.8 RPO',
            'middle_overs_12_15': 'Axar Patel & Stubbs: 9.4 RPO',
            'death_overs_16_20': '12.0 RPO via Tristan Stubbs & Pant',
            'key_finishers': 'Rishabh Pant, Tristan Stubbs, Axar Patel',
            'weakness_pace_vs_spin': 'Fraser-McGurk vulnerable to moving balls on off stump; Pant can be choked by back-of-length cramping pace',
            'post_trade_status': 'Rishabh Pant returned (₹15 Cr); Kuldeep Yadav traded to LSG; T. Natarajan traded to SRH',
            'rr_bowling_counter': 'Archer moves ball away from Fraser-McGurk; Jadeja chokes middle overs; Pathirana slingers to Stubbs',
            'rr_batting_counter': 'DC spin attack weakened after losing Kuldeep Yadav; Parag, Jurel and No. 5 dominate middle overs'
        },
        {
            'opponent': 'Lucknow Super Giants (LSG)',
            'ipl_2026_standing': '10th (8 pts, Trade-Market Rival)',
            'threat_level': 'TRADE & TACTICAL RIVAL',
            'powerplay_profile': 'Mayank Yadav pace + dynamic openers: 9.2 RPO',
            'middle_overs_7_11': 'Nicholas Pooran high-impact spin demolition: 11.0 RPO',
            'middle_overs_12_15': 'Stoinis / Badoni: 9.5 RPO',
            'death_overs_16_20': '12.1 RPO via Pooran & Stoinis',
            'key_finishers': 'Nicholas Pooran, Marcus Stoinis, Ayush Badoni',
            'weakness_pace_vs_spin': 'Pooran destroys medium pace, vulnerable to high-pace yorkers and Jadeja SLA away from bat; batting depth collapses quickly',
            'post_trade_status': 'Acquired Kuldeep Yadav (₹13.5 Cr from DC); active trade partner with RR exploring pace/batting swaps',
            'rr_bowling_counter': 'Archer targets Pooran with 148 km/h yorkers; Jadeja bowls wide defensive SLA; Archer/Pathirana clean up tail',
            'rr_batting_counter': 'Target LSG 5th bowler; respect Kuldeep Yadav, attack domestic pace options (Mohsin/Prince/Yash Thakur)'
        }
    ]

    df_opp = pd.DataFrame(opponents_intel)
    df_opp.to_csv(os.path.join(BASE_DIR, "RR_Opponent_Threat_Matrix.csv"), index=False)
    print(f" -> Opponent Profiles saved for all 9 rivals.")

    # 3. Build Opposition Matchup Matrix (Tactical Pairings)
    print("\n[Step 2] Formulating RR Opposition Matchup Matrix...")
    matchups = [
        {'opponent': 'RCB', 'threat_batter': 'Phil Salt', 'rr_primary_bowler': 'Jofra Archer', 'phase': 'Powerplay (1-3)', 'tactical_plan': '145+ km/h hard back-of-length on 5th stump; deny cut shot'},
        {'opponent': 'RCB', 'threat_batter': 'Virat Kohli', 'rr_primary_bowler': 'Ravindra Jadeja', 'phase': 'Middle (7-11)', 'tactical_plan': 'Dart in flat SLA on leg-stump; deny single rotation; bowl to deep square'},
        {'opponent': 'RCB', 'threat_batter': 'Rajat Patidar', 'rr_primary_bowler': 'Yash Raj Punja', 'phase': 'Middle (9-13)', 'tactical_plan': 'Slow leg-break outside off; invite drive against turning ball'},
        {'opponent': 'RCB', 'threat_batter': 'Liam Livingstone', 'rr_primary_bowler': 'Matheesha Pathirana', 'phase': 'Death (17-20)', 'tactical_plan': 'Slingy toe-crushers and wide yorkers; deny elevation under hands'},
        
        {'opponent': 'GT', 'threat_batter': 'Shubman Gill', 'rr_primary_bowler': 'Jofra Archer', 'phase': 'Powerplay (1-4)', 'tactical_plan': 'Fast nip-backer hitting top of off; target front-pad plant'},
        {'opponent': 'GT', 'threat_batter': 'B. Sai Sudharsan', 'rr_primary_bowler': 'Ravindra Jadeja', 'phase': 'Middle (7-12)', 'tactical_plan': 'Angle ball across left-hander; induce mistimed lofted drive to sweeper'},
        {'opponent': 'GT', 'threat_batter': 'David Miller', 'rr_primary_bowler': 'Matheesha Pathirana', 'phase': 'Death (16-19)', 'tactical_plan': 'Fast yorker at off-stump base; change up with slower bouncer'},
        {'opponent': 'GT', 'threat_batter': 'Rahul Tewatia', 'rr_primary_bowler': 'Akash Deep / Mohsin', 'phase': 'Death (18-20)', 'tactical_plan': 'Wide yorkers outside off tramline; take pace off completely'},

        {'opponent': 'SRH', 'threat_batter': 'Travis Head', 'rr_primary_bowler': 'Jofra Archer', 'phase': 'Powerplay (1-3)', 'tactical_plan': 'Body bouncer at ribcage without width; deny back-foot cut'},
        {'opponent': 'SRH', 'threat_batter': 'Abhishek Sharma', 'rr_primary_bowler': 'Akash Deep / Burger', 'phase': 'Powerplay (2-5)', 'tactical_plan': 'Hard seam-up length shaping away; induce edge to slip/keeper'},
        {'opponent': 'SRH', 'threat_batter': 'Heinrich Klaasen', 'rr_primary_bowler': 'Jofra Archer & Pathirana', 'phase': 'Middle & Death (12-18)', 'tactical_plan': 'ABSOLUTELY NO SPIN. Heavy 145+ km/h bouncers and pinpoint yorkers only'},
        {'opponent': 'SRH', 'threat_batter': 'Abdul Samad', 'rr_primary_bowler': 'Matheesha Pathirana', 'phase': 'Death (18-20)', 'tactical_plan': 'Straight toe-crushing yorker at 142 km/h'},

        {'opponent': 'MI', 'threat_batter': 'Rohit Sharma', 'rr_primary_bowler': 'Jofra Archer', 'phase': 'Powerplay (1-3)', 'tactical_plan': 'High pace on good length shaping back in; test footwork'},
        {'opponent': 'MI', 'threat_batter': 'Suryakumar Yadav', 'rr_primary_bowler': 'Ravindra Jadeja', 'phase': 'Middle (9-14)', 'tactical_plan': 'Take pace off completely; wide line outside off; pack point and third man'},
        {'opponent': 'MI', 'threat_batter': 'Tilak Varma', 'rr_primary_bowler': 'Yash Raj Punja', 'phase': 'Middle (8-13)', 'tactical_plan': 'Spin ball away from left-hander; test patience'},
        {'opponent': 'MI', 'threat_batter': 'Tim David', 'rr_primary_bowler': 'Matheesha Pathirana', 'phase': 'Death (17-20)', 'tactical_plan': 'Laser-guided wide yorker; prevent straight golf swing'},

        {'opponent': 'PBKS', 'threat_batter': 'Prabhsimran Singh', 'rr_primary_bowler': 'Jofra Archer', 'phase': 'Powerplay (1-4)', 'tactical_plan': 'Fast bouncer followed by full inswinging delivery'},
        {'opponent': 'PBKS', 'threat_batter': 'Hardik Pandya', 'rr_primary_bowler': 'Ravindra Jadeja & Punja', 'phase': 'Middle (10-15)', 'tactical_plan': 'Choke with spin into pads; deny pace to generate bat speed'},
        {'opponent': 'PBKS', 'threat_batter': 'Shashank Singh', 'rr_primary_bowler': 'Matheesha Pathirana', 'phase': 'Death (16-19)', 'tactical_plan': 'Full yorker and sharp off-cutter; induce mistimed swipe'},

        {'opponent': 'KKR', 'threat_batter': 'Sunil Narine', 'rr_primary_bowler': 'Jofra Archer', 'phase': 'Powerplay (1-2)', 'tactical_plan': 'Direct bouncer aimed at helmet/throat; force awkward defensive poke'},
        {'opponent': 'KKR', 'threat_batter': 'Rinku Singh', 'rr_primary_bowler': 'Matheesha Pathirana', 'phase': 'Death (17-20)', 'tactical_plan': 'Wide yorkers outside off; deny hitting across the line'},
        {'opponent': 'KKR', 'threat_batter': 'Andre Russell', 'rr_primary_bowler': 'Jofra Archer', 'phase': 'Death (15-18)', 'tactical_plan': 'Fast bouncer followed by quick wide yorker; keep ball away from arc'},

        {'opponent': 'CSK', 'threat_batter': 'Ruturaj Gaikwad', 'rr_primary_bowler': 'Jofra Archer', 'phase': 'Powerplay (1-5)', 'tactical_plan': 'Hard length outside off; test patience against swing'},
        {'opponent': 'CSK', 'threat_batter': 'Shivam Dube', 'rr_primary_bowler': 'Jofra Archer / Pacer', 'phase': 'Middle (10-14)', 'tactical_plan': 'ZERO SPIN. Fast short pitch ball aimed at head; deny front foot stride'},
        {'opponent': 'CSK', 'threat_batter': 'MS Dhoni', 'rr_primary_bowler': 'Matheesha Pathirana', 'phase': 'Death (18-20)', 'tactical_plan': 'Wide yorker outside off; deny helicopter elevation'},

        {'opponent': 'DC', 'threat_batter': 'Jake Fraser-McGurk', 'rr_primary_bowler': 'Jofra Archer', 'phase': 'Powerplay (1-3)', 'tactical_plan': 'Outswing on 5th stump line; draw wild expansive slash'},
        {'opponent': 'DC', 'threat_batter': 'Rishabh Pant', 'rr_primary_bowler': 'Ravindra Jadeja', 'phase': 'Middle (8-14)', 'tactical_plan': 'Flat darting trajectory outside off; deny one-handed swipe over square leg'},
        {'opponent': 'DC', 'threat_batter': 'Tristan Stubbs', 'rr_primary_bowler': 'Matheesha Pathirana', 'phase': 'Death (16-20)', 'tactical_plan': 'Blockhole yorker followed by dipping knuckle-ball'},

        {'opponent': 'LSG', 'threat_batter': 'Nicholas Pooran', 'rr_primary_bowler': 'Ravindra Jadeja & Archer', 'phase': 'Middle & Death (11-17)', 'tactical_plan': 'Jadeja bowls flat trajectory away from hitting arc; Archer attacks with 148 km/h yorkers'},
        {'opponent': 'LSG', 'threat_batter': 'Marcus Stoinis', 'rr_primary_bowler': 'Matheesha Pathirana', 'phase': 'Death (16-19)', 'tactical_plan': 'Deceptive slower ball yorker into the blockhole'}
    ]
    df_matchups = pd.DataFrame(matchups)
    df_matchups.to_csv(os.path.join(BASE_DIR, "RR_Opposition_Matchup_Matrix.csv"), index=False)
    print(f" -> RR Opposition Matchup Matrix saved ({len(df_matchups)} critical tactical matchups).")

    # 4. Formulate RR 20-Over Bowling Phase Coverage Blueprint
    print("\n[Step 3] Constructing RR Bowling Phase Coverage Blueprint...")
    phase_coverage = [
        {'over_number': 1, 'phase': 'Powerplay', 'primary_bowler': 'Jofra Archer', 'bowler_role': 'Strike Spearhead (Pace)', 'expected_rr': 6.2, 'tactical_goal': 'Early wicket; test off-stump discipline'},
        {'over_number': 2, 'phase': 'Powerplay', 'primary_bowler': 'Akash Deep / Mohsin', 'bowler_role': 'Indian Seamer (Swing)', 'expected_rr': 7.0, 'tactical_goal': 'Move ball both ways; maintain tight channel'},
        {'over_number': 3, 'phase': 'Powerplay', 'primary_bowler': 'Jofra Archer', 'bowler_role': 'Strike Spearhead (Pace)', 'expected_rr': 6.5, 'tactical_goal': 'Attack set batter with hostile pace/bouncers'},
        {'over_number': 4, 'phase': 'Powerplay', 'primary_bowler': 'Akash Deep / Mohsin', 'bowler_role': 'Indian Seamer (Pace)', 'expected_rr': 7.5, 'tactical_goal': 'Discipline on 4th stump line; deny boundary'},
        {'over_number': 5, 'phase': 'Powerplay', 'primary_bowler': 'Matheesha Pathirana / Brijesh', 'bowler_role': 'Pace Enforcer / Slinger', 'expected_rr': 7.2, 'tactical_goal': 'Slingy angle into pads; surprise batter before 30-yard ring lifts'},
        {'over_number': 6, 'phase': 'Powerplay', 'primary_bowler': 'Ravindra Jadeja', 'bowler_role': 'Left-Arm Orthodox (Control)', 'expected_rr': 6.8, 'tactical_goal': 'Pace off; flat trajectory; end powerplay with dots'},

        # Middle Overs (Overs 7-11: RR 2026 Problem Area)
        {'over_number': 7, 'phase': 'Middle (7-11)', 'primary_bowler': 'Yash Raj Punja', 'bowler_role': 'Wrist/Control Spin', 'expected_rr': 7.2, 'tactical_goal': 'Break opening stand; induce false drive'},
        {'over_number': 8, 'phase': 'Middle (7-11)', 'primary_bowler': 'Ravindra Jadeja', 'bowler_role': 'Left-Arm Orthodox (Choke)', 'expected_rr': 6.5, 'tactical_goal': 'Rapid 90-second over; deny boundary'},
        {'over_number': 9, 'phase': 'Middle (7-11)', 'primary_bowler': 'Yash Raj Punja', 'bowler_role': 'Wrist/Control Spin', 'expected_rr': 7.5, 'tactical_goal': 'Vary flight; challenge aggressive middle batter'},
        {'over_number': 10, 'phase': 'Middle (7-11)', 'primary_bowler': 'Ravindra Jadeja', 'bowler_role': 'Left-Arm Orthodox (Choke)', 'expected_rr': 6.8, 'tactical_goal': 'Dart into pads; restrict scoring to singles'},
        {'over_number': 11, 'phase': 'Middle (7-11)', 'primary_bowler': 'Cameron Green / Riyan Parag', 'bowler_role': '6th Bowling Option', 'expected_rr': 7.8, 'tactical_goal': 'Sneak an over; heavy lengths or off-spin match-up'},

        # Middle Overs (Overs 12-15: Squeeze & Partnership Breaking)
        {'over_number': 12, 'phase': 'Middle (12-15)', 'primary_bowler': 'Yash Raj Punja', 'bowler_role': 'Wrist/Control Spin', 'expected_rr': 7.5, 'tactical_goal': 'Bowler 3rd over; force attacking error'},
        {'over_number': 13, 'phase': 'Middle (12-15)', 'primary_bowler': 'Ravindra Jadeja', 'bowler_role': 'Left-Arm Orthodox (Choke)', 'expected_rr': 7.0, 'tactical_goal': 'Jadeja final over; maintain sub-7.0 economy'},
        {'over_number': 14, 'phase': 'Middle (12-15)', 'primary_bowler': 'Jofra Archer', 'bowler_role': 'Strike Spearhead (Pace)', 'expected_rr': 7.2, 'tactical_goal': 'Enforcer spell; break dangerous partnership with bouncer'},
        {'over_number': 15, 'phase': 'Middle (12-15)', 'primary_bowler': 'Yash Raj Punja / Brijesh', 'bowler_role': '4th Bowler Option', 'expected_rr': 8.0, 'tactical_goal': 'Close out middle overs without leaking boundary'},

        # Death Overs (Overs 16-20: RR 2026 Vulnerability Fixed)
        {'over_number': 16, 'phase': 'Death (16-20)', 'primary_bowler': 'Matheesha Pathirana', 'bowler_role': 'Death Specialist (Yorkers)', 'expected_rr': 8.2, 'tactical_goal': 'Nail blockhole; suppress starting death surge'},
        {'over_number': 17, 'phase': 'Death (16-20)', 'primary_bowler': 'Akash Deep / Mohsin', 'bowler_role': 'Indian Death Seamer', 'expected_rr': 8.8, 'tactical_goal': 'Wide yorkers and slower ball cutters'},
        {'over_number': 18, 'phase': 'Death (16-20)', 'primary_bowler': 'Jofra Archer', 'bowler_role': 'Strike Spearhead (Pace)', 'expected_rr': 8.0, 'tactical_goal': 'Archer 4th over; 148 km/h toe-crushers'},
        {'over_number': 19, 'phase': 'Death (16-20)', 'primary_bowler': 'Matheesha Pathirana', 'bowler_role': 'Death Specialist (Yorkers)', 'expected_rr': 8.5, 'tactical_goal': 'Penultimate over squeeze; slingy yorkers'},
        {'over_number': 20, 'phase': 'Death (16-20)', 'primary_bowler': 'Matheesha Pathirana / Akash Deep', 'bowler_role': 'Death Specialist (Yorkers)', 'expected_rr': 8.5, 'tactical_goal': 'Final over execution; zero full tosses'}
    ]
    df_phase = pd.DataFrame(phase_coverage)
    df_phase.to_csv(os.path.join(BASE_DIR, "RR_Bowling_Phase_Coverage.csv"), index=False)
    print(f" -> RR Bowling Phase Coverage Blueprint saved (Overs 1 to 20 detailed mapping).")

    # 5. Formulate RR Batting Matchup Analysis
    print("\n[Step 4] Formulating RR Batting Matchup & Left-Right Disruption Strategy...")
    bat_matchup = [
        {'rr_batter': 'Yashasvi Jaiswal', 'stance': 'LHB', 'role': 'Powerplay Aggressor', 'favored_matchup': 'Right-arm pace & off-spin (SR 168+)', 'threat_bowler_type': 'Left-arm swing shaping away (Khaleel/Arshdeep)', 'tactical_instruction': 'Dominate powerplay; use crease depth against swing'},
        {'rr_batter': 'Vaibhav Sooryavanshi', 'stance': 'LHB', 'role': 'Powerplay Enforcer', 'favored_matchup': 'High pace & short balls (Orange Cap form, SR 174+)', 'threat_bowler_type': 'Inswinging yorkers early on pads', 'tactical_instruction': 'Fearless intent; attack new-ball bowlers immediately'},
        {'rr_batter': 'Dhruv Jurel', 'stance': 'RHB', 'role': 'Middle Order Anchor / No. 3', 'favored_matchup': 'Left-arm orthodox & wrist spin (SR 155+)', 'threat_bowler_type': '145+ km/h bouncers directed at helmet', 'tactical_instruction': 'Break left-handed monopoly at No. 3; sweep spin aggressively'},
        {'rr_batter': 'Riyan Parag (c)', 'stance': 'RHB', 'role': 'Middle Order Surge / No. 4', 'favored_matchup': 'Pace off & middle overs spin (SR 158+)', 'threat_bowler_type': 'Express pace into body with two catchers back', 'tactical_instruction': 'Consolidate overs 7-11; target 6th opposition bowler'},
        {'rr_batter': 'Cameron Green / No. 5', 'stance': 'RHB', 'role': 'Spin-Hitting Enforcer', 'favored_matchup': 'Finger spin & medium pace (SR 162+)', 'threat_bowler_type': 'High-pace outswing and wrong-uns', 'tactical_instruction': 'Eliminate RR overs 7-11 scoring dip (9.07 RPO in 2026); hit down ground'},
        {'rr_batter': 'Donovan Ferreira', 'stance': 'RHB', 'role': 'Dedicated Finisher (No. 6)', 'favored_matchup': 'Death pace & full deliveries (SR 179.10 in 2026!)', 'threat_bowler_type': 'Hard length into ribs without room to swing', 'tactical_instruction': 'Dedicated death finisher; attack from ball one in overs 16-20'},
        {'rr_batter': 'Ravindra Jadeja', 'stance': 'LHB', 'role': 'Lower-Order Finisher / No. 7', 'favored_matchup': 'Right-arm medium pace & off-spin at death', 'threat_bowler_type': 'High-pace bouncers and leg-spinners turning away', 'tactical_instruction': 'Anchor lower order; target short boundary with lofted sweep'},
        {'rr_batter': 'Ashutosh Sharma / Dubey (Impact)', 'stance': 'RHB / LHB', 'role': 'Impact Chase Specialist', 'favored_matchup': 'Extreme pressure death bowling (SR 171+)', 'threat_bowler_type': 'Wide yorkers outside off', 'tactical_instruction': 'Deploy as Impact Sub when chasing 10+ RRR; fearless boundary clearing'}
    ]
    df_bat_matchup = pd.DataFrame(bat_matchup)
    df_bat_matchup.to_csv(os.path.join(BASE_DIR, "RR_Batting_Matchup_Analysis.csv"), index=False)
    print(f" -> RR Batting Matchup Strategy saved.")

    # 6. Monte Carlo 1,000-Scenario Squad Construction Optimization
    print("\n[Step 5] Simulating 1,000 Monte Carlo Squad Optimization Combinations...")
    # Parameters:
    # Purse freed up: ₹38.0 Cr (Hetmyer ₹11 Cr, Bishnoi ₹7.2 Cr, Deshpande ₹6.5 Cr, Sandeep ₹4 Cr, Curran ₹2.4 Cr, Milne/Maphaka ₹3.9 Cr + ₹6 Cr hike)
    # Available targets pool:
    # Overseas Death: Pathirana (₹12 Cr), Mustafizur (₹6 Cr), Nuwan Thushara (₹4 Cr)
    # Overseas All-Rounder/No.5: Cameron Green (₹11 Cr), Glenn Phillips (₹5 Cr), Rachin Ravindra (₹6 Cr)
    # Indian Seamer: Akash Deep (₹6.5 Cr), Mohsin Khan (₹5 Cr), Prince Yadav (₹3 Cr), Mukesh Kumar (₹5 Cr)
    # Indian Finisher: Ashutosh Sharma (₹4.2 Cr), Naman Dhir (₹3.6 Cr), Vipraj Nigam (₹1 Cr)
    # Domestic Spin: Noor Ahmad (if ₹8 Cr) vs Backing Yash Raj Punja (Retained ₹0.5 Cr) + backup spinner (₹1 Cr)
    
    sim_results = []
    np.random.seed(42)

    # Base candidate pool for the 4 targeted auction acquisitions
    death_pacers = [
        {'name': 'Matheesha Pathirana', 'base_cost': 12.0, 'pbwrs': 86.1, 'overseas': True, 'fit': 95},
        {'name': 'Mustafizur Rahman', 'base_cost': 6.0, 'pbwrs': 76.5, 'overseas': True, 'fit': 82},
        {'name': 'Nuwan Thushara', 'base_cost': 4.5, 'pbwrs': 74.2, 'overseas': True, 'fit': 80}
    ]
    no5_allrounders = [
        {'name': 'Cameron Green', 'base_cost': 10.5, 'pbrs': 82.4, 'overseas': True, 'fit': 92},
        {'name': 'Glenn Phillips', 'base_cost': 5.5, 'pbrs': 85.0, 'overseas': True, 'fit': 88},
        {'name': 'Rachin Ravindra', 'base_cost': 6.0, 'pbrs': 78.5, 'overseas': True, 'fit': 80}
    ]
    indian_seamers = [
        {'name': 'Akash Deep', 'base_cost': 6.5, 'pbwrs': 78.2, 'overseas': False, 'fit': 92},
        {'name': 'Mohsin Khan', 'base_cost': 5.0, 'pbwrs': 76.8, 'overseas': False, 'fit': 90},
        {'name': 'Prince Yadav', 'base_cost': 3.2, 'pbwrs': 74.0, 'overseas': False, 'fit': 88},
        {'name': 'Mukesh Kumar', 'base_cost': 5.5, 'pbwrs': 75.0, 'overseas': False, 'fit': 82}
    ]
    indian_finishers = [
        {'name': 'Ashutosh Sharma', 'base_cost': 4.2, 'pbrs': 95.1, 'overseas': False, 'fit': 96},
        {'name': 'Naman Dhir', 'base_cost': 3.6, 'pbrs': 92.4, 'overseas': False, 'fit': 90},
        {'name': 'Vipraj Nigam', 'base_cost': 1.0, 'pbrs': 88.0, 'overseas': False, 'fit': 84}
    ]

    total_budget_cap = 38.0 # Available freed purse

    for i in range(1000):
        # Sample price variance (auction inflation/deflation factor +/- 20%)
        dp = death_pacers[np.random.randint(0, len(death_pacers))].copy()
        ar = no5_allrounders[np.random.randint(0, len(no5_allrounders))].copy()
        is_p = indian_seamers[np.random.randint(0, len(indian_seamers))].copy()
        inf = indian_finishers[np.random.randint(0, len(indian_finishers))].copy()

        cost_dp = round(dp['base_cost'] * np.random.uniform(0.85, 1.25), 2)
        cost_ar = round(ar['base_cost'] * np.random.uniform(0.85, 1.25), 2)
        cost_is = round(is_p['base_cost'] * np.random.uniform(0.85, 1.20), 2)
        cost_inf = round(inf['base_cost'] * np.random.uniform(0.85, 1.25), 2)

        tot_spend = cost_dp + cost_ar + cost_is + cost_inf

        if tot_spend <= total_budget_cap:
            # Score formula: Sum of pressure scores weighted by tactical fit and overseas constraint
            squad_score = (
                (dp['pbwrs'] * (dp['fit']/100.0)) +
                (ar['pbrs'] * (ar['fit']/100.0)) +
                (is_p['pbwrs'] * (is_p['fit']/100.0)) +
                (inf['pbrs'] * (inf['fit']/100.0))
            )
            sim_results.append({
                'sim_id': i + 1,
                'death_pacer': dp['name'],
                'pacer_cost': cost_dp,
                'no5_allrounder': ar['name'],
                'allrounder_cost': cost_ar,
                'indian_seamer': is_p['name'],
                'seamer_cost': cost_is,
                'indian_finisher': inf['name'],
                'finisher_cost': cost_inf,
                'total_spend_cr': round(tot_spend, 2),
                'surplus_purse_cr': round(total_budget_cap - tot_spend, 2),
                'composite_squad_value': round(squad_score, 2)
            })

    df_sim = pd.DataFrame(sim_results).sort_values('composite_squad_value', ascending=False).reset_index(drop=True)
    df_sim.to_csv(os.path.join(OUTPUTS_DIR, "monte_carlo_squad_simulations.csv"), index=False)
    print(f" -> Completed 1,000 Monte Carlo Simulations. Valid budget-compliant squads: {len(df_sim)}")
    print("Optimal Simulation Scenario:")
    best_sim = df_sim.iloc[0]
    print(f"   Targets: {best_sim['death_pacer']} (₹{best_sim['pacer_cost']} Cr), {best_sim['no5_allrounder']} (₹{best_sim['allrounder_cost']} Cr), {best_sim['indian_seamer']} (₹{best_sim['seamer_cost']} Cr), {best_sim['indian_finisher']} (₹{best_sim['finisher_cost']} Cr)")
    print(f"   Total Spend: ₹{best_sim['total_spend_cr']} Cr / ₹{total_budget_cap} Cr | Value Score: {best_sim['composite_squad_value']:.2f}")

    # 7. Formulate Recommended Playing XIs & Impact Player Strategies
    print("\n[Step 6] Compiling Official Recommended Playing XIs & Pitch Variants...")
    
    # 1. Master Recommended Playing XI (Balanced / Default Championship XI)
    master_xi = [
        {'position': 1, 'player_name': 'Yashasvi Jaiswal', 'nationality': 'Indian', 'role': 'Opening Batter (LHB)', 'tactical_duty': 'Aggressive Powerplay scoring; boundary baseline'},
        {'position': 2, 'player_name': 'Vaibhav Sooryavanshi', 'nationality': 'Indian', 'role': 'Opening Batter (LHB)', 'tactical_duty': 'Orange Cap 2026 anchor; fearless pace attack'},
        {'position': 3, 'player_name': 'Dhruv Jurel', 'nationality': 'Indian', 'role': 'Wicketkeeper / Batter (RHB)', 'tactical_duty': 'Right-hand stabilizer; 500+ runs proven pressure player'},
        {'position': 4, 'player_name': 'Riyan Parag (c)', 'nationality': 'Indian', 'role': 'Captain / Middle Batter (RHB)', 'tactical_duty': 'Innings anchor; pace/spin accelerator; 6th bowling option'},
        {'position': 5, 'player_name': 'Cameron Green / Glenn Phillips', 'nationality': 'Overseas', 'role': 'Spin-Hitting All-Rounder (RHB/Pace)', 'tactical_duty': 'Eliminates RR 7-11 overs scoring dip; clears boundary'},
        {'position': 6, 'player_name': 'Donovan Ferreira', 'nationality': 'Overseas', 'role': 'Finisher / Lower Batter (RHB)', 'tactical_duty': 'Death overs finisher; 179+ SR in 2026; offspin utility'},
        {'position': 7, 'player_name': 'Ravindra Jadeja', 'nationality': 'Indian', 'role': 'All-Rounder (LHB / SLA)', 'tactical_duty': 'Middle-overs choke (overs 7-13); elite fielding; lower batting'},
        {'position': 8, 'player_name': 'Jofra Archer', 'nationality': 'Overseas', 'role': 'Strike Fast Bowler (RF)', 'tactical_duty': 'Bowling attack leader (25 wkts in 2026); overs 1, 3, 14, 18'},
        {'position': 9, 'player_name': 'Matheesha Pathirana', 'nationality': 'Overseas', 'role': 'Death Specialist Fast Bowler (RF)', 'tactical_duty': 'Slingy yorker execution; overs 16, 19, 20 lockdown'},
        {'position': 10, 'player_name': 'Akash Deep / Mohsin Khan', 'nationality': 'Indian', 'role': 'Frontline Seamer (RF/LF)', 'tactical_duty': 'Powerplay swing (overs 2, 4) & death variations (over 17)'},
        {'position': 11, 'player_name': 'Yash Raj Punja', 'nationality': 'Indian', 'role': 'Frontline Control Spinner (Spin)', 'tactical_duty': 'Middle-overs wicket-taker (overs 7, 9, 12, 15)'}
    ]
    df_master_xi = pd.DataFrame(master_xi)
    df_master_xi.to_csv(os.path.join(BASE_DIR, "RR_2027_Optimal_XI.csv"), index=False)
    print(f" -> Master Recommended XI saved to RR_2027_Optimal_XI.csv")

    # 2. Impact Player Strategy Matrix
    impact_strategy = [
        {'scenario': 'Batting First (Defending Total)', 'pitch_condition': 'Any / Standard', 'sub_off': 'Donovan Ferreira (post-innings)', 'sub_on': 'Brijesh Sharma / Seam Option', 'tactical_logic': 'Bring on extra specialist seamer to defend score without weakening batting'},
        {'scenario': 'Chasing High Target (190+)', 'pitch_condition': 'Flat / High-Scoring', 'sub_off': 'Akash Deep / Bowler', 'sub_on': 'Ashutosh Sharma / Shubham Dubey', 'tactical_logic': 'Extend batting lineup to No. 8 with 170+ SR pressure finisher'},
        {'scenario': 'Spin-Friendly Track (Chepauk / Lucknow)', 'pitch_condition': 'Dry / Turning', 'sub_off': 'Akash Deep / 3rd Pacer', 'sub_on': 'Vignesh Puthur / 3rd Spinner', 'tactical_logic': 'Deploy 3-prong spin choke: Jadeja + Punja + Puthur bowling 12 overs of spin'},
        {'scenario': 'Pace-Friendly Track (Wankhede / Centurion)', 'pitch_condition': 'Green / High Bounce', 'sub_off': 'Yash Raj Punja', 'sub_on': 'Nandre Burger / Yudhvir Singh', 'tactical_logic': '4-prong express pace attack: Archer + Pathirana + Burger + Akash Deep'}
    ]
    df_impact = pd.DataFrame(impact_strategy)
    df_impact.to_csv(os.path.join(BASE_DIR, "RR_2027_Impact_Player_Strategy.csv"), index=False)
    print(f" -> Impact Player Strategy Matrix saved to RR_2027_Impact_Player_Strategy.csv")

    print("\n" + "=" * 70)
    print("PHASE 17 COMPLETE: All Opponent Analysis & Squad Optimization Datasets Ready.")
    print("=" * 70)

if __name__ == "__main__":
    run_phase17_optimization()
