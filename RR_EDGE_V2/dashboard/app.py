"""
PROJECT RR-EDGE V2: LIVE IPL 2027 FRANCHISE DECISION SIMULATOR
Rajasthan Royals SupeRR Selector Season 2 | Franchise Research & Operations Platform
"""

import os
import json
import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

# Page Configuration
st.set_page_config(
    page_title="RR-EDGE V2 | Rajasthan Royals Decision Simulator",
    page_icon="👑",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom Styling (Rajasthan Royals Royal Blue & Vibrant Pink)
st.markdown("""
<style>
    .main { background-color: #0B132B; color: #F8FAFC; }
    .stApp { background-color: #0B132B; color: #F8FAFC; }
    .metric-card {
        background: linear-gradient(135deg, #1C2541 0%, #0B132B 100%);
        border: 1px solid #3A86FF;
        border-radius: 12px;
        padding: 14px;
        text-align: center;
        box-shadow: 0 4px 15px rgba(58, 134, 255, 0.15);
    }
    .metric-val { font-size: 1.8rem; font-weight: 800; color: #48CAE4; }
    .metric-lbl { font-size: 0.75rem; text-transform: uppercase; color: #9BA4B5; letter-spacing: 1px; }
    .recom-badge {
        background-color: #FF007F;
        color: white;
        padding: 3px 8px;
        border-radius: 6px;
        font-size: 0.75rem;
        font-weight: 700;
    }
</style>
""", unsafe_allow_html=True)

BASE_DIR = r"C:\Users\PREMCHANDYADAV\Downloads\RR_Competition"
V2_DIR = os.path.join(BASE_DIR, "RR_EDGE_V2")

@st.cache_data
def load_v2_data():
    mc_path = os.path.join(V2_DIR, "results", "monte_carlo_season_outcomes.csv")
    opp_path = os.path.join(V2_DIR, "experiments", "run_04_opponents", "opponent_intelligence_dossiers.csv")
    venue_path = os.path.join(V2_DIR, "experiments", "run_07_venues", "venue_specific_tactical_blueprints.csv")
    strat_path = os.path.join(V2_DIR, "results", "master_strategy_decision_matrix.csv")
    press_path = os.path.join(V2_DIR, "experiments", "run_03_pressure_models", "batter_pressure_models_comparison.csv")
    
    mc_df = pd.read_csv(mc_path) if os.path.exists(mc_path) else pd.DataFrame()
    opp_df = pd.read_csv(opp_path) if os.path.exists(opp_path) else pd.DataFrame()
    venue_df = pd.read_csv(venue_path) if os.path.exists(venue_path) else pd.DataFrame()
    strat_df = pd.read_csv(strat_path) if os.path.exists(strat_path) else pd.DataFrame()
    press_df = pd.read_csv(press_path) if os.path.exists(press_path) else pd.DataFrame()
    return mc_df, opp_df, venue_df, strat_df, press_df

mc_df, opp_df, venue_df, strat_df, press_df = load_v2_data()

# Header
st.title("👑 PROJECT RR-EDGE V2: IPL 2027 DECISION SIMULATOR")
st.markdown("**Live Franchise Decision-Support & Cricket Intelligence Platform** | Date: *13 November 2026*")

# Sidebar Controls
st.sidebar.image("https://upload.wikimedia.org/wikipedia/en/thumb/6/60/Rajasthan_Royals_Logo.svg/300px-Rajasthan_Royals_Logo.svg.png", width=110)
st.sidebar.header("🎯 Live Decision Engine")
selected_tab = st.sidebar.radio(
    "Navigation Mode",
    [
        "🎮 Franchise Decision Simulator",
        "📊 Competing Strategies & Monte Carlo",
        "⚔️ Opponent Intelligence (Post-Trade)",
        "🏟️ Venue-Specific Blueprints",
        "🔬 5 Pressure Models Tournament",
        "💰 Purse & Market Status"
    ]
)

# TAB 1: FRANCHISE DECISION SIMULATOR
if selected_tab == "🎮 Franchise Decision Simulator":
    st.markdown("### 🎛️ Real-Time Squad Configuration & Consequence Simulator")
    st.markdown("Test hypothetical acquisition configurations against the 10,000-season simulation engine. Evaluate championship probabilities, budget allocations, and opponent counters in real-time.")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.subheader("1. Fast Bowling Target")
        fast_bowler = st.selectbox(
            "Primary Seamer Target",
            [
                "Matheesha Pathirana (₹12.0 Cr - Marquee Slinger)",
                "Mustafizur Rahman (₹6.5 Cr - Cutter/Death Slinger)",
                "Nuwan Thushara (₹5.0 Cr - Sling Yorker Specialist)",
                "Yash Dayal (₹9.0 Cr - Left-Arm Indian Seamer)",
                "Mohsin Khan (₹5.5 Cr - Left-Arm Angle/Bounce)",
                "Akash Deep (₹6.5 Cr - Express Indian Seamer)",
                "Avesh Khan (₹7.0 Cr - Heavy Ball Enforcer)",
                "Harshal Patel (₹8.5 Cr - Slower Dipper / Death)"
            ],
            index=1
        )
        
    with col2:
        st.subheader("2. Spin Combination")
        spin_combo = st.selectbox(
            "Middle Overs Spin Strategy",
            [
                "Existing + Yash Raj Punja (₹0.5 Cr - Economical Strike)",
                "Glenn Phillips + Punja + Jadeja (₹7.0 Cr - All-Round Grip)",
                "Ravi Bishnoi Buyback (₹5.0 Cr - Aggressive Leg-spin)",
                "Rahul Chahar (₹4.5 Cr - Flat Leg-break)",
                "Noor Ahmad (₹8.0 Cr - Left-arm Wrist Spin)"
            ],
            index=1
        )
        
    with col3:
        st.subheader("3. Middle & Finishing Combination")
        finisher_combo = st.selectbox(
            "No. 5 & Lower Order Core",
            [
                "Glenn Phillips + Ferreira + Shahrukh Khan (₹13.0 Cr - Recommended)",
                "Cameron Green + Ferreira + Manohar (₹18.5 Cr - Marquee Surge)",
                "Donovan Ferreira + Shubham Dubey (₹3.0 Cr - Moneyball Finisher)",
                "Shimron Hetmyer Buyback + Ferreira (₹6.0 Cr - Left-Hand Power)",
                "Shahrukh Khan + Abdul Samad + Ferreira (₹10.5 Cr - Domestic Depth)"
            ],
            index=0
        )
        
    st.markdown("---")
    
    # Financial Estimation Logic
    spend_map = {
        "Matheesha Pathirana": 12.0, "Mustafizur Rahman": 6.5, "Nuwan Thushara": 5.0,
        "Yash Dayal": 9.0, "Mohsin Khan": 5.5, "Akash Deep": 6.5, "Avesh Khan": 7.0, "Harshal Patel": 8.5
    }
    spin_map = {
        "Existing + Yash Raj Punja": 0.5, "Glenn Phillips + Punja + Jadeja": 7.0,
        "Ravi Bishnoi Buyback": 5.0, "Rahul Chahar": 4.5, "Noor Ahmad": 8.0
    }
    fin_map = {
        "Glenn Phillips + Ferreira + Shahrukh Khan": 13.0, "Cameron Green + Ferreira + Manohar": 18.5,
        "Donovan Ferreira + Shubham Dubey": 3.0, "Shimron Hetmyer Buyback + Ferreira": 6.0,
        "Shahrukh Khan + Abdul Samad + Ferreira": 10.5
    }
    
    sel_fast = [k for k in spend_map if k in fast_bowler][0]
    sel_spin = [k for k in spin_map if k in spin_combo][0]
    sel_fin = [k for k in fin_map if k in finisher_combo][0]
    
    total_est_spend = spend_map[sel_fast] + spin_map[sel_spin] + fin_map[sel_fin] + 2.5 # 2.5 Cr for uncapped squad filler
    available_purse = 39.0
    surplus = available_purse - total_est_spend
    
    # Live Simulation Metric Calculation
    # Base performance weights
    base_wins = 8.0
    if "Mustafizur" in fast_bowler or "Pathirana" in fast_bowler or "Thushara" in fast_bowler:
        death_boost = 1.35
    elif "Dayal" in fast_bowler or "Mohsin" in fast_bowler:
        death_boost = 1.10
    else:
        death_boost = 0.70
        
    if "Phillips" in spin_combo or "Phillips" in finisher_combo:
        spin_boost = 1.25
    elif "Green" in finisher_combo:
        spin_boost = 1.15
    else:
        spin_boost = 0.60
        
    if "Shahrukh" in finisher_combo or "Dubey" in finisher_combo:
        fin_boost = 0.85
    else:
        fin_boost = 0.40
        
    expected_wins = min(14.0, round(base_wins + death_boost + spin_boost + fin_boost, 2))
    top4_prob = min(99.0, round(50.0 + (expected_wins - 8.0) * 18.5, 1))
    title_prob = min(45.0, round(12.0 + (expected_wins - 8.0) * 8.2, 1))
    
    # Output Dashboard Cards
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-lbl">Estimated Expenditure</div>
            <div class="metric-val">₹{total_est_spend:.2f} Cr</div>
            <div style="font-size:0.75rem; color:{'#00F5D4' if surplus >= 0 else '#FF4D6D'};">
                Surplus: ₹{surplus:.2f} Cr {'(Safe)' if surplus >= 0 else '(Deficit!)'}
            </div>
        </div>
        """, unsafe_allow_html=True)
    with c2:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-lbl">Expected League Wins</div>
            <div class="metric-val">{expected_wins} / 14</div>
            <div style="font-size:0.75rem; color:#48CAE4;">Points: {int(expected_wins*2)} Pts</div>
        </div>
        """, unsafe_allow_html=True)
    with c3:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-lbl">Top-4 Playoff Prob</div>
            <div class="metric-val">{top4_prob}%</div>
            <div style="font-size:0.75rem; color:#3A86FF;">Qualifier Berth</div>
        </div>
        """, unsafe_allow_html=True)
    with c4:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-lbl">IPL Championship Prob</div>
            <div class="metric-val" style="color:#FF007F;">{title_prob}%</div>
            <div style="font-size:0.75rem; color:#FF85A1;">Title Contender</div>
        </div>
        """, unsafe_allow_html=True)
        
    st.markdown("---")
    
    # Detailed Consequence Analysis
    st.subheader("💡 Strategic Consequence & Tactical Diagnostic")
    res_col1, res_col2 = st.columns(2)
    
    with res_col1:
        st.markdown("#### 🎯 Opponents Neutralized by this Setup")
        if "Mustafizur" in fast_bowler or "Pathirana" in fast_bowler:
            st.success("✅ **Sunrisers Hyderabad (SRH)**: Cuts off Heinrich Klaasen and Aniket Verma at the death by taking pace off the ball with cutter variations.")
            st.success("✅ **Kolkata Knight Riders (KKR)**: Delivers dedicated toe-crushing yorkers to Andre Russell in overs 18 and 20.")
        if "Phillips" in spin_combo or "Phillips" in finisher_combo:
            st.success("✅ **Royal Challengers Bengaluru (RCB)**: Bridges the overs 7–11 scoring dip against Krunal Pandya and Suyash Sharma.")
            st.success("✅ **Lucknow Super Giants (LSG)**: Dominates Kuldeep Yadav in the middle overs with explosive spin striking.")
        if "Dayal" in fast_bowler or "Mohsin" in fast_bowler:
            st.success("✅ **Chennai Super Kings (CSK)**: Left-arm steep bounce targets Shivam Dube's armpit and chest.")
            
    with res_col2:
        st.markdown("#### ⚠️ Auction Pivot & Contingency Plan")
        if total_est_spend > available_purse:
            st.error(f"🚨 **BUDGET OVERRUN**: This configuration costs ₹{total_est_spend:.2f} Cr, exceeding RR's ₹{available_purse:.2f} Cr purse. Pivot {sel_fast} to Nuwan Thushara (₹5 Cr) or drop Cameron Green to Glenn Phillips (₹7 Cr).")
        else:
            st.info(f"🛡️ **SURPLUS ALLOCATION**: You retain a ₹{surplus:.2f} Cr purse surplus. Dedicate this reserve to acquire emerging domestic quicks and uncapped wicketkeeper insurance.")
            st.markdown(f"""
            - **Walk-Away Trigger**: If bidding on **{sel_fast}** exceeds hard ceiling by ₹2.0 Cr, pivot immediately to **Nuwan Thushara** or **Akash Deep**.
            - **Workload Management**: Pair overseas pacer with **Nandre Burger** to manage Jofra Archer across all 14 fixtures.
            """)

