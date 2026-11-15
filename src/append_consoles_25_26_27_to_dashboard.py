"""
Appends Consoles 25, 26, and 27 to RR_EDGE_Dashboard/app.py cleanly.
"""

import re

APP_PATH = "RR_EDGE_Dashboard/app.py"

with open(APP_PATH, "r", encoding="utf-8") as f:
    content = f.read()

# 1. Update Navigation Radio Options
old_nav_block = '''        "22. Squad WAR, Psychometric Clutch & Injury Resilience Hub",
        "23. SMS Jaipur Aerodynamics & Trajectory Flight Physics",
        "24. Zubin Bharucha High-Performance Academy & Biomechanical Lab"
    ]'''

new_nav_block = '''        "22. Squad WAR, Psychometric Clutch & Injury Resilience Hub",
        "23. SMS Jaipur Aerodynamics & Trajectory Flight Physics",
        "24. Zubin Bharucha High-Performance Academy & Biomechanical Lab",
        "25. Contract Surplus Value & Pareto Frontier Allocation",
        "26. Bayesian Cluster Collapse Hazards & Crisis Survival",
        "27. 9-Franchise Opponent Neutralization & Matchup Predictor"
    ]'''

if old_nav_block in content:
    content = content.replace(old_nav_block, new_nav_block)
    print("Successfully updated sidebar radio navigation.")
else:
    print("Warning: old_nav_block not found directly, checking regex...")
    # try replacing the closing bracket after 24
    pattern = r'("24\. Zubin Bharucha High-Performance Academy & Biomechanical Lab"\s*\])'
    replacement = r'''"24. Zubin Bharucha High-Performance Academy & Biomechanical Lab",
        "25. Contract Surplus Value & Pareto Frontier Allocation",
        "26. Bayesian Cluster Collapse Hazards & Crisis Survival",
        "27. 9-Franchise Opponent Neutralization & Matchup Predictor"
    ]'''
    content = re.sub(pattern, replacement, content)

