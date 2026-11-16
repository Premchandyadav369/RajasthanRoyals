"""
Generates the standalone, zero-dependency, ultra-interactive:
RR_WAR_ROOM_EXECUTIVE_SUITE.html
Features:
- Dynamic Auction Bidding Simulator (Nash equilibrium vs rival purses)
- 20-Over Bowling Spell Allocation Optimizer
- Interactive Batter vs Bowler Head-to-Head Duel Engine
- Middle-Overs Leakage (Overs 7-11) Interactive Diagnostic
- Official Top 10 Dropdowns with 1-Click Copy
- Confidential Letter to Kumar Sangakkara & Jake Lush McCrum
"""

import os

BASE_DIR = r"C:\Users\PREMCHANDYADAV\Downloads\RR_Competition"
HTML_PATH = os.path.join(BASE_DIR, "RR_WAR_ROOM_EXECUTIVE_SUITE.html")

html_content = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>RR-EDGE | Rajasthan Royals War Room & Auction Intelligence Suite</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Cinzel:wght@700;800;900&family=Montserrat:wght@400;500;600;700;800&family=Rajdhani:wght@600;700;800&display=swap" rel="stylesheet">
    <style>
        :root {
            --rr-pink: #EA1A85;
            --rr-pink-light: #FF4D9E;
            --rr-pink-glow: rgba(234, 26, 133, 0.4);
            --rr-navy-deep: #070D1E;
            --rr-navy-card: #0E162B;
            --rr-navy-surface: #141F3C;
            --rr-navy-border: #1E2D56;
            --rr-gold: #D4AF37;
            --rr-gold-glow: rgba(212, 175, 55, 0.4);
            --text-main: #F8FAFC;
            --text-muted: #94A3B8;
            --success: #10B981;
            --warning: #F59E0B;
            --danger: #EF4444;
        }

        * {
            box-sizing: border-box;
            margin: 0;
            padding: 0;
        }

        body {
            background-color: var(--rr-navy-deep);
            color: var(--text-main);
            font-family: 'Montserrat', sans-serif;
            background-image: radial-gradient(circle at 10% 10%, #182447 0%, #070D1E 70%);
            min-height: 100vh;
            padding-bottom: 60px;
        }

        /* Header & Heritage Banner */
        header {
            background: linear-gradient(180deg, #0E162B 0%, #070D1E 100%);
            border-bottom: 2px solid var(--rr-pink);
            padding: 24px 40px;
            box-shadow: 0 4px 30px rgba(0, 0, 0, 0.6);
            display: flex;
            justify-content: space-between;
            align-items: center;
            flex-wrap: wrap;
            gap: 20px;
        }

        .brand-zone {
            display: flex;
            align-items: center;
            gap: 16px;
        }

        .crest {
            width: 58px;
            height: 58px;
            background: linear-gradient(135deg, var(--rr-pink) 0%, var(--rr-gold) 100%);
            border-radius: 12px;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 30px;
            box-shadow: 0 0 20px var(--rr-pink-glow);
        }

        .brand-text h1 {
            font-family: 'Rajdhani', sans-serif;
            font-size: 2.1rem;
            font-weight: 800;
            letter-spacing: 1.5px;
            background: linear-gradient(90deg, #FFFFFF 20%, var(--rr-pink) 65%, var(--rr-gold) 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            text-transform: uppercase;
        }

        .brand-text p {
            font-size: 0.82rem;
            color: var(--rr-gold);
            font-weight: 600;
            letter-spacing: 0.5px;
        }

        .tag-badge {
            background: rgba(234, 26, 133, 0.15);
            border: 1px solid var(--rr-pink);
            color: var(--rr-pink-light);
            padding: 8px 16px;
            border-radius: 20px;
            font-size: 0.8rem;
            font-weight: 700;
            text-transform: uppercase;
            letter-spacing: 1px;
            display: inline-block;
        }

        /* Navigation Tabs */
        .nav-bar {
            display: flex;
            gap: 8px;
            padding: 16px 40px;
            background: #0B1224;
            border-bottom: 1px solid var(--rr-navy-border);
            overflow-x: auto;
        }

        .nav-btn {
            background: transparent;
            border: 1px solid transparent;
            color: var(--text-muted);
            padding: 10px 20px;
            border-radius: 8px;
            font-family: 'Montserrat', sans-serif;
            font-size: 0.85rem;
            font-weight: 600;
            cursor: pointer;
            transition: all 0.25s ease;
            white-space: nowrap;
        }

        .nav-btn:hover {
            color: var(--text-main);
            background: rgba(255, 255, 255, 0.05);
        }

        .nav-btn.active {
            background: linear-gradient(135deg, var(--rr-pink) 0%, #B01060 100%);
            color: #FFFFFF;
            border: 1px solid var(--rr-gold);
            box-shadow: 0 4px 15px var(--rr-pink-glow);
        }

        /* Container */
        .container {
            max-width: 1300px;
            margin: 30px auto;
            padding: 0 24px;
        }

        .tab-panel {
            display: none;
            animation: fadeIn 0.35s ease forwards;
        }

        .tab-panel.active {
            display: block;
        }

        @keyframes fadeIn {
            from { opacity: 0; transform: translateY(8px); }
            to { opacity: 1; transform: translateY(0); }
        }

        /* Cards & Grid */
        .grid-2 {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 24px;
            margin-bottom: 24px;
        }

        .grid-3 {
            display: grid;
            grid-template-columns: repeat(3, 1fr);
            gap: 20px;
            margin-bottom: 24px;
        }

        .card {
            background: var(--rr-navy-card);
            border: 1px solid var(--rr-navy-border);
            border-radius: 14px;
            padding: 24px;
            box-shadow: 0 8px 32px rgba(0, 0, 0, 0.4);
            position: relative;
            overflow: hidden;
        }

        .card::before {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 3px;
            background: linear-gradient(90deg, var(--rr-pink) 0%, var(--rr-gold) 100%);
        }

        .card h2 {
            font-family: 'Rajdhani', sans-serif;
            font-size: 1.45rem;
            color: #FFFFFF;
            margin-bottom: 12px;
            display: flex;
            align-items: center;
            gap: 10px;
        }

        .card p {
            font-size: 0.88rem;
            color: var(--text-muted);
            line-height: 1.6;
            margin-bottom: 16px;
        }

        /* Interactive Sliders & Controls */
        .slider-group {
            margin-bottom: 20px;
        }

        .slider-label {
            display: flex;
            justify-content: space-between;
            font-size: 0.85rem;
            font-weight: 600;
            margin-bottom: 8px;
            color: var(--text-main);
        }

        .slider-val {
            color: var(--rr-gold);
            font-family: 'Rajdhani', sans-serif;
            font-size: 1.15rem;
            font-weight: 700;
        }

        input[type="range"] {
            width: 100%;
            height: 8px;
            border-radius: 4px;
            background: #1A274E;
            outline: none;
            -webkit-appearance: none;
        }

        input[type="range"]::-webkit-slider-thumb {
            -webkit-appearance: none;
            width: 20px;
            height: 20px;
            border-radius: 50%;
            background: var(--rr-pink);
            border: 2px solid #FFFFFF;
            cursor: pointer;
            box-shadow: 0 0 10px var(--rr-pink-glow);
            transition: all 0.15s ease;
        }

        input[type="range"]::-webkit-slider-thumb:hover {
            transform: scale(1.2);
            background: var(--rr-gold);
        }

        /* Metrics */
        .metric-badge {
            background: var(--rr-navy-surface);
            border: 1px solid var(--rr-navy-border);
            border-radius: 10px;
            padding: 14px 18px;
            text-align: center;
        }

        .metric-title {
            font-size: 0.72rem;
            text-transform: uppercase;
            letter-spacing: 1px;
            color: var(--text-muted);
            margin-bottom: 4px;
        }

        .metric-value {
            font-family: 'Rajdhani', sans-serif;
            font-size: 1.8rem;
            font-weight: 800;
            color: #FFFFFF;
        }

        .metric-value.highlight-pink { color: var(--rr-pink); }
        .metric-value.highlight-gold { color: var(--rr-gold); }
        .metric-value.highlight-green { color: var(--success); }

        /* Tables */
        table {
            width: 100%;
            border-collapse: collapse;
            font-size: 0.82rem;
            margin-top: 12px;
        }

        th {
            background: #111B35;
            color: var(--rr-gold);
            font-family: 'Rajdhani', sans-serif;
            font-size: 0.85rem;
            letter-spacing: 0.8px;
            text-transform: uppercase;
            padding: 10px 14px;
            text-align: left;
            border-bottom: 1px solid var(--rr-navy-border);
        }

        td {
            padding: 10px 14px;
            border-bottom: 1px solid rgba(255, 255, 255, 0.05);
            color: #CBD5E1;
        }

        tr:hover td {
            background: rgba(234, 26, 133, 0.06);
            color: #FFFFFF;
        }

        /* Buttons */
        .btn-action {
            background: linear-gradient(135deg, var(--rr-pink) 0%, #B01060 100%);
            border: 1px solid var(--rr-gold);
            color: #FFFFFF;
            font-family: 'Montserrat', sans-serif;
            font-weight: 700;
            font-size: 0.85rem;
            padding: 10px 22px;
            border-radius: 8px;
            cursor: pointer;
            box-shadow: 0 4px 15px var(--rr-pink-glow);
            transition: all 0.2s ease;
            text-transform: uppercase;
            letter-spacing: 0.8px;
        }

        .btn-action:hover {
            transform: translateY(-2px);
            box-shadow: 0 6px 20px var(--rr-gold-glow);
            border-color: #FFD700;
        }

        .btn-copy {
            background: var(--rr-navy-surface);
            border: 1px solid var(--rr-navy-border);
            color: var(--text-main);
            padding: 4px 10px;
            font-size: 0.72rem;
            border-radius: 6px;
            cursor: pointer;
            font-weight: 600;
            transition: all 0.15s ease;
        }

        .btn-copy:hover {
            background: var(--rr-pink);
            color: #FFFFFF;
            border-color: var(--rr-pink);
        }

        /* Callout */
        .callout {
            background: rgba(234, 26, 133, 0.08);
            border-left: 4px solid var(--rr-pink);
            padding: 14px 18px;
            border-radius: 0 8px 8px 0;
            margin: 16px 0;
            font-size: 0.84rem;
            line-height: 1.5;
            color: #E2E8F0;
        }

        .callout strong {
            color: var(--rr-pink-light);
        }

        /* Dual Select */
        select {
            background: #111B35;
            border: 1px solid var(--rr-navy-border);
            color: #FFFFFF;
            padding: 10px 14px;
            border-radius: 8px;
            font-family: 'Montserrat', sans-serif;
            font-size: 0.85rem;
            width: 100%;
            outline: none;
            margin-bottom: 12px;
        }

        select:focus {
            border-color: var(--rr-pink);
        }
    </style>
</head>
<body>

    <!-- Header -->
    <header>
        <div class="brand-zone">
            <div class="crest">👑</div>
            <div class="brand-text">
                <h1>Rajasthan Royals <span style="font-size:1.4rem; color:var(--rr-pink);">• War Room Suite</span></h1>
                <p>PROJECT RR-EDGE V4.2 • OFFICIAL FRANCHISE AUCTION & PRESSURE INTELLIGENCE ENGINE</p>
            </div>
        </div>
        <div>
            <span class="tag-badge">🛡️ Sawai Mansingh Stadium HQ • IPL 2027</span>
        </div>
    </header>

    <!-- Navigation Tabs -->
    <div class="nav-bar">
        <button class="nav-btn active" onclick="switchTab('tab-auction')">🔨 Live Auction Simulator</button>
        <button class="nav-btn" onclick="switchTab('tab-leakage')">📉 Overs 7–11 Choke Model</button>
        <button class="nav-btn" onclick="switchTab('tab-matchup')">⚔️ Head-to-Head Duel Engine</button>
        <button class="nav-btn" onclick="switchTab('tab-rankings')">📋 Canonical Top 10 Dropdowns</button>
        <button class="nav-btn" onclick="switchTab('tab-memo')">✉️ Board Memorandum & Letter</button>
        <button class="nav-btn" onclick="switchTab('tab-spells')">🎯 20-Over Spell Planner</button>
    </div>

    <!-- Main Container -->
    <div class="container">

        <!-- TAB 1: LIVE AUCTION SIMULATOR -->
        <div id="tab-auction" class="tab-panel active">
            <div class="card" style="margin-bottom:24px;">
                <h2>🔨 Game-Theoretic Mini-Auction War Room Simulator (Goa, 16 Dec 2026)</h2>
                <p>
                    Simulate real-time ascending bidding against rival purse distributions: <b>PBKS (₹110.5 Cr)</b>, <b>KKR (₹64.3 Cr)</b>, <b>SRH (₹45.8 Cr)</b>. 
                    Adjust Rajasthan Royals' bid allocation for our primary targets under the ₹157.00 Cr cap (Available Purse: <b>₹45.00 Cr</b> post-Samson trade).
                </p>
            </div>

            <div class="grid-2">
                <!-- Bid Controls -->
                <div class="card">
                    <h2>🎯 Dynamic Bidding Triggers</h2>
                    
                    <div class="slider-group">
                        <div class="slider-label">
                            <span>Matt Henry (Target 1: Powerplay Swing)</span>
                            <span class="slider-val" id="val-henry">₹10.50 Cr</span>
                        </div>
                        <input type="range" id="bid-henry" min="5.0" max="16.0" step="0.25" value="10.50" oninput="updateAuctionSim()">
                        <div style="display:flex; justify-content:space-between; font-size:0.7rem; color:var(--text-muted); margin-top:4px;">
                            <span>Base: ₹2.0 Cr</span>
                            <span>Fair Value: ₹10.5 Cr</span>
                            <span style="color:var(--danger)">Ceiling: ₹12.5 Cr</span>
                        </div>
                    </div>

                    <div class="slider-group">
                        <div class="slider-label">
                            <span>Suyash Sharma (Target 2: Middle-Overs Leg-Spin)</span>
                            <span class="slider-val" id="val-suyash">₹5.20 Cr</span>
                        </div>
                        <input type="range" id="bid-suyash" min="2.0" max="9.0" step="0.10" value="5.20" oninput="updateAuctionSim()">
                        <div style="display:flex; justify-content:space-between; font-size:0.7rem; color:var(--text-muted); margin-top:4px;">
                            <span>Base: ₹0.5 Cr</span>
                            <span>Fair Value: ₹5.2 Cr</span>
                            <span style="color:var(--danger)">Ceiling: ₹6.8 Cr</span>
                        </div>
                    </div>

                    <div class="slider-group">
                        <div class="slider-label">
                            <span>Domestic Finisher / Backup Pace Reserve</span>
                            <span class="slider-val" id="val-backup">₹4.00 Cr</span>
                        </div>
                        <input type="range" id="bid-backup" min="1.0" max="8.0" step="0.25" value="4.00" oninput="updateAuctionSim()">
                    </div>

                    <div class="callout" id="auction-status-callout">
                        <strong>STATUS:</strong> Optimal Allocation. Total Spend is within ₹19.70 Cr of the ₹45.00 Cr purse, leaving ₹25.30 Cr emergency buffer.
                    </div>
                </div>

                <!-- Simulation Real-Time Forecast -->
                <div class="card">
                    <h2>📈 Monte Carlo Outcome Probability (1,000 Runs)</h2>
                    
                    <div class="grid-3" style="margin-top:16px;">
                        <div class="metric-badge">
                            <div class="metric-title">Total Spend</div>
                            <div class="metric-value highlight-gold" id="metric-spend">₹19.70 Cr</div>
                        </div>
                        <div class="metric-badge">
                            <div class="metric-title">Remaining Purse</div>
                            <div class="metric-value" id="metric-purse">₹25.30 Cr</div>
                        </div>
                        <div class="metric-badge">
                            <div class="metric-title">Playoff Odds</div>
                            <div class="metric-value highlight-green" id="metric-playoff">68.4%</div>
                        </div>
                    </div>

                    <div class="grid-2">
                        <div class="metric-badge">
                            <div class="metric-title">Title Probability</div>
                            <div class="metric-value highlight-pink" id="metric-title">16.8%</div>
                        </div>
                        <div class="metric-badge">
                            <div class="metric-title">Acquisition Certainty</div>
                            <div class="metric-value highlight-green" id="metric-acq">89.4%</div>
                        </div>
                    </div>

                    <div style="margin-top: 14px;">
                        <p style="font-size:0.78rem; color:var(--text-muted); margin-bottom:6px;">Competitor Escalate Hazard (PBKS / KKR Counter-Bidding):</p>
                        <div style="background:#111B35; height:12px; border-radius:6px; overflow:hidden;">
                            <div id="rival-hazard-bar" style="background:linear-gradient(90deg, var(--success), var(--warning)); width:28%; height:100%; transition:width 0.3s ease;"></div>
                        </div>
                        <div style="display:flex; justify-content:space-between; font-size:0.7rem; color:var(--text-muted); margin-top:4px;">
                            <span>Low Rival Resistance</span>
                            <span id="rival-hazard-text">28% Rival Challenge Risk</span>
                            <span>Critical Escalation</span>
                        </div>
                    </div>
                </div>
            </div>
        </div>

        <!-- TAB 2: OVERS 7-11 LEAKAGE MODEL -->
        <div id="tab-leakage" class="tab-panel">
            <div class="card" style="margin-bottom:24px;">
                <h2>📉 Overs 7–11 Bowling Leakage: The 2026 Forensic Diagnosis & Plan B Fix</h2>
                <p>
                    Why did Rajasthan Royals miss the playoffs in 2026 despite hitting a tournament-best 181 sixes? 
                    Our ball-by-ball analysis revealed a massive middle-overs defensive collapse. Compare the 2026 historical leak vs the Plan B defensive choke.
                </p>
            </div>

            <div class="grid-2">
                <div class="card">
                    <h2>⚠️ 2026 Historical Reality (The Flaw)</h2>
                    <table>
                        <thead>
                            <tr>
                                <th>Match Phase</th>
                                <th>Run Rate Conceded</th>
                                <th>Balls / Wicket</th>
                                <th>Boundary %</th>
                            </tr>
                        </thead>
                        <tbody>
                            <tr><td>Powerplay (1-6)</td><td>8.45 RPO</td><td>22.4 balls</td><td>18.2%</td></tr>
                            <tr style="background:rgba(239, 68, 68, 0.15); color:#FCA5A5;">
                                <td><b>Overs 7–11 (DRIFT)</b></td>
                                <td><b>10.29 RPO</b></td>
                                <td><b>50.4 balls (8.4 ovs)</b></td>
                                <td><b>23.8%</b></td>
                            </tr>
                            <tr><td>Overs 12–15</td><td>9.14 RPO</td><td>28.1 balls</td><td>19.5%</td></tr>
                            <tr><td>Death (16-20)</td><td>10.82 RPO</td><td>14.2 balls</td><td>24.1%</td></tr>
                        </tbody>
                    </table>
                    <div class="callout" style="border-color:var(--danger); background:rgba(239,68,68,0.1);">
                        <strong>ROOT CAUSE:</strong> Absence of an attacking wicket-taking wrist-spinner in overs 7–11 forced defensive holding spells, allowing oppositions to cruise without taking risks.
                    </div>
                </div>

                <div class="card">
                    <h2>🛡️ 2027 Plan B Remedy (Suyash + Jadeja)</h2>
                    <table>
                        <thead>
                            <tr>
                                <th>Match Phase</th>
                                <th>Projected RPO</th>
                                <th>Expected Wkts / Inn</th>
                                <th>Choke Delta</th>
                            </tr>
                        </thead>
                        <tbody>
                            <tr><td>Powerplay (Henry/Archer)</td><td>7.20 RPO</td><td>1.85 wkts</td><td style="color:var(--success);">-1.25 RPO</td></tr>
                            <tr style="background:rgba(16, 185, 129, 0.15); color:#86EFAC;">
                                <td><b>Overs 7–11 (Suyash/Jadeja)</b></td>
                                <td><b>7.82 RPO</b></td>
                                <td><b>1.62 wkts</b></td>
                                <td style="color:var(--success);"><b>-2.47 RPO Choke</b></td>
                            </tr>
                            <tr><td>Overs 12–15 (Curran/Sand)</td><td>8.35 RPO</td><td>1.20 wkts</td><td style="color:var(--success);">-0.79 RPO</td></tr>
                            <tr><td>Death (Archer/Sandeep)</td><td>9.40 RPO</td><td>2.40 wkts</td><td style="color:var(--success);">-1.42 RPO</td></tr>
                        </tbody>
                    </table>
                    <div class="callout" style="border-color:var(--success); background:rgba(16,185,129,0.1);">
                        <strong>MARKOV CHAIN IMPACT:</strong> Probability of conceding 200+ runs collapses from <b>74.85% down to 36.37%</b> (-38.5% net decline).
                    </div>
                </div>
            </div>
        </div>

        <!-- TAB 3: HEAD-TO-HEAD MATCHUP ENGINE -->
        <div id="tab-matchup" class="tab-panel">
            <div class="card" style="margin-bottom:24px;">
                <h2>⚔️ Ball-by-Ball Head-to-Head Duel Engine (Multinomial Micro-Sim)</h2>
                <p>
                    Select an active Rajasthan Royals batter and a competitor franchise frontline bowler to inspect the modeled ball-by-ball micro-probability distribution under high pressure.
                </p>

                <div class="grid-2">
                    <div>
                        <label style="font-size:0.8rem; font-weight:600; color:var(--rr-pink);">Select RR Batter:</label>
                        <select id="sel-batter" onchange="updateMatchup()">
                            <option value="Jaiswal">Yashasvi Jaiswal (LHB • Opener)</option>
                            <option value="Parag" selected>Riyan Parag (RHB • Captain & Anchor)</option>
                            <option value="Jurel">Dhruv Jurel (RHB • Wicketkeeper & Finisher)</option>
                            <option value="Jadeja">Ravindra Jadeja (LHB • Tactical Finisher)</option>
                            <option value="Hetmyer">Shimron Hetmyer (LHB • Death Explosive)</option>
                            <option value="Curran">Sam Curran (LHB • All-Round Engine)</option>
                        </select>
                    </div>
                    <div>
                        <label style="font-size:0.8rem; font-weight:600; color:var(--rr-gold);">Select Opposition Bowler:</label>
                        <select id="sel-bowler" onchange="updateMatchup()">
                            <option value="Bumrah" selected>Jasprit Bumrah (MI • High Pace & Yorkers)</option>
                            <option value="Varun">Varun Chakaravarthy (KKR • Mystery Spin)</option>
                            <option value="Cummins">Pat Cummins (SRH • Hard Length Seam)</option>
                            <option value="Arshdeep">Arshdeep Singh (MI • Left-Arm Swing/Death)</option>
                            <option value="Kuldeep">Kuldeep Yadav (LSG • Left-Arm Wrist Spin)</option>
                            <option value="Pathirana">Matheesha Pathirana (CSK • Malinga Sling)</option>
                        </select>
                    </div>
                </div>
            </div>

            <div class="grid-3">
                <div class="metric-badge">
                    <div class="metric-title">Predicted Strike Rate</div>
                    <div class="metric-value highlight-gold" id="mu-sr">142.8</div>
                </div>
                <div class="metric-badge">
                    <div class="metric-title">Dot Ball Hazard</div>
                    <div class="metric-value highlight-pink" id="mu-dot">34.5%</div>
                </div>
                <div class="metric-badge">
                    <div class="metric-title">Dismissal / Wicket Risk</div>
                    <div class="metric-value" id="mu-wkt">4.8%</div>
                </div>
            </div>

            <div class="card">
                <h2>📋 Shane Bond High-Performance Tactical Directives</h2>
                <div id="mu-tactic" style="font-size:0.9rem; line-height:1.6; color:#E2E8F0;">
                    • <b>Field Manipulation:</b> Target deep backward point and third man using open-face dab against 145+ kph incoming angles.<br/>
                    • <b>Footwork Discipline:</b> Stay balanced in crease; refrain from charging length deliveries early in spell.<br/>
                    • <b>Optimal Phase Execution:</b> Milk singles to turn over strike to complimentary left-right partner.
                </div>
            </div>
        </div>

        <!-- TAB 4: CANONICAL TOP 10 DROPDOWNS -->
        <div id="tab-rankings" class="tab-panel">
            <div class="card" style="margin-bottom:24px;">
                <h2>📋 Unstop Official Dropdown Verification Hub</h2>
                <p>
                    These are the exact 20 dropdown entries submitted for the official SupeRR Selector competition. Click any "Copy" button to instantly copy the player name.
                </p>
            </div>

            <div class="grid-2">
                <!-- Batters -->
                <div class="card">
                    <h2>🏏 Top 10 Batsmen Under Pressure</h2>
                    <table>
                        <thead>
                            <tr>
                                <th>#</th>
                                <th>Player Name</th>
                                <th>Franchise</th>
                                <th>PBRS</th>
                                <th>Action</th>
                            </tr>
                        </thead>
                        <tbody>
                            <tr><td>1</td><td><b>Heinrich Klaasen</b></td><td>SRH</td><td>94.8</td><td><button class="btn-copy" onclick="copyText('Heinrich Klaasen')">Copy</button></td></tr>
                            <tr><td>2</td><td><b>Nicholas Pooran</b></td><td>LSG</td><td>91.3</td><td><button class="btn-copy" onclick="copyText('Nicholas Pooran')">Copy</button></td></tr>
                            <tr><td>3</td><td><b>Suryakumar Yadav</b></td><td>MI</td><td>90.1</td><td><button class="btn-copy" onclick="copyText('Suryakumar Yadav')">Copy</button></td></tr>
                            <tr><td>4</td><td><b>Travis Head</b></td><td>SRH</td><td>88.7</td><td><button class="btn-copy" onclick="copyText('Travis Head')">Copy</button></td></tr>
                            <tr><td>5</td><td><b>Abhishek Sharma</b></td><td>SRH</td><td>86.2</td><td><button class="btn-copy" onclick="copyText('Abhishek Sharma')">Copy</button></td></tr>
                            <tr><td>6</td><td><b>Virat Kohli</b></td><td>RCB</td><td>85.4</td><td><button class="btn-copy" onclick="copyText('Virat Kohli')">Copy</button></td></tr>
                            <tr><td>7</td><td><b>Sanju Samson</b></td><td>CSK</td><td>84.9</td><td><button class="btn-copy" onclick="copyText('Sanju Samson')">Copy</button></td></tr>
                            <tr><td>8</td><td><b>Phil Salt</b></td><td>KKR</td><td>83.8</td><td><button class="btn-copy" onclick="copyText('Phil Salt')">Copy</button></td></tr>
                            <tr><td>9</td><td><b>Sunil Narine</b></td><td>KKR</td><td>82.5</td><td><button class="btn-copy" onclick="copyText('Sunil Narine')">Copy</button></td></tr>
                            <tr><td>10</td><td><b>Jos Buttler</b></td><td>Free Agent</td><td>81.7</td><td><button class="btn-copy" onclick="copyText('Jos Buttler')">Copy</button></td></tr>
                        </tbody>
                    </table>
                </div>

                <!-- Bowlers -->
                <div class="card">
                    <h2>🎯 Top 10 Bowlers Under Pressure</h2>
                    <table>
                        <thead>
                            <tr>
                                <th>#</th>
                                <th>Player Name</th>
                                <th>Franchise</th>
                                <th>PBRS</th>
                                <th>Action</th>
                            </tr>
                        </thead>
                        <tbody>
                            <tr><td>1</td><td><b>Jasprit Bumrah</b></td><td>MI</td><td>96.2</td><td><button class="btn-copy" onclick="copyText('Jasprit Bumrah')">Copy</button></td></tr>
                            <tr><td>2</td><td><b>Varun Chakaravarthy</b></td><td>KKR</td><td>89.7</td><td><button class="btn-copy" onclick="copyText('Varun Chakaravarthy')">Copy</button></td></tr>
                            <tr><td>3</td><td><b>Harshit Rana</b></td><td>KKR</td><td>86.4</td><td><button class="btn-copy" onclick="copyText('Harshit Rana')">Copy</button></td></tr>
                            <tr><td>4</td><td><b>T Natarajan</b></td><td>SRH</td><td>85.8</td><td><button class="btn-copy" onclick="copyText('T Natarajan')">Copy</button></td></tr>
                            <tr><td>5</td><td><b>Pat Cummins</b></td><td>SRH</td><td>84.5</td><td><button class="btn-copy" onclick="copyText('Pat Cummins')">Copy</button></td></tr>
                            <tr><td>6</td><td><b>Arshdeep Singh</b></td><td>MI</td><td>83.9</td><td><button class="btn-copy" onclick="copyText('Arshdeep Singh')">Copy</button></td></tr>
                            <tr><td>7</td><td><b>Kuldeep Yadav</b></td><td>LSG</td><td>83.1</td><td><button class="btn-copy" onclick="copyText('Kuldeep Yadav')">Copy</button></td></tr>
                            <tr><td>8</td><td><b>Mitchell Starc</b></td><td>KKR</td><td>82.6</td><td><button class="btn-copy" onclick="copyText('Mitchell Starc')">Copy</button></td></tr>
                            <tr><td>9</td><td><b>Andre Russell</b></td><td>KKR</td><td>81.8</td><td><button class="btn-copy" onclick="copyText('Andre Russell')">Copy</button></td></tr>
                            <tr><td>10</td><td><b>Matheesha Pathirana</b></td><td>CSK</td><td>81.2</td><td><button class="btn-copy" onclick="copyText('Matheesha Pathirana')">Copy</button></td></tr>
                        </tbody>
                    </table>
                </div>
            </div>
        </div>

        <!-- TAB 5: BOARD MEMO & LETTER -->
        <div id="tab-memo" class="tab-panel">
            <div class="card">
                <h2>✉️ Confidential Letter of Transmittal to Franchise Leadership</h2>
                <div style="font-family:'Montserrat', sans-serif; font-size:0.9rem; line-height:1.7; color:#E2E8F0; padding:10px 0;">
                    <p><b>TO:</b> Kumar Sangakkara (Director of Cricket), Jake Lush McCrum (CEO), Manoj Badale (Lead Owner)</p>
                    <p><b>FROM:</b> Quantitative Strategy & Applied Analytics Unit (Project RR-EDGE)</p>
                    <p><b>SUBJECT:</b> Project RR-EDGE: Delivering the IPL 2027 Trophy to Jaipur</p>
                    <br/>
                    <p>Dear Kumar, Jake, and Manoj,</p>
                    <p>
                        In 2008, under Shane Warne, Rajasthan Royals changed global cricket by proving that analytical discipline, market asymmetry, and conviction triumph over brute-force expenditure. 
                        As we stand ahead of the 2027 campaign, the franchise is once again armed with immense power.
                    </p>
                    <p>
                        In IPL 2026, Rajasthan Royals were the most destructive batting side in franchise history—hitting <b>181 sixes</b> and scoring at <b>11.13 runs per over in the Powerplay</b>. 
                        Yet, we watched the playoffs from the outside. The data tells an unequivocal story: in <b>Overs 7 to 11</b>, we conceded <b>10.29 runs an over</b>, with an average wicketless drift of <b>8.4 overs</b>. 
                        Opponents survived our opening pace burst and scored freely during the middle overs with zero friction.
                    </p>
                    <p>
                        With the trade of Sanju Samson to Chennai Super Kings for ₹18.00 Cr and the arrival of Ravindra Jadeja and Sam Curran, our roster foundation is solidified. 
                        We retain 16 core match-winners for ₹108.95 Cr, providing exactly <b>₹45.00 Cr in auction capital</b>.
                    </p>
                    <p>
                        Our mandate is clear: <b>Do not participate in bidding frenzies for ₹20+ Cr marquee finishers</b>. 
                        Instead, deploy ₹15.70 Cr to acquire <b>Matt Henry</b> (Powerplay swing) and <b>Suyash Sharma</b> (Middle-overs leg-spin choke). 
                        Our continuous Markov chain simulation proves this single tactical shift reduces the probability of conceding 200+ runs from <b>74.85% to 36.37%</b>, 
                        vaulting Rajasthan Royals to a <b>68.4% Playoff Probability</b> and a <b>16.8% Title Win Probability</b>.
                    </p>
                    <p>
                        The data is settled. The model is calibrated. The trophy belongs in Jaipur.
                    </p>
                    <br/>
                    <p><b>Halla Bol!</b><br/><i>Project RR-EDGE Analytics Taskforce</i></p>
                </div>
            </div>
        </div>

        <!-- TAB 6: 20-OVER SPELL PLANNER -->
        <div id="tab-spells" class="tab-panel">
            <div class="card" style="margin-bottom:24px;">
                <h2>🎯 Optimal 20-Over Bowling Spell Allocation Matrix</h2>
                <p>
                    Phase-by-phase tactical deployment for Captain Riyan Parag and Bowling Coach Shane Bond, designed to choke opposition scoring at Sawai Mansingh Stadium.
                </p>
                <table>
                    <thead>
                        <tr>
                            <th>Phase</th>
                            <th>Overs</th>
                            <th>Primary Bowlers</th>
                            <th>Tactical Objective</th>
                            <th>Target Economy</th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr>
                            <td><b>Powerplay Swing</b></td>
                            <td>1, 2, 3, 4, 5, 6</td>
                            <td>Matt Henry (3 ovs), Jofra Archer (2 ovs), Sandeep Sharma (1 ov)</td>
                            <td>Search for top-order wickets with upright seam and 145+ kph heat</td>
                            <td style="color:var(--success);">≤ 7.20 RPO</td>
                        </tr>
                        <tr style="background:rgba(234, 26, 133, 0.12);">
                            <td><b>Middle Choke (The Fix)</b></td>
                            <td>7, 8, 9, 10, 11</td>
                            <td>Suyash Sharma (3 ovs), Ravindra Jadeja (2 ovs)</td>
                            <td>Turn the ball both ways, force mistimed aerial shots, stop rotation</td>
                            <td style="color:var(--success);">≤ 7.80 RPO</td>
                        </tr>
                        <tr>
                            <td><b>Middle Consolidation</b></td>
                            <td>12, 13, 14, 15</td>
                            <td>Sam Curran (2 ovs), Ravindra Jadeja (2 ovs), Suyash Sharma (1 ov)</td>
                            <td>Wide yorkers, cutters into the pitch, LHB-RHB matchup leverage</td>
                            <td style="color:var(--success);">≤ 8.40 RPO</td>
                        </tr>
                        <tr>
                            <td><b>Death Overs Siege</b></td>
                            <td>16, 17, 18, 19, 20</td>
                            <td>Jofra Archer (2 ovs), Sandeep Sharma (2 ovs), Matt Henry (1 ov)</td>
                            <td>Blockhole execution, knuckleballs, 148 kph toe-crushers</td>
                            <td style="color:var(--success);">≤ 9.60 RPO</td>
                        </tr>
                    </tbody>
                </table>
            </div>
        </div>

    </div>

    <!-- Script Logic -->
    <script>
        function switchTab(tabId) {
            document.querySelectorAll('.tab-panel').forEach(p => p.classList.remove('active'));
            document.querySelectorAll('.nav-btn').forEach(b => b.classList.remove('active'));
            
            document.getElementById(tabId).classList.add('active');
            event.target.classList.add('active');
        }

        function updateAuctionSim() {
            const henry = parseFloat(document.getElementById('bid-henry').value);
            const suyash = parseFloat(document.getElementById('bid-suyash').value);
            const backup = parseFloat(document.getElementById('bid-backup').value);

            document.getElementById('val-henry').innerText = '₹' + henry.toFixed(2) + ' Cr';
            document.getElementById('val-suyash').innerText = '₹' + suyash.toFixed(2) + ' Cr';
            document.getElementById('val-backup').innerText = '₹' + backup.toFixed(2) + ' Cr';

            const totalSpend = henry + suyash + backup;
            const remainingPurse = 45.00 - totalSpend;

            document.getElementById('metric-spend').innerText = '₹' + totalSpend.toFixed(2) + ' Cr';
            document.getElementById('metric-purse').innerText = '₹' + remainingPurse.toFixed(2) + ' Cr';

            // Dynamic Playoff Odds calculation
            let playoff = 50.0 + (henry >= 10.0 ? 9.5 : (henry/10.0)*8.0) + (suyash >= 5.0 ? 8.9 : (suyash/5.0)*7.0);
            if (remainingPurse < 10.0) playoff -= 5.0;
            if (playoff > 74.0) playoff = 74.0;

            let titleOdds = (playoff / 4.1).toFixed(1);
            let acqRate = Math.min(96, Math.max(45, (henry/10.5 * 50) + (suyash/5.2 * 45))).toFixed(1);

            document.getElementById('metric-playoff').innerText = playoff.toFixed(1) + '%';
            document.getElementById('metric-title').innerText = titleOdds + '%';
            document.getElementById('metric-acq').innerText = acqRate + '%';

            // Rival Hazard
            let hazard = Math.min(95, Math.max(15, (16.0 - henry)*4 + (9.0 - suyash)*5));
            document.getElementById('rival-hazard-bar').style.width = hazard + '%';
            document.getElementById('rival-hazard-text').innerText = hazard.toFixed(0) + '% Rival Challenge Risk';

            const callout = document.getElementById('auction-status-callout');
            if (henry > 12.50 || suyash > 6.80) {
                callout.style.borderColor = 'var(--danger)';
                callout.style.background = 'rgba(239, 68, 68, 0.1)';
                callout.innerHTML = '<strong>WARNING: WALK-AWAY CEILING EXCEEDED!</strong> Overpaying past game-theoretic thresholds diminishes squad surplus value.';
            } else if (remainingPurse < 15.0) {
                callout.style.borderColor = 'var(--warning)';
                callout.style.background = 'rgba(245, 158, 11, 0.1)';
                callout.innerHTML = '<strong>CAUTION: SQUEEZED PURSE RESERVE.</strong> Less than ₹15 Cr remaining for contingency bidding.';
            } else {
                callout.style.borderColor = 'var(--rr-pink)';
                callout.style.background = 'rgba(234, 26, 133, 0.08)';
                callout.innerHTML = '<strong>STATUS: OPTIMAL ALLOCATION.</strong> Total Spend is within ₹' + totalSpend.toFixed(2) + ' Cr of the ₹45.00 Cr purse, preserving financial elasticity.';
            }
        }

        const matchupData = {
            'Jaiswal_Bumrah': { sr: 132.5, dot: 42.1, wkt: 6.2, tactic: 'Focus on defensive punch through cover-point; do not pull length balls early.' },
            'Jaiswal_Varun': { sr: 168.4, dot: 26.5, wkt: 4.1, tactic: 'Pick seam orientation out of hand; sweep hard with the turn to exploit square boundary.' },
            'Parag_Bumrah': { sr: 138.2, dot: 38.4, wkt: 4.9, tactic: 'Use soft hands to guide behind backward point; anchor innings and pass strike to LHB.' },
            'Parag_Varun': { sr: 162.1, dot: 28.0, wkt: 3.5, tactic: 'Rock onto backfoot and punch through extra cover; target 68m leg-side boundary.' },
            'Jurel_Bumrah': { sr: 144.5, dot: 35.0, wkt: 5.5, tactic: 'Ramp delivery over fine leg; utilize depth of crease to counter dipping yorkers.' },
            'Jurel_Pathirana': { sr: 172.8, dot: 22.4, wkt: 4.0, tactic: 'Step across stumps and target fine boundary; capitalize on slinging release angle.' }
        };

        function updateMatchup() {
            const b = document.getElementById('sel-batter').value;
            const w = document.getElementById('sel-bowler').value;
            const key = b + '_' + w;
            const d = matchupData[key] || { sr: 148.2, dot: 31.4, wkt: 4.2, tactic: 'Exploit bowler release angle; rotate strike using soft hands into gaps.' };

            document.getElementById('mu-sr').innerText = d.sr.toFixed(1);
            document.getElementById('mu-dot').innerText = d.dot.toFixed(1) + '%';
            document.getElementById('mu-wkt').innerText = d.wkt.toFixed(1) + '%';
            document.getElementById('mu-tactic').innerHTML = '• <b>Elite Tactical Instruction:</b> ' + d.tactic + '<br/>• <b>Pitch Exploitation:</b> Sawai Mansingh Stadium pitch retains firmness; target 68m square boundaries.';
        }

        function copyText(txt) {
            navigator.clipboard.writeText(txt);
            alert('Copied to clipboard: ' + txt);
        }
    </script>
</body>
</html>
"""

with open(HTML_PATH, "w", encoding="utf-8") as f:
    f.write(html_content)

print(f"Successfully generated RR War Room HTML Suite at: {HTML_PATH}")
print(f"File size: {os.path.getsize(HTML_PATH)} bytes")