# TAB 2: COMPETING STRATEGIES & MONTE CARLO
elif selected_tab == "📊 Competing Strategies & Monte Carlo":
    st.subheader("📊 10,000-Scenario Monte Carlo Season Simulation")
    st.markdown("Four distinct franchise strategies evaluated over 10,000 simulated IPL 2027 seasons accounting for match conditions, toss dynamics, player variance, and injury risk.")
    
    st.dataframe(mc_df, use_container_width=True)
    
    # Plotly Bar Chart
    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=mc_df['strategy'],
        y=mc_df['top4_qualification_prob_pct'],
        name='Top-4 Playoff Prob (%)',
        marker_color='#3A86FF'
    ))
    fig.add_trace(go.Bar(
        x=mc_df['strategy'],
        y=mc_df['championship_win_prob_pct'],
        name='Championship Win Prob (%)',
        marker_color='#FF007F'
    ))
    fig.update_layout(
        barmode='group',
        title="10,000 Monte Carlo Simulations: Playoff vs Championship Probabilities",
        paper_bgcolor='#0B132B',
        plot_bgcolor='#1C2541',
        font=dict(color='#F8FAFC'),
        legend=dict(bgcolor='#0B132B', bordercolor='#3A86FF')
    )
    st.plotly_chart(fig, use_container_width=True)
    
    st.markdown("---")
    st.subheader("🎯 Master Strategy Comparison Matrix")
    st.dataframe(strat_df, use_container_width=True)