# 2. Append the 3 new consoles at the end
additional_consoles = """

# -------------------------------------------------------------
# PAGE 25: CONTRACT SURPLUS VALUE & PARETO FRONTIER ALLOCATION
# -------------------------------------------------------------
elif page == "25. Contract Surplus Value & Pareto Frontier Allocation":
    st.markdown(\"\"\"
    <div class='rr-heritage-banner'>
        <div style='display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap;'>
            <div>
                <span class='rr-badge' style='margin-bottom: 8px;'>💰 FINANCIAL ECONOMETRICS & MONEYBALL</span>
                <div style='font-family: Rajdhani, sans-serif; font-size: 2.2rem; font-weight: 900; letter-spacing: 1.5px; color: #FFFFFF;'>
                    CONTRACT SURPLUS VALUE <span style='color: #EA1A85;'>(CSV) & PARETO FRONTIER</span>
                </div>
                <div style='font-family: Montserrat, sans-serif; font-size: 0.95rem; color: #D4AF37; font-weight: 600; margin-top: 4px;'>
                    Sabermetric Auction Valuation: FMV = α + β₁(WAR) + β₂(CLI) + β₃(Scarcity) - Realized Price
                </div>
            </div>
            <div style='text-align: right; margin-top: 10px;'>
                <span style='background: rgba(212, 175, 55, 0.2); border: 1px solid #D4AF37; color: #D4AF37; padding: 6px 14px; border-radius: 20px; font-weight: 700; font-size: 0.85rem;'>
                    PURSE: ₹45.00 CR MINI-AUCTION
                </span>
            </div>
        </div>
    </div>
    \"\"\", unsafe_allow_html=True)

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Matt Henry FMV vs Cost", "₹14.8 Cr vs ₹10.5 Cr", "+₹4.30 Cr CSV (+41.0%)")
    c2.metric("Suyash Sharma FMV vs Cost", "₹8.9 Cr vs ₹5.2 Cr", "+₹3.70 Cr CSV (+71.2%)")
    c3.metric("Marquee Batting Replacement", "₹12.5 Cr vs ₹22.0 Cr", "-₹9.50 Cr Deficit (-43.2%)")
    c4.metric("Plan B Net Surplus Value", "+₹8.40 Cr", "Preserves ₹26.1 Cr Cushion")

    st.markdown("---")
    st.subheader("📊 Individual Player Contract Surplus Value (CSV) Ledger")
    csv_player_path = os.path.join(BASE_DIR, "outputs", "advanced_dimensions", "contract_surplus_player_valuations.csv")
    if os.path.exists(csv_player_path):
        df_cp = pd.read_csv(csv_player_path)
        st.dataframe(df_cp, use_container_width=True)

    st.markdown("---")
    st.subheader("🎯 Pareto-Optimal Mini-Auction Portfolio Allocations (Risk vs Net Win Shares)")
    csv_port_path = os.path.join(BASE_DIR, "outputs", "advanced_dimensions", "contract_surplus_and_pareto_frontiers.csv")
    if os.path.exists(csv_port_path):
        df_ports = pd.read_csv(csv_port_path)
        st.dataframe(df_ports, use_container_width=True)
        
        st.info("💡 **Pareto Frontier Proof**: Portfolio B (RR-EDGE Optimal) strictly dominates Portfolio A across both axes: higher expected Net WAR (5.95 vs 2.95) and dramatically lower volatility/risk (21.5% vs 84.0%), while avoiding the catastrophic -₹7.2 Cr winner's curse deficit.")


# -------------------------------------------------------------
# PAGE 26: BAYESIAN CLUSTER COLLAPSE HAZARDS & CRISIS SURVIVAL
# -------------------------------------------------------------
elif page == "26. Bayesian Cluster Collapse Hazards & Crisis Survival":
    st.markdown(\"\"\"
    <div class='rr-heritage-banner'>
        <div style='display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap;'>
            <div>
                <span class='rr-badge' style='margin-bottom: 8px;'>📉 COX PROPORTIONAL HAZARDS SURVIVAL ANALYSIS</span>
                <div style='font-family: Rajdhani, sans-serif; font-size: 2.2rem; font-weight: 900; letter-spacing: 1.5px; color: #FFFFFF;'>
                    BAYESIAN CLUSTER COLLAPSE <span style='color: #EA1A85;'>HAZARD MODELING</span>
                </div>
                <div style='font-family: Montserrat, sans-serif; font-size: 0.95rem; color: #D4AF37; font-weight: 600; margin-top: 4px;'>
                    Multi-Wicket Domino Effect: h(t|X) = h₀(t) exp(β₁·RRR + β₂·DotSpike + β₃·CVI)
                </div>
            </div>
            <div style='text-align: right; margin-top: 10px;'>
                <span style='background: rgba(16, 185, 129, 0.2); border: 1px solid #10B981; color: #10B981; padding: 6px 14px; border-radius: 20px; font-weight: 700; font-size: 0.85rem;'>
                    HIGH-PRESSURE CALIBRATED
                </span>
            </div>
        </div>
    </div>
    \"\"\", unsafe_allow_html=True)

    h1, h2, h3, h4 = st.columns(4)
    h1.metric("Run Chase >190 Middle Survival", "78.6% (vs 51.4%)", "+27.2% Batting Stability")
    h2.metric("Death Overs Finishing Survival", "71.8% (vs 41.2%)", "+30.6% Icebox Finish (Jurel)")
    h3.metric("Overs 7-11 Opponent Collapse Induction", "49.2% (vs 18.5%)", "+30.7% Chokehold Wickets")
    h4.metric("Dhruv Jurel Dot-Ball Spike in Crisis", "12.4%", "Lowest in Tournament")

    st.markdown("---")
    st.subheader("📋 Empirical Phase-by-Phase Cluster Collapse Hazard Registry")
    hazard_path = os.path.join(BASE_DIR, "outputs", "advanced_dimensions", "cluster_collapse_hazard_models.csv")
    if os.path.exists(hazard_path):
        df_hz = pd.read_csv(hazard_path)
        st.dataframe(df_hz, use_container_width=True)

    st.markdown("---")
    st.subheader("🛡️ Tactical Antidote: The Samson-to-Jadeja/Jurel Pressure Transfer")
    st.markdown(\"\"\"
    * **The 2026 Vulnerability**: When Samson fell in overs 7-10, RR experienced a **48.6% cluster collapse hazard**, losing a 2nd wicket within 8.2 balls due to middle-order dot-ball panic.
    * **The 2027 Antidote**: **Ravindra Jadeja (CVI 0.14)** and **Dhruv Jurel (CVI 0.19)** boast the lowest panic dot-ball rates in T20 cricket. Their rotation strike efficiency suppresses cluster collapse hazard from **48.6% down to 21.4%**.
    \"\"\")


# -------------------------------------------------------------
# PAGE 27: 9-FRANCHISE OPPONENT NEUTRALIZATION & MATCHUP PREDICTOR
# -------------------------------------------------------------
elif page == "27. 9-Franchise Opponent Neutralization & Matchup Predictor":
    st.markdown(\"\"\"
    <div class='rr-heritage-banner'>
        <div style='display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap;'>
            <div>
                <span class='rr-badge' style='margin-bottom: 8px;'>⚔️ COMPETITIVE HEAD-TO-HEAD SIMULATOR</span>
                <div style='font-family: Rajdhani, sans-serif; font-size: 2.2rem; font-weight: 900; letter-spacing: 1.5px; color: #FFFFFF;'>
                    9-FRANCHISE OPPONENT <span style='color: #EA1A85;'>NEUTRALIZATION MATRIX</span>
                </div>
                <div style='font-family: Montserrat, sans-serif; font-size: 0.95rem; color: #D4AF37; font-weight: 600; margin-top: 4px;'>
                    Biomechanically Targeted Weapon Assignment & Head-to-Head Win Probability Optimization
                </div>
            </div>
            <div style='text-align: right; margin-top: 10px;'>
                <span style='background: rgba(234, 26, 133, 0.2); border: 1px solid #EA1A85; color: #FF4D9E; padding: 6px 14px; border-radius: 20px; font-weight: 700; font-size: 0.85rem;'>
                    TOURNAMENT WIN RATE: 68.4%
                </span>
            </div>
        </div>
    </div>
    \"\"\", unsafe_allow_html=True)

    opp_path = os.path.join(BASE_DIR, "outputs", "advanced_dimensions", "opponent_neutralization_matrix.csv")
    if os.path.exists(opp_path):
        df_opp = pd.read_csv(opp_path)
        
        st.subheader("🔍 Interactive Opponent Scouting & Neutralization Selector")
        selected_rival = st.selectbox("Select Target Opponent Franchise:", df_opp["Franchise"].tolist())
        
        row = df_opp[df_opp["Franchise"] == selected_rival].iloc[0]
        
        r1, r2, r3, r4 = st.columns(4)
        r1.metric("Marquee Opponent Threat", str(row["MarqueeThreat"]))
        r2.metric("RR Assigned Weapon", str(row["RR_CounterWeapon"]))
        r3.metric("Projected Win Probability", f"{row['RREDGE_WinProb_Pct']}%", f"{row['WinProbLift_Pct']}% vs Baseline")
        r4.metric("Projected NRR Impact", str(row["NetRR_Impact"]))
        
        st.markdown(f"**🎯 Biomechanical Vulnerability**: {row['ThreatWeakness']}")
        st.markdown(f"**🏟️ SMS Jaipur Field Placement Strategy**: {row['FieldStrategy']}")
        
        st.markdown("---")
        st.subheader("📋 Complete 9-Franchise Opponent Matrix")
        st.dataframe(df_opp, use_container_width=True)
"""

content += additional_consoles

with open(APP_PATH, "w", encoding="utf-8") as f:
    f.write(content)

print("Successfully wrote updated app.py with Consoles 25, 26, 27!")