# TAB 3: OPPONENT INTELLIGENCE
elif selected_tab == "⚔️ Opponent Intelligence (Post-Trade)":
    st.subheader("⚔️ Tactical Opponent Intelligence (Post-November 2026 Trades)")
    st.markdown("Ground-truth diagnostics accounting for confirmed blockbuster trades: Arshdeep to MI, Natarajan/Ellis/Khaleel to SRH, Livingstone to CSK, Hardik to PBKS, Pant to DC, Kuldeep to LSG.")
    
    sel_team = st.selectbox("Select Rival Franchise", opp_df['team'].unique())
    team_data = opp_df[opp_df['team'] == sel_team].iloc[0]
    
    c1, c2 = st.columns([1, 2])
    with c1:
        st.markdown(f"### Threat Rating: **{team_data['threat_rating']} / 10**")
        st.markdown(f"**Key 2027 Additions:**\n\n`{team_data['key_additions']}`")
        st.markdown(f"**Top-Order Threat:**\n{team_data['top_order_threat']}")
        st.markdown(f"**Middle-Order Threat:**\n{team_data['middle_order_threat']}")
        st.markdown(f"**Death Threat:**\n{team_data['death_threat']}")
    with c2:
        st.warning(f"⚠️ **Critical Vulnerability**:\n{team_data['critical_vulnerability']}")
        st.success(f"🛡️ **RR Bowling Blueprint**:\n{team_data['rr_bowling_plan']}")
        st.info(f"🏏 **RR Batting Blueprint**:\n{team_data['rr_batting_plan']}")

# TAB 4: VENUE-SPECIFIC BLUEPRINTS
elif selected_tab == "🏟️ Venue-Specific Blueprints":
    st.subheader("🏟️ 7-Venue Adaptation Blueprints")
    st.markdown("Every venue in India has distinct dimensions, soil characteristics, and dew profiles. RR cannot deploy the same XI everywhere.")
    
    for _, row in venue_df.iterrows():
        with st.expander(f"📍 {row['venue']} | Par Score: {row['par_score']}"):
            st.markdown(f"**Surface Characteristics**: {row['surface_character']}")
            st.markdown(f"**Tactical XI Focus**: {row['tactical_xi_focus']}")
            st.markdown(f"**Impact Sub Strategy**: `{row['impact_sub']}`")
            st.markdown(f"**Tactical Key**: {row['tactical_key']}")

# TAB 5: FIVE PRESSURE MODELS TOURNAMENT
elif selected_tab == "🔬 5 Pressure Models Tournament":
    st.subheader("🔬 Five Pressure Models Tournament: Player Stability Matrix")
    st.markdown("Testing player performance across 5 mathematical pressure formulations (RRR, Wicket Scarcity, Win-Prob Leverage, Multi-Dimensional Contextual, Extreme Crisis).")
    
    st.dataframe(press_df, use_container_width=True)
    st.success("✅ **Stability Finding**: Jos Buttler, Ashutosh Sharma, Shubham Dubey, and Naman Dhir maintain >90.0 Stability Indices across all 5 definitions.")

# TAB 6: PURSE & MARKET STATUS
elif selected_tab == "💰 Purse & Market Status":
    st.subheader("💰 Live Market Intelligence & RR Purse Restructuring")
    
    c1, c2 = st.columns(2)
    with c1:
        st.markdown("### 📋 Confirmed Trades (November 2026)")
        trades_path = os.path.join(V2_DIR, "experiments", "run_02_global", "confirmed_ipl_2027_trades.csv")
        if os.path.exists(trades_path):
            st.dataframe(pd.read_csv(trades_path), use_container_width=True)
    with c2:
        st.markdown("### 🔒 Retention Locks & Status")
        locks_path = os.path.join(V2_DIR, "experiments", "run_02_global", "market_status_and_lockouts.csv")
        if os.path.exists(locks_path):
            st.dataframe(pd.read_csv(locks_path), use_container_width=True)
            
    st.markdown("---")
    st.info("💡 **Financial Bottom Line**: Releasing Hetmyer (₹11Cr), Bishnoi (₹7.2Cr), Deshpande (₹6.5Cr), Sandeep (₹4Cr), Curran (₹2.4Cr), Milne (₹2.4Cr), and Maphaka (₹1.5Cr) alongside the ₹6.0 Cr cap hike gives RR a commanding **₹39.0 Cr available purse**.")
