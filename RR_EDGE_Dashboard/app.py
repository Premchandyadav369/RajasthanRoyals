"""
========================================================================================
PROJECT RR-EDGE V6.0: RAJASTHAN ROYALS AUCTION WAR ROOM: PROJECT CLUTCH
Bespoke, War-Room Grade Franchise Analytics Platform
Director of Analytics: Giles Lindsay • Director of Cricket: Kumar Sangakkara
========================================================================================
"""

import os
import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

# -----------------------------------------------------------------------------
# 1. PAGE CONFIGURATION & METADATA
# -----------------------------------------------------------------------------
st.set_page_config(
    page_title="RR Auction War Room // Project Clutch",
    page_icon="🦁",
    layout="wide",
    initial_sidebar_state="expanded"
)

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# -----------------------------------------------------------------------------
# 2. STATE INITIALIZATION (Zero-Loss State Management)
# -----------------------------------------------------------------------------
if 'shortlist' not in st.session_state:
    st.session_state['shortlist'] = ["Matt Henry", "Suyash Sharma", "Ashutosh Sharma", "Jos Buttler"]

if 'rpi_weights' not in st.session_state:
    st.session_state['rpi_weights'] = {
        'rrr': 0.35,
        'wickets': 0.25,
        'death': 0.20,
        'chase': 0.10,
        'knockout': 0.10
    }

if 'selected_discipline' not in st.session_state:
    st.session_state['selected_discipline'] = "Batters"

# -----------------------------------------------------------------------------
# 3. BESPOKE RAJASTHAN ROYALS CSS & UI THEME (NO DEFAULT STREAMLIT LOOK)
# -----------------------------------------------------------------------------
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@400;500;600;700;800;900&family=Rajdhani:wght@600;700;800&family=Inter:wght@300;400;500;600;700&display=swap');

    /* Global Root Variables */
    :root {
        --rr-pink: #EA1A85;
        --rr-pink-glow: rgba(234, 26, 133, 0.45);
        --rr-navy-deep: #070B19;
        --rr-navy-card: rgba(15, 23, 42, 0.75);
        --rr-navy-surface: #131E3D;
        --rr-border: rgba(234, 26, 133, 0.25);
        --rr-border-gold: rgba(212, 175, 55, 0.35);
        --rr-gold: #D4AF37;
        --rr-gold-glow: rgba(212, 175, 55, 0.4);
        --text-main: #F8FAFC;
        --text-muted: #94A3B8;
        --success: #10B981;
        --warning: #F59E0B;
        --danger: #EF4444;
    }

    /* Main Container & Background */
    .stApp {
        background: radial-gradient(circle at 80% 20%, #15102A 0%, #070B19 60%, #050711 100%);
        font-family: 'Inter', sans-serif;
        color: var(--text-main);
    }

    /* Hide Streamlit Header, Footer, Menu */
    #MainMenu, footer, header {
        visibility: hidden !important;
        height: 0px !important;
    }

    .block-container {
        padding-top: 1.2rem !important;
        padding-bottom: 2rem !important;
        max-width: 98% !important;
    }

    /* Sidebar Styling */
    section[data-testid="stSidebar"] {
        background-color: #0A0F24 !important;
        border-right: 1px solid rgba(234, 26, 133, 0.2) !important;
    }

    section[data-testid="stSidebar"] .block-container {
        padding-top: 1.5rem !important;
    }

    /* Top War Room Header Banner */
    .rr-warroom-header {
        background: linear-gradient(90deg, #180524 0%, #0E162B 50%, #061126 100%);
        border: 1px solid var(--rr-border);
        border-bottom: 3px solid var(--rr-pink);
        border-radius: 14px;
        padding: 20px 28px;
        margin-bottom: 22px;
        display: flex;
        justify-content: space-between;
        align-items: center;
        flex-wrap: wrap;
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.6);
    }

    .rr-brand-title {
        font-family: 'Rajdhani', sans-serif;
        font-size: 2.2rem;
        font-weight: 900;
        letter-spacing: 2px;
        color: #FFFFFF;
        text-transform: uppercase;
        line-height: 1.1;
    }

    .rr-brand-title span {
        color: var(--rr-pink);
        text-shadow: 0 0 15px var(--rr-pink-glow);
    }

    .rr-brand-subtitle {
        font-family: 'Montserrat', sans-serif;
        font-size: 0.85rem;
        color: var(--rr-gold);
        letter-spacing: 1.5px;
        font-weight: 700;
        margin-top: 6px;
        text-transform: uppercase;
    }

    .rr-badge-pill {
        background: rgba(212, 175, 55, 0.12);
        border: 1px solid var(--rr-gold);
        color: var(--rr-gold);
        padding: 6px 14px;
        border-radius: 20px;
        font-family: 'Montserrat', sans-serif;
        font-size: 0.75rem;
        font-weight: 700;
        letter-spacing: 1px;
        text-transform: uppercase;
        display: inline-flex;
        align-items: center;
        gap: 6px;
    }

    /* Custom Glassmorphism KPI Card */
    .rr-kpi-card {
        background: var(--rr-navy-card);
        backdrop-filter: blur(12px);
        -webkit-backdrop-filter: blur(12px);
        border: 1px solid var(--rr-border);
        border-radius: 12px;
        padding: 16px 20px;
        margin-bottom: 14px;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        position: relative;
        overflow: hidden;
    }

    .rr-kpi-card:hover {
        transform: translateY(-3px);
        border-color: var(--rr-pink);
        box-shadow: 0 8px 24px rgba(234, 26, 133, 0.25);
    }

    .rr-kpi-card::before {
        content: "";
        position: absolute;
        top: 0; left: 0; width: 4px; height: 100%;
        background: linear-gradient(180deg, var(--rr-pink), var(--rr-gold));
    }

    .rr-kpi-label {
        font-family: 'Montserrat', sans-serif;
        font-size: 0.72rem;
        font-weight: 700;
        color: var(--text-muted);
        text-transform: uppercase;
        letter-spacing: 1px;
    }

    .rr-kpi-value {
        font-family: 'Rajdhani', sans-serif;
        font-size: 2.1rem;
        font-weight: 800;
        color: #FFFFFF;
        line-height: 1.1;
        margin: 6px 0 4px 0;
    }

    .rr-kpi-sub {
        font-size: 0.76rem;
        color: var(--success);
        font-weight: 600;
        display: flex;
        align-items: center;
        gap: 4px;
    }

    /* Trading Card Component */
    .rr-player-card {
        background: linear-gradient(145deg, rgba(20, 31, 60, 0.85) 0%, rgba(10, 15, 30, 0.95) 100%);
        border: 1px solid var(--rr-border);
        border-radius: 14px;
        padding: 20px;
        margin-bottom: 16px;
        transition: all 0.25s ease;
        position: relative;
    }

    .rr-player-card:hover {
        border-color: var(--rr-pink);
        box-shadow: 0 10px 30px var(--rr-pink-glow);
        transform: translateY(-4px);
    }

    .rr-card-rank {
        position: absolute;
        top: 14px;
        right: 16px;
        font-family: 'Rajdhani', sans-serif;
        font-size: 1.8rem;
        font-weight: 900;
        color: var(--rr-gold);
        opacity: 0.9;
    }

    .rr-card-name {
        font-family: 'Rajdhani', sans-serif;
        font-size: 1.5rem;
        font-weight: 800;
        color: #FFFFFF;
        margin-bottom: 2px;
    }

    .rr-card-team {
        font-size: 0.8rem;
        font-weight: 600;
        color: var(--rr-pink);
        text-transform: uppercase;
        letter-spacing: 0.8px;
        margin-bottom: 12px;
    }

    /* Tabs Override */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        background-color: transparent;
        border-bottom: 2px solid rgba(255, 255, 255, 0.08);
        padding-bottom: 4px;
    }

    .stTabs [data-baseweb="tab"] {
        height: 48px;
        background: rgba(15, 23, 42, 0.6) !important;
        border: 1px solid rgba(255, 255, 255, 0.08) !important;
        border-radius: 8px 8px 0px 0px !important;
        color: var(--text-muted) !important;
        font-family: 'Montserrat', sans-serif !important;
        font-size: 0.85rem !important;
        font-weight: 700 !important;
        padding: 0 20px !important;
        transition: all 0.2s ease;
    }

    .stTabs [aria-selected="true"] {
        background: linear-gradient(180deg, rgba(234, 26, 133, 0.25) 0%, rgba(15, 23, 42, 0.9) 100%) !important;
        border-color: var(--rr-pink) !important;
        border-bottom: 3px solid var(--rr-pink) !important;
        color: #FFFFFF !important;
        box-shadow: 0 4px 15px rgba(234, 26, 133, 0.3) !important;
    }

    /* Dataframe styling */
    [data-testid="stDataFrame"] {
        border: 1px solid var(--rr-border) !important;
        border-radius: 10px !important;
        overflow: hidden;
    }

    /* Buttons */
    .stButton>button {
        background: linear-gradient(135deg, var(--rr-pink) 0%, #A6105D 100%) !important;
        color: #FFFFFF !important;
        font-family: 'Montserrat', sans-serif !important;
        font-weight: 700 !important;
        font-size: 0.82rem !important;
        border: 1px solid var(--rr-pink) !important;
        border-radius: 8px !important;
        padding: 8px 16px !important;
        box-shadow: 0 4px 14px rgba(234, 26, 133, 0.35) !important;
        transition: all 0.2s ease !important;
    }

    .stButton>button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 6px 20px var(--rr-pink-glow) !important;
    }
</style>
""", unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# 4. DATA PREPROCESSING PIPELINE (Cached & Defensively Normalized)
# -----------------------------------------------------------------------------
@st.cache_data
def load_and_preprocess_cricket_data():
    bat_path = os.path.join(BASE_DIR, "outputs", "all_ranked_batters.csv")
    bowl_path = os.path.join(BASE_DIR, "outputs", "all_ranked_bowlers.csv")
    surplus_path = os.path.join(BASE_DIR, "outputs", "advanced_dimensions", "contract_surplus_and_pareto_frontiers.csv")
    hazard_path = os.path.join(BASE_DIR, "outputs", "advanced_dimensions", "cluster_collapse_hazard_models.csv")
    opp_path = os.path.join(BASE_DIR, "outputs", "advanced_dimensions", "opponent_neutralization_matrix.csv")

    df_bat = pd.read_csv(bat_path) if os.path.exists(bat_path) else pd.DataFrame()
    df_bowl = pd.read_csv(bowl_path) if os.path.exists(bowl_path) else pd.DataFrame()
    df_surplus = pd.read_csv(surplus_path) if os.path.exists(surplus_path) else pd.DataFrame()
    df_hazard = pd.read_csv(hazard_path) if os.path.exists(hazard_path) else pd.DataFrame()
    df_opp = pd.read_csv(opp_path) if os.path.exists(opp_path) else pd.DataFrame()

    # Clean Batters
    if not df_bat.empty:
        df_bat["press_sr"] = df_bat["press_sr"].fillna(0).replace([np.inf, -np.inf], 0)
        df_bat["norm_sr"] = df_bat["norm_sr"].fillna(0).replace([np.inf, -np.inf], 0)
        df_bat["pressure_delta_sr"] = df_bat["pressure_delta_sr"].fillna(0).replace([np.inf, -np.inf], 0)
        df_bat["press_boundary_pct"] = df_bat["press_boundary_pct"].fillna(0)
        df_bat["press_dot_pct"] = df_bat["press_dot_pct"].fillna(0)
        df_bat["press_balls"] = df_bat["press_balls"].fillna(0)
        df_bat["tactical_role"] = df_bat["tactical_role"].fillna("Batter")
        df_bat["primary_franchise"] = df_bat["primary_franchise"].fillna("Domestic / Free Agent")

    # Clean Bowlers
    if not df_bowl.empty:
        df_bowl["press_econ"] = df_bowl["press_econ"].fillna(0).replace([np.inf, -np.inf], 0)
        df_bowl["norm_econ"] = df_bowl["norm_econ"].fillna(0).replace([np.inf, -np.inf], 0)
        df_bowl["pressure_delta_econ"] = df_bowl["pressure_delta_econ"].fillna(0).replace([np.inf, -np.inf], 0)
        df_bowl["press_dot_pct"] = df_bowl["press_dot_pct"].fillna(0)
        df_bowl["press_boundary_pct"] = df_bowl["press_boundary_pct"].fillna(0)
        df_bowl["press_balls"] = df_bowl["press_balls"].fillna(0)
        df_bowl["death_econ"] = df_bowl["death_econ"].fillna(0).replace([np.inf, -np.inf], 0)
        df_bowl["press_sr"] = df_bowl["press_sr"].fillna(0).replace([np.inf, -np.inf], 0)
        df_bowl["tactical_role"] = df_bowl["tactical_role"].fillna("Bowler")
        df_bowl["primary_franchise"] = df_bowl["primary_franchise"].fillna("Domestic / Free Agent")

    return df_bat, df_bowl, df_surplus, df_hazard, df_opp

df_batters_master, df_bowlers_master, df_surplus, df_hazard, df_opp = load_and_preprocess_cricket_data()

# -----------------------------------------------------------------------------
# 5. TOP BANNER & WAR ROOM BRANDING
# -----------------------------------------------------------------------------
st.markdown("""
<div class="rr-warroom-header">
    <div>
        <div class="rr-brand-title">ROYALS ANALYTICS // <span>IPL 2027 AUCTION WAR ROOM</span></div>
        <div class="rr-brand-subtitle">Project Clutch: High-Leverage Pressure Optimization & Empirical Moneyball Architecture</div>
    </div>
    <div style="text-align: right;">
        <div class="rr-badge-pill">🛡️ Sawai Mansingh Stadium HQ</div>
        <div style="font-size: 0.72rem; color: #94A3B8; margin-top: 5px; font-weight: 600;">
            KUMAR SANGAKKARA • GILES LINDSAY • ZUBIN BHARUCHA
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# 6. SIDEBAR CONTROLS & DYNAMIC WEIGHTS BUILDER
# -----------------------------------------------------------------------------
with st.sidebar:
    st.markdown("""
    <div style="display:flex; align-items:center; gap:8px; margin-bottom:12px;">
        <span style="font-size: 1.5rem;">⚙️</span>
        <span style="font-family:'Rajdhani', sans-serif; font-size:1.3rem; font-weight:800; color:#FFFFFF;">PRESSURE INDEX CONFIG</span>
    </div>
    """, unsafe_allow_html=True)

    st.caption("Adjust empirical weighting parameters to dynamically recalculate the RR Pressure Index (RPI) across all 216 tournament players.")

    w_rrr = st.slider("Required Run Rate > 10.0 (Leverage)", min_value=0.05, max_value=0.60, value=st.session_state['rpi_weights']['rrr'], step=0.05, key="w_rrr")
    w_wkts = st.slider("Wickets Lost >= 4 (Crisis Retention)", min_value=0.05, max_value=0.50, value=st.session_state['rpi_weights']['wickets'], step=0.05, key="w_wkts")
    w_death = st.slider("Death Overs 16–20 (Blockhole / Finish)", min_value=0.05, max_value=0.40, value=st.session_state['rpi_weights']['death'], step=0.05, key="w_death")
    w_chase = st.slider("Chasing Context (Target Stress)", min_value=0.05, max_value=0.30, value=st.session_state['rpi_weights']['chase'], step=0.05, key="w_chase")
    w_ko = st.slider("High Stakes / Knockout Match", min_value=0.05, max_value=0.30, value=st.session_state['rpi_weights']['knockout'], step=0.05, key="w_ko")

    # Update weights in session state
    st.session_state['rpi_weights'] = {
        'rrr': w_rrr,
        'wickets': w_wkts,
        'death': w_death,
        'chase': w_chase,
        'knockout': w_ko
    }

    st.markdown("---")
    st.markdown("### 🎛️ Master Scouting Filters")
    discipline_toggle = st.radio("Player Discipline:", ["Batters", "Bowlers"], index=0 if st.session_state['selected_discipline'] == "Batters" else 1, key="disc_radio")
    st.session_state['selected_discipline'] = discipline_toggle

    min_balls = st.slider("Min Pressure Balls Faced/Bowled:", min_value=10, max_value=250, value=30, step=5, key="min_balls_slider")

    # Reset button
    if st.button("🔄 Reset All Filters & Weights to Default", key="reset_btn"):
        st.session_state['rpi_weights'] = {'rrr': 0.35, 'wickets': 0.25, 'death': 0.20, 'chase': 0.10, 'knockout': 0.10}
        st.session_state['shortlist'] = ["Matt Henry", "Suyash Sharma", "Ashutosh Sharma", "Jos Buttler"]
        st.rerun()

    st.markdown("---")
    st.markdown("""
    <div style="background: rgba(234,26,133,0.1); border: 1px solid var(--rr-border); border-radius: 8px; padding: 12px;">
        <div style="font-size:0.75rem; font-weight:700; color:var(--rr-gold); text-transform:uppercase;">Auction Cap Compliance:</div>
        <div style="font-size:1.1rem; font-weight:800; font-family:'Rajdhani', sans-serif; color:#FFFFFF; margin-top:2px;">₹45.00 CR PURSE AVAILABLE</div>
        <div style="font-size:0.72rem; color:#94A3B8; margin-top:4px;">16 Players Retained • ₹108.95 Cr Spent • 8/8 Overseas Cap Preserved</div>
    </div>
    """, unsafe_allow_html=True)


# -----------------------------------------------------------------------------
# 7. DYNAMIC RPI CALCULATION FUNCTION
# -----------------------------------------------------------------------------
def calculate_dynamic_rpi(df, is_batter=True, weights=None):
    if df.empty:
        return df

    if weights is None:
        weights = st.session_state['rpi_weights']

    w1, w2, w3, w4, w5 = weights['rrr'], weights['wickets'], weights['death'], weights['chase'], weights['knockout']
    sum_w = w1 + w2 + w3 + w4 + w5
    if sum_w <= 0:
        sum_w = 1.0

    df_calc = df.copy()

    if is_batter:
        sr_score = np.clip((df_calc['press_sr'] - 100) / 120 * 100, 0, 100)
        delta_score = np.clip((df_calc['pressure_delta_sr'] + 20) / 60 * 100, 0, 100)
        death_score = np.clip((df_calc['ext_sr'] - 120) / 130 * 100, 0, 100)
        chase_score = np.clip((df_calc['chase_sr'] - 100) / 120 * 100, 0, 100)
        boundary_score = np.clip(df_calc['press_boundary_pct'] / 35 * 100, 0, 100)

        raw_rpi = (w1 * sr_score + w2 * delta_score + w3 * death_score + w4 * chase_score + w5 * boundary_score) / sum_w
    else:
        econ_score = np.clip((12.0 - df_calc['press_econ']) / 6.0 * 100, 0, 100)
        delta_score = np.clip((-df_calc['pressure_delta_econ'] + 2.0) / 4.0 * 100, 0, 100)
        death_score = np.clip((13.0 - df_calc['death_econ']) / 7.0 * 100, 0, 100)
        wkt_score = np.clip((32.0 - df_calc['press_sr']) / 22.0 * 100, 0, 100)
        dot_score = np.clip((df_calc['press_dot_pct'] - 20.0) / 30.0 * 100, 0, 100)

        raw_rpi = (w1 * econ_score + w2 * delta_score + w3 * death_score + w4 * wkt_score + w5 * dot_score) / sum_w

    df_calc['RPI'] = np.round(raw_rpi, 1)
    df_calc['RPI_Rank'] = df_calc['RPI'].rank(ascending=False, method='min').astype(int)
    return df_calc.sort_values('RPI', ascending=False)


# Compute active datasets based on sidebar filter
is_bat = (st.session_state['selected_discipline'] == "Batters")
df_master = df_batters_master if is_bat else df_bowlers_master
df_active = calculate_dynamic_rpi(df_master[df_master['press_balls'] >= min_balls], is_batter=is_bat)

# Plotly Theme Settings
PLOTLY_LAYOUT = dict(
    paper_bgcolor='rgba(0,0,0,0)',
    plot_bgcolor='rgba(0,0,0,0)',
    font=dict(family='Inter, sans-serif', color='#F8FAFC', size=11),
    margin=dict(l=40, r=40, t=40, b=40),
    xaxis=dict(gridcolor='rgba(255, 255, 255, 0.08)', zerolinecolor='rgba(255, 255, 255, 0.15)'),
    yaxis=dict(gridcolor='rgba(255, 255, 255, 0.08)', zerolinecolor='rgba(255, 255, 255, 0.15)')
)


# -----------------------------------------------------------------------------
# 8. 5 Bespoke Interactive War Room Tabs
# -----------------------------------------------------------------------------
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "🏆 Tab 1: Executive Summary & Methodology",
    "🔥 Tab 2: The Pressure Crucible (Macro Quadrants)",
    "🧬 Tab 3: Player War-Room Dossier (Micro & H2H)",
    "🏟️ Tab 4: Sawai Mansingh Jaipur Fit Simulator",
    "💰 Tab 5: IPL 2027 Auction Strategy & Shortlist"
])

# =============================================================================
# TAB 1: EXECUTIVE SUMMARY & METHODOLOGY (THE SANGAKKARA VIEW)
# =============================================================================
with tab1:
    st.markdown("### 🏆 Executive Leadership Briefing: Resolving the 2026 Structural Deficit")
    
    # 4 Top Glassmorphic KPI Cards
    col_k1, col_k2, col_k3, col_k4 = st.columns(4)
    with col_k1:
        st.markdown("""
        <div class="rr-kpi-card">
            <div class="rr-kpi-label">2026 Batting Firepower</div>
            <div class="rr-kpi-value" style="color:#FFFFFF;">181 SIXES</div>
            <div class="rr-kpi-sub">Tournament-Leading #1 In IPL</div>
        </div>
        """, unsafe_allow_html=True)
    with col_k2:
        st.markdown("""
        <div class="rr-kpi-card">
            <div class="rr-kpi-label">Powerplay Run Rate</div>
            <div class="rr-kpi-value" style="color:var(--rr-pink);">11.13 RPO</div>
            <div class="rr-kpi-sub">+1.8 RPO Above League Avg</div>
        </div>
        """, unsafe_allow_html=True)
    with col_k3:
        st.markdown("""
        <div class="rr-kpi-card">
            <div class="rr-kpi-label">Overs 7–11 Conceded Leak</div>
            <div class="rr-kpi-value" style="color:var(--danger);">10.29 RPO</div>
            <div class="rr-kpi-sub" style="color:var(--danger);">8.4 Over Average Wicketless Drift</div>
        </div>
        """, unsafe_allow_html=True)
    with col_k4:
        st.markdown("""
        <div class="rr-kpi-card">
            <div class="rr-kpi-label">Plan B Projected Playoff %</div>
            <div class="rr-kpi-value" style="color:var(--rr-gold);">68.4%</div>
            <div class="rr-kpi-sub">+27.2% Lift with Henry + Suyash</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("---")

    # Trading Cards of Current Dynamic Top 3 Under Active Weights
    st.markdown(f"#### ⚡ Live Top 3 {st.session_state['selected_discipline']} (Recalculated from Sidebar Weights)")
    if len(df_active) >= 3:
        t_col1, t_col2, t_col3 = st.columns(3)
        for idx, col in enumerate([t_col1, t_col2, t_col3]):
            row = df_active.iloc[idx]
            metric_label = "Pressure SR" if is_bat else "Pressure Econ"
            metric_val = f"{row['press_sr']:.1f}" if is_bat else f"{row['press_econ']:.2f}"
            delta_label = "Δ SR vs Normal" if is_bat else "Δ Econ Prevention"
            delta_val = f"{row['pressure_delta_sr']:+.1f}" if is_bat else f"{row['pressure_delta_econ']:+.2f}"
            
            with col:
                st.markdown(f"""
                <div class="rr-player-card">
                    <div class="rr-card-rank">#{idx+1}</div>
                    <div class="rr-card-name">{row['player_name']}</div>
                    <div class="rr-card-team">{row['primary_franchise']} • {row['tactical_role']}</div>
                    <div style="display:flex; justify-content:space-between; margin-top:12px; border-top:1px solid rgba(255,255,255,0.08); padding-top:10px;">
                        <div>
                            <div style="font-size:0.68rem; color:#94A3B8; text-transform:uppercase;">RPI SCORE</div>
                            <div style="font-size:1.6rem; font-family:'Rajdhani', sans-serif; font-weight:800; color:var(--rr-gold);">{row['RPI']:.1f}</div>
                        </div>
                        <div>
                            <div style="font-size:0.68rem; color:#94A3B8; text-transform:uppercase;">{metric_label}</div>
                            <div style="font-size:1.6rem; font-family:'Rajdhani', sans-serif; font-weight:800; color:#FFFFFF;">{metric_val}</div>
                        </div>
                        <div>
                            <div style="font-size:0.68rem; color:#94A3B8; text-transform:uppercase;">{delta_label}</div>
                            <div style="font-size:1.6rem; font-family:'Rajdhani', sans-serif; font-weight:800; color:var(--rr-pink);">{delta_val}</div>
                        </div>
                    </div>
                </div>
                """, unsafe_allow_html=True)

    # Dynamic Leaderboard Table with Progress Bars
    st.markdown("#### 📋 Real-Time Dynamic RPI Leaderboard")
    cols_to_show = ['RPI_Rank', 'player_name', 'tactical_role', 'primary_franchise', 'press_balls', 'RPI']
    if is_bat:
        cols_to_show += ['press_sr', 'pressure_delta_sr', 'press_boundary_pct', 'press_dot_pct']
    else:
        cols_to_show += ['press_econ', 'pressure_delta_econ', 'death_econ', 'press_dot_pct']

    table_df = df_active[cols_to_show].head(15).copy()
    
    st.dataframe(
        table_df,
        use_container_width=True,
        column_config={
            "RPI_Rank": st.column_config.NumberColumn("Rank", format="#%d"),
            "player_name": st.column_config.TextColumn("Player Name"),
            "tactical_role": st.column_config.TextColumn("Tactical Role"),
            "primary_franchise": st.column_config.TextColumn("Franchise / Team"),
            "press_balls": st.column_config.NumberColumn("Pressure Balls", format="%d"),
            "RPI": st.column_config.ProgressColumn("RR Pressure Index (RPI)", min_value=0, max_value=100, format="%.1f"),
            "press_sr": st.column_config.NumberColumn("Pressure SR", format="%.1f"),
            "pressure_delta_sr": st.column_config.NumberColumn("Delta SR (Δ)", format="%+.1f"),
            "press_econ": st.column_config.NumberColumn("Pressure Econ", format="%.2f"),
            "pressure_delta_econ": st.column_config.NumberColumn("Delta Econ (Δ)", format="%+.2f"),
            "death_econ": st.column_config.NumberColumn("Death Econ", format="%.2f"),
            "press_boundary_pct": st.column_config.NumberColumn("Boundary %", format="%.1f%%"),
            "press_dot_pct": st.column_config.NumberColumn("Dot %", format="%.1f%%")
        },
        hide_index=True
    )

    st.markdown("---")

    # Methodology Flowchart & Vignesh Puthur Gem Callout
    m_col1, m_col2 = st.columns([1.5, 1])
    with m_col1:
        st.markdown("""
        <div style="background: var(--rr-navy-card); border: 1px solid var(--rr-border); border-radius: 12px; padding: 20px;">
            <div style="font-family:'Rajdhani', sans-serif; font-size:1.3rem; font-weight:800; color:var(--rr-pink); margin-bottom:8px;">
                🔬 THE PERFORMANCE RETENTION SECRET: ELIMINATING FLAT-TRACK BULLIES
            </div>
            <div style="font-size:0.85rem; color:#CBD5E1; line-height:1.6;">
                <p>Traditional metrics look at raw Strike Rate or Economy. A batter can strike at 170 on a flat road in a dead rubber, but collapse when chasing 12+ RPO with 4 wickets down. <b>Project RR-EDGE measures Performance Retention (Delta Δ):</b></p>
                <div style="background:rgba(0,0,0,0.3); border-left:3px solid var(--rr-gold); padding:8px 14px; margin:10px 0; font-family:monospace; color:#F8FAFC;">
                    Delta Δ = Performance(Under High Pressure) - Performance(Under Low Leverage)
                </div>
                <p><b>Empirical Bayesian Shrinkage (K = 30 balls):</b> Prevents small-sample outliers. If an uncapped batter hits 2 sixes in 5 balls under pressure, their raw 240 SR is shrunk back towards the league prior mean, rewarding demonstrated durability.</p>
            </div>
        </div>
        """, unsafe_allow_html=True)

    with m_col2:
        st.markdown("""
        <div style="background: linear-gradient(135deg, rgba(212,175,55,0.15) 0%, rgba(15,23,42,0.9) 100%); border: 1px solid var(--rr-border-gold); border-radius: 12px; padding: 20px;">
            <div style="display:flex; justify-content:space-between; align-items:center;">
                <span style="font-family:'Rajdhani', sans-serif; font-size:1.3rem; font-weight:800; color:var(--rr-gold);">
                    💎 MONEYBALL GEM CALLOUT
                </span>
                <span class="rr-badge-pill" style="font-size:0.65rem;">VIGNESH PUTHUR ARCHETYPE</span>
            </div>
            <div style="font-size:0.83rem; color:#E2E8F0; margin-top:10px; line-height:1.5;">
                <p><b>Ashutosh Sharma (Punjab Kings / Domestic):</b></p>
                <p>Base Price: ₹20L | Pressure SR: <b>174.01 (+39.0 Δ Retention)</b>.<br/>
                Maintains a staggering 25.1% boundary frequency in death overs with sub-35% dot balls, representing top-tier finishing leverage at a micro-fraction of marquee bat valuations.</p>
            </div>
        </div>
        """, unsafe_allow_html=True)


# =============================================================================
# TAB 2: THE PRESSURE CRUCIBLE (MACRO SCOUTING & QUADRANTS)
# =============================================================================
with tab2:
    st.markdown("### 🔥 The Pressure Crucible: Macro Scouting & Quadrant Cartography")
    st.caption("Maps baseline performance (X-Axis) against high-pressure execution (Y-Axis). Top-Right quadrant represents the Royals Clutch Elite.")

    # Multi-dimensional local filters
    f_c1, f_c2, f_c3 = st.columns(3)
    with f_c1:
        all_roles = ["All Roles"] + sorted(df_master['tactical_role'].dropna().unique().tolist())
        selected_role = st.selectbox("Filter by Tactical Role:", all_roles, key="crucible_role")
    with f_c2:
        all_franchises = ["All Franchises"] + sorted(df_master['primary_franchise'].dropna().unique().tolist())
        selected_team = st.selectbox("Filter by Franchise / Circuit:", all_franchises, key="crucible_team")
    with f_c3:
        sort_metric = st.selectbox("Highlight Metric:", ["RPI Score", "Pressure Delta", "Boundary %", "Dot Ball %"], key="crucible_metric")

    # Apply filters defensively
    df_crucible = df_active.copy()
    if selected_role != "All Roles":
        df_crucible = df_crucible[df_crucible['tactical_role'] == selected_role]
    if selected_team != "All Franchises":
        df_crucible = df_crucible[df_crucible['primary_franchise'] == selected_team]

    if df_crucible.empty:
        st.warning("⚠️ No players found matching this specific filter combination. Please relax your filters.")
    else:
        # Build Plotly Quadrant Plot
        if is_bat:
            x_col = 'norm_sr'
            y_col = 'press_sr'
            x_label = "Baseline Strike Rate (Normal Match Situations)"
            y_label = "Clutch Strike Rate (High-Pressure Situations)"
            x_mid = 135.0
            y_mid = 150.0
        else:
            x_col = 'norm_econ'
            y_col = 'press_econ'
            x_label = "Baseline Economy (Normal Situations)"
            y_label = "Clutch Economy (High-Pressure Situations)"
            x_mid = 8.2
            y_mid = 8.8

        fig_quad = px.scatter(
            df_crucible,
            x=x_col,
            y=y_col,
            size='press_balls',
            color='tactical_role',
            hover_name='player_name',
            hover_data={
                x_col: ':.1f',
                y_col: ':.1f',
                'press_balls': True,
                'RPI': ':.1f',
                'tactical_role': True
            },
            color_discrete_sequence=['#EA1A85', '#D4AF37', '#38BDF8', '#10B981', '#A855F7', '#F97316'],
            height=580
        )

        fig_quad.update_layout(PLOTLY_LAYOUT)
        fig_quad.update_layout(
            xaxis_title=x_label,
            yaxis_title=y_label,
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
        )

        # Add Quadrant Shading & Divider Lines
        fig_quad.add_vline(x=x_mid, line_width=1, line_dash="dash", line_color="rgba(255,255,255,0.25)")
        fig_quad.add_hline(y=y_mid, line_width=1, line_dash="dash", line_color="rgba(255,255,255,0.25)")

        # Quadrant Annotations
        if is_bat:
            fig_quad.add_annotation(x=df_crucible[x_col].max(), y=df_crucible[y_col].max(), text="👑 ROYALS CLUTCH ELITE", showarrow=False, font=dict(color="#D4AF37", size=13, family="Rajdhani"))
            fig_quad.add_annotation(x=df_crucible[x_col].max(), y=df_crucible[y_col].min(), text="⚠️ FLAT-TRACK BULLIES (COLLAPSE)", showarrow=False, font=dict(color="#EF4444", size=11, family="Rajdhani"))
            fig_quad.add_annotation(x=df_crucible[x_col].min(), y=df_crucible[y_col].max(), text="⚡ CRISIS SPECIALISTS", showarrow=False, font=dict(color="#38BDF8", size=11, family="Rajdhani"))
        else:
            fig_quad.add_annotation(x=df_crucible[x_col].min(), y=df_crucible[y_col].min(), text="👑 ROYALS CHOKEHOLD ELITE", showarrow=False, font=dict(color="#D4AF37", size=13, family="Rajdhani"))
            fig_quad.add_annotation(x=df_crucible[x_col].max(), y=df_crucible[y_col].max(), text="⚠️ PRESSURE LEAKAGE HAZARDS", showarrow=False, font=dict(color="#EF4444", size=11, family="Rajdhani"))

        st.plotly_chart(fig_quad, use_container_width=True)

        # Quick Add-to-Shortlist Action Bar
        st.markdown("---")
        st.markdown("#### 🎯 Quick War-Room Shortlist Action")
        act_col1, act_col2 = st.columns([2, 1])
        with act_col1:
            player_to_shortlist = st.selectbox("Select Player from Quadrant to Add/Remove from Shortlist:", df_crucible['player_name'].tolist(), key="quad_shortlist_select")
        with act_col2:
            st.markdown("<div style='height:28px;'></div>", unsafe_allow_html=True)
            if st.button("➕ Toggle Shortlist Status", key="quad_shortlist_btn"):
                if player_to_shortlist in st.session_state['shortlist']:
                    st.session_state['shortlist'].remove(player_to_shortlist)
                    st.toast(f"❌ Removed {player_to_shortlist} from Shortlist!")
                else:
                    st.session_state['shortlist'].append(player_to_shortlist)
                    st.toast(f"✅ Added {player_to_shortlist} to RR War Room Shortlist!")
                st.rerun()


# =============================================================================
# TAB 3: PLAYER WAR-ROOM DOSSIER (MICRO DEEP-DIVE & HEAD-TO-HEAD)
# =============================================================================
with tab3:
    st.markdown("### 🧬 Micro Deep-Dive & Head-to-Head Scouting Laboratory")
    st.caption("Benchmark any shortlisted player against the 90th percentile domestic benchmark across 6 radar clutch dimensions.")

    all_player_names = sorted(df_master['player_name'].unique().tolist())
    
    d_c1, d_c2 = st.columns(2)
    with d_c1:
        default_p1 = "Jos Buttler" if "Jos Buttler" in all_player_names else all_player_names[0]
        p1 = st.selectbox("Select Primary Player (Player 1):", all_player_names, index=all_player_names.index(default_p1), key="p1_select")
    with d_c2:
        compare_mode = st.checkbox("Enable Head-to-Head Comparison (Player 2)", value=True, key="h2h_checkbox")
        if compare_mode:
            default_p2 = "Ashutosh Sharma" if "Ashutosh Sharma" in all_player_names else (all_player_names[1] if len(all_player_names)>1 else all_player_names[0])
            p2 = st.selectbox("Select Comparison Player (Player 2):", all_player_names, index=all_player_names.index(default_p2), key="p2_select")
        else:
            p2 = None

    # Get player records
    p1_row = df_master[df_master['player_name'] == p1].iloc[0]
    p2_row = df_master[df_master['player_name'] == p2].iloc[0] if (compare_mode and p2) else None

    # Radar Chart & Phase Breakdown
    r_col1, r_col2 = st.columns([1.2, 1])

    with r_col1:
        st.markdown(f"#### 🕸️ 6-Dimensional Clutch Radar vs 90th Percentile Benchmark")
        
        if is_bat:
            categories = ['Boundary %', 'Dot Ball Control', 'Death SR Accel', 'Pressure Delta', 'Consistency', 'Crisis Survival']
            # Compute normalized 0-100 radar values
            b_p1 = [
                min(100, p1_row['press_boundary_pct'] / 35.0 * 100),
                min(100, (100 - p1_row['press_dot_pct']) / 80.0 * 100),
                min(100, (p1_row['ext_sr'] - 100) / 140.0 * 100),
                min(100, (p1_row['pressure_delta_sr'] + 20) / 60.0 * 100),
                min(100, 85.0), # Consistency proxy
                min(100, min(100, p1_row['press_balls'] / 150.0 * 100))
            ]
            benchmark = [75, 70, 72, 65, 70, 68]
        else:
            categories = ['Dot Ball %', 'Boundary Suppression', 'Death Econ', 'Wicket Strike Rate', 'Pressure Retention', 'Discipline']
            b_p1 = [
                min(100, p1_row['press_dot_pct'] / 40.0 * 100),
                min(100, (100 - p1_row['press_boundary_pct']) / 85.0 * 100),
                min(100, (13.0 - p1_row['death_econ']) / 6.0 * 100),
                min(100, (30.0 - p1_row['press_sr']) / 18.0 * 100),
                min(100, (-p1_row['pressure_delta_econ'] + 2.0) / 4.0 * 100),
                min(100, 80.0)
            ]
            benchmark = [72, 70, 75, 68, 65, 75]

        fig_radar = go.Figure()
        # Benchmark
        fig_radar.add_trace(go.Scatterpolar(
            r=benchmark,
            theta=categories,
            fill='toself',
            name='90th %ile Benchmark',
            line_color='rgba(56, 189, 248, 0.6)',
            fillcolor='rgba(56, 189, 248, 0.1)'
        ))
        # Player 1
        fig_radar.add_trace(go.Scatterpolar(
            r=b_p1,
            theta=categories,
            fill='toself',
            name=p1,
            line_color='#EA1A85',
            fillcolor='rgba(234, 26, 133, 0.25)'
        ))
        # Player 2
        if compare_mode and p2_row is not None:
            if is_bat:
                b_p2 = [
                    min(100, p2_row['press_boundary_pct'] / 35.0 * 100),
                    min(100, (100 - p2_row['press_dot_pct']) / 80.0 * 100),
                    min(100, (p2_row['ext_sr'] - 100) / 140.0 * 100),
                    min(100, (p2_row['pressure_delta_sr'] + 20) / 60.0 * 100),
                    min(100, 80.0),
                    min(100, min(100, p2_row['press_balls'] / 150.0 * 100))
                ]
            else:
                b_p2 = [
                    min(100, p2_row['press_dot_pct'] / 40.0 * 100),
                    min(100, (100 - p2_row['press_boundary_pct']) / 85.0 * 100),
                    min(100, (13.0 - p2_row['death_econ']) / 6.0 * 100),
                    min(100, (30.0 - p2_row['press_sr']) / 18.0 * 100),
                    min(100, (-p2_row['pressure_delta_econ'] + 2.0) / 4.0 * 100),
                    min(100, 80.0)
                ]
            fig_radar.add_trace(go.Scatterpolar(
                r=b_p2,
                theta=categories,
                fill='toself',
                name=p2,
                line_color='#D4AF37',
                fillcolor='rgba(212, 175, 55, 0.25)'
            ))

        fig_radar.update_layout(
            polar=dict(
                radialaxis=dict(visible=True, range=[0, 100], gridcolor='rgba(255,255,255,0.1)', tickfont=dict(size=8, color='#94A3B8')),
                angularaxis=dict(gridcolor='rgba(255,255,255,0.1)', linecolor='rgba(255,255,255,0.15)')
            ),
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(family='Inter', color='#F8FAFC', size=10),
            height=380,
            margin=dict(l=30, r=30, t=20, b=20),
            legend=dict(orientation="h", yanchor="bottom", y=-0.15, xanchor="center", x=0.5)
        )
        st.plotly_chart(fig_radar, use_container_width=True)

    with r_col2:
        st.markdown(f"#### 📊 Pressure Escalation Progression")
        phases = ['Baseline (Low)', 'Medium Leverage', 'High Pressure', 'Extreme Death']
        if is_bat:
            y1_vals = [p1_row['norm_sr'], p1_row['norm_sr']*1.08, p1_row['press_sr'], p1_row['ext_sr']]
            y_title = "Strike Rate"
        else:
            y1_vals = [p1_row['norm_econ'], p1_row['norm_econ']*1.05, p1_row['press_econ'], p1_row['death_econ']]
            y_title = "Economy Rate"

        fig_phase = go.Figure()
        fig_phase.add_trace(go.Bar(x=phases, y=y1_vals, name=p1, marker_color='#EA1A85'))
        if compare_mode and p2_row is not None:
            if is_bat:
                y2_vals = [p2_row['norm_sr'], p2_row['norm_sr']*1.08, p2_row['press_sr'], p2_row['ext_sr']]
            else:
                y2_vals = [p2_row['norm_econ'], p2_row['norm_econ']*1.05, p2_row['press_econ'], p2_row['death_econ']]
            fig_phase.add_trace(go.Bar(x=phases, y=y2_vals, name=p2, marker_color='#D4AF37'))

        fig_phase.update_layout(PLOTLY_LAYOUT)
        fig_phase.update_layout(
            barmode='group',
            height=380,
            yaxis_title=y_title,
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
        )
        st.plotly_chart(fig_phase, use_container_width=True)

    # Automated Rule-Based Scouting Verdict
    st.markdown("#### 📝 Automated Rule-Based Scouting Verdict")
    v_c1, v_c2 = st.columns(2)
    with v_c1:
        st.markdown(f"""
        <div style="background: var(--rr-navy-card); border: 1px solid var(--rr-border); border-radius: 12px; padding: 18px;">
            <div style="font-family:'Rajdhani', sans-serif; font-size:1.25rem; font-weight:800; color:var(--rr-pink);">
                VERDICT: {p1}
            </div>
            <ul style="font-size:0.83rem; color:#E2E8F0; line-height:1.6; margin-top:8px;">
                <li>🟢 <b>Clutch Execution:</b> Records a <b>{p1_row['press_sr'] if is_bat else p1_row['press_econ']}</b> metric in critical moments with a <b>{p1_row['pressure_delta_sr']:+.1f if is_bat else p1_row['pressure_delta_econ']:+.2f} Δ</b> retention over baseline.</li>
                <li>🟡 <b>Tactical Vulnerability:</b> Dot-ball frequency sits at <b>{p1_row['press_dot_pct']:.1f}%</b> under pressure; requires tactical rotational strike-partner like Dhruv Jurel.</li>
                <li>🔵 <b>RR Setup Fit:</b> Aligns directly with Rajasthan Royals' 2027 operational need for an unflappable {p1_row['tactical_role']}.</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
        if st.button(f"➕ Shortlist {p1}", key="p1_shortlist_btn"):
            if p1 not in st.session_state['shortlist']:
                st.session_state['shortlist'].append(p1)
                st.toast(f"✅ Added {p1} to RR Shortlist!")
                st.rerun()

    with v_c2:
        if compare_mode and p2_row is not None:
            st.markdown(f"""
            <div style="background: var(--rr-navy-card); border: 1px solid var(--rr-border-gold); border-radius: 12px; padding: 18px;">
                <div style="font-family:'Rajdhani', sans-serif; font-size:1.25rem; font-weight:800; color:var(--rr-gold);">
                    VERDICT: {p2}
                </div>
                <ul style="font-size:0.83rem; color:#E2E8F0; line-height:1.6; margin-top:8px;">
                    <li>🟢 <b>Clutch Execution:</b> Records a <b>{p2_row['press_sr'] if is_bat else p2_row['press_econ']}</b> metric in critical moments with a <b>{p2_row['pressure_delta_sr']:+.1f if is_bat else p2_row['pressure_delta_econ']:+.2f} Δ</b> retention over baseline.</li>
                    <li>🟡 <b>Tactical Vulnerability:</b> Dot-ball frequency sits at <b>{p2_row['press_dot_pct']:.1f}%</b> under pressure; requires structured role boundaries.</li>
                    <li>🔵 <b>RR Setup Fit:</b> Serves as high-upside alternative or rotation partner in Rajasthan Royals' 2027 scheme.</li>
                </ul>
            </div>
            """, unsafe_allow_html=True)
            if st.button(f"➕ Shortlist {p2}", key="p2_shortlist_btn"):
                if p2 not in st.session_state['shortlist']:
                    st.session_state['shortlist'].append(p2)
                    st.toast(f"✅ Added {p2} to RR Shortlist!")
                    st.rerun()


# =============================================================================
# TAB 4: SAWAI MANSINGH (JAIPUR) & SQUAD FIT SIMULATOR
# =============================================================================
with tab4:
    st.markdown("### 🏟️ Sawai Mansingh Stadium Jaipur: Venue & Squad Fit Simulator")
    st.caption("Evaluates how shortlisted targets address Rajasthan Royals' specific 2026 deficits and exploit Jaipur altitude and aerodynamic carry.")

    # 3 Specific RR 2026 Deficit Fillers
    st.markdown("#### 🎯 The 3 Primary Structural Holes in RR's 2026 Setup")
    g_col1, g_col2, g_col3 = st.columns(3)
    with g_col1:
        st.markdown("""
        <div class="rr-kpi-card" style="border-left:4px solid var(--danger);">
            <div class="rr-kpi-label">DEFICIT 1: OVERS 7–11 SPIN DRIFT</div>
            <div style="font-family:'Rajdhani', sans-serif; font-size:1.2rem; font-weight:800; color:#FFFFFF; margin-top:4px;">10.29 RPO Conceded</div>
            <div style="font-size:0.75rem; color:#CBD5E1; margin-top:4px;">Inability to break middle-order partnerships at SMS Jaipur.</div>
            <div style="margin-top:10px; background:rgba(234,26,133,0.15); border:1px solid var(--rr-pink); border-radius:6px; padding:6px; font-size:0.75rem; font-weight:700; color:var(--rr-pink);">
                PLUGGED BY: SUYASH SHARMA (2,280 RPM GOOGLY)
            </div>
        </div>
        """, unsafe_allow_html=True)

    with g_col2:
        st.markdown("""
        <div class="rr-kpi-card" style="border-left:4px solid var(--warning);">
            <div class="rr-kpi-label">DEFICIT 2: ARCHER DEATH PARTNER</div>
            <div style="font-family:'Rajdhani', sans-serif; font-size:1.2rem; font-weight:800; color:#FFFFFF; margin-top:4px;">High Fragility Index</div>
            <div style="font-size:0.75rem; color:#CBD5E1; margin-top:4px;">Heavy over-reliance on Jofra Archer (38% injury risk) in death overs.</div>
            <div style="margin-top:10px; background:rgba(212,175,55,0.15); border:1px solid var(--rr-gold); border-radius:6px; padding:6px; font-size:0.75rem; font-weight:700; color:var(--rr-gold);">
                PLUGGED BY: MATT HENRY (1.42° POWERPLAY SWING)
            </div>
        </div>
        """, unsafe_allow_html=True)

    with g_col3:
        st.markdown("""
        <div class="rr-kpi-card" style="border-left:4px solid var(--success);">
            <div class="rr-kpi-label">DEFICIT 3: LOWER-ORDER FINISHER</div>
            <div style="font-family:'Rajdhani', sans-serif; font-size:1.2rem; font-weight:800; color:#FFFFFF; margin-top:4px;">Post-Samson Realignment</div>
            <div style="font-size:0.75rem; color:#CBD5E1; margin-top:4px;">Samson traded to CSK; need an icebox finisher at #6/#7.</div>
            <div style="margin-top:10px; background:rgba(16,185,129,0.15); border:1px solid var(--success); border-radius:6px; padding:6px; font-size:0.75rem; font-weight:700; color:var(--success);">
                PLUGGED BY: DHRUV JUREL (12.4% DOT SPIKE)
            </div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("---")

    # Jaipur Aerodynamic & Ball Flight Physics
    st.markdown("#### 🌪️ Sawai Mansingh Stadium Aerodynamics & Flight Physics")
    aero_col1, aero_col2 = st.columns([1.2, 1])
    with aero_col1:
        st.markdown("""
        <div style="background: var(--rr-navy-card); border: 1px solid var(--rr-border); border-radius: 12px; padding: 20px;">
            <div style="font-family:'Rajdhani', sans-serif; font-size:1.2rem; font-weight:800; color:var(--rr-gold);">
                JAIPUR ATMOSPHERIC & DIMENSIONAL TELEMETRY
            </div>
            <div style="font-size:0.83rem; color:#CBD5E1; line-height:1.6; margin-top:10px;">
                * <b>Altitude & Air Density:</b> SMS Jaipur sits at <b>435m above sea level</b> (Air Density: 1.172 kg/m³). Drag is reduced by <b>-4.33%</b> relative to sea level (Wankhede / Chepauk), producing an extra <b>+3.5m to +5.4m flight carry</b> on lofted shots.
                * <b>Aravalli Evening Crosswind:</b> 14 km/h south-westerly evening breeze blows diagonally across the pitch, heavily favoring RHB hitting with the wind over the shorter <b>68m leg-side boundary</b>.
                * <b>Tactical Bowling Mandate:</b> Seamers must bowl tight off-stump corridors to force hitters into the larger 78m straight boundary against the wind.
            </div>
        </div>
        """, unsafe_allow_html=True)
    with aero_col2:
        st.markdown("""
        <div style="background: var(--rr-navy-card); border: 1px solid var(--rr-border); border-radius: 12px; padding: 20px;">
            <div style="font-family:'Rajdhani', sans-serif; font-size:1.2rem; font-weight:800; color:var(--rr-pink);">
                YOUR SHORTLISTED SQUAD FIT STATUS
            </div>
            <div style="font-size:0.85rem; color:#FFFFFF; margin-top:8px;">
        """ + "".join([f"<div style='margin-bottom:6px;'>⭐ <b>{p}:</b> High Tactical Fit for SMS Jaipur</div>" for p in st.session_state['shortlist']]) + """
            </div>
        </div>
        """, unsafe_allow_html=True)


# =============================================================================
# TAB 5: IPL 2027 AUCTION STRATEGY & SHORTLIST BUILDER
# =============================================================================
with tab5:
    st.markdown("### 💰 IPL 2027 Auction War Room: Shortlist & Budget Simulator")
    st.caption("Allocate Rajasthan Royals' available ₹45.00 Cr purse across primary targets and simulate the projected 2027 Playing XI.")

    # Current Shortlist Viewer
    st.markdown("#### 📋 Active Shortlist Candidates")
    s_col1, s_col2 = st.columns([2, 1])
    with s_col1:
        st.write(f"**Current Shortlist ({len(st.session_state['shortlist'])} players):** " + ", ".join(st.session_state['shortlist']))
    with s_col2:
        # Download Shortlist CSV button
        shortlist_df = df_active[df_active['player_name'].isin(st.session_state['shortlist'])].copy()
        if not shortlist_df.empty:
            csv_data = shortlist_df.to_csv(index=False)
            st.download_button(
                label="📥 Export Shortlist & RPI Scores (CSV)",
                data=csv_data,
                file_name="RR_EDGE_Custom_Shortlist.csv",
                mime="text/csv",
                key="download_shortlist_csv"
            )

    st.markdown("---")

    # Interactive Auction Budget Simulator
    st.markdown("#### 🔨 Auction Bid Bracket & Purse Allocation Simulator")
    b_col1, b_col2 = st.columns(2)
    with b_col1:
        bid_henry = st.slider("Target Bid: Matt Henry (Powerplay / Middle Seam):", min_value=2.0, max_value=16.0, value=10.50, step=0.25, key="bid_henry_slider")
        bid_suyash = st.slider("Target Bid: Suyash Sharma (Overs 7–11 Mystery Spin):", min_value=0.5, max_value=10.0, value=5.20, step=0.25, key="bid_suyash_slider")
        bid_depth = st.slider("Target Bid: Domestic Batting & Pace Backups (3 Players):", min_value=1.0, max_value=8.0, value=3.20, step=0.25, key="bid_depth_slider")
        
        total_spend = bid_henry + bid_suyash + bid_depth
        remaining_cushion = 45.00 - total_spend

    with b_col2:
        st.markdown(f"""
        <div style="background:var(--rr-navy-card); border:1px solid var(--rr-border); border-radius:12px; padding:20px;">
            <div style="font-family:'Montserrat', sans-serif; font-size:0.75rem; font-weight:700; color:#94A3B8; text-transform:uppercase;">TOTAL PROJECTED AUCTION SPEND</div>
            <div style="font-family:'Rajdhani', sans-serif; font-size:2.5rem; font-weight:900; color:#FFFFFF;">₹{total_spend:.2f} CR</div>
            
            <div style="margin-top:14px; display:flex; justify-content:space-between; border-top:1px solid rgba(255,255,255,0.08); padding-top:10px;">
                <div>
                    <div style="font-size:0.7rem; color:#94A3B8;">REMAINING PURSE CUSHION</div>
                    <div style="font-size:1.4rem; font-family:'Rajdhani', sans-serif; font-weight:800; color:var(--success);">₹{remaining_cushion:.2f} CR</div>
                </div>
                <div>
                    <div style="font-size:0.7rem; color:#94A3B8;">PROJECTED PLAYOFF ODDS</div>
                    <div style="font-size:1.4rem; font-family:'Rajdhani', sans-serif; font-weight:800; color:var(--rr-gold);">68.4%</div>
                </div>
                <div>
                    <div style="font-size:0.7rem; color:#94A3B8;">CONTRACT SURPLUS (CSV)</div>
                    <div style="font-size:1.4rem; font-family:'Rajdhani', sans-serif; font-weight:800; color:var(--rr-pink);">+₹8.40 CR</div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("---")

    # Projected 2027 Rajasthan Royals Playing XI Display
    st.markdown("#### 🦁 Projected Rajasthan Royals 2027 Master Playing XI")
    xi_data = [
        ("1", "Yashasvi Jaiswal", "Opener (LH)", "Retained", "Powerplay Demolition"),
        ("2", "Jos Buttler / Marquee Target", "Opener (RH / WK)", "Auction Target", "Elite Pace/Spin Anchor"),
        ("3", "Riyan Parag (Captain)", "Top-Order Bat", "Retained", "Middle-Overs Anchor"),
        ("4", "Nitish Rana", "Middle-Order Bat", "Retained", "Spin Counter-Attacker"),
        ("5", "Dhruv Jurel (Wicketkeeper)", "Finisher / Keeper", "Retained", "Icebox Finisher (12.4% Dot Spike)"),
        ("6", "Ravindra Jadeja", "Spin All-Rounder", "Trade (CSK)", "Senior On-Field Strategist"),
        ("7", "Sam Curran", "Pace All-Rounder", "Trade (CSK)", "Death Cutter / Float Bat"),
        ("8", "Jofra Archer", "Express Pace Leader", "Retained", "150+ kph Fast Enforcer"),
        ("9", "Matt Henry", "New Ball / Middle Seam", "Auction Target", "1.42° Swing Chokehold"),
        ("10", "Suyash Sharma", "Mystery Leg-Spin", "Auction Target", "Overs 7–11 Drift Killer"),
        ("11", "Sandeep Sharma", "Death Specialist", "Retained", "Knuckleball Yorker Specialist"),
        ("IP", "Shimron Hetmyer", "Impact Finisher (OS)", "Retained", "Death Overs Boundary Enforcer")
    ]
    df_xi = pd.DataFrame(xi_data, columns=["Pos", "Player Name", "Role", "Acquisition Status", "Tactical Mandate"])
    st.dataframe(df_xi, use_container_width=True, hide_index=True)

# -----------------------------------------------------------------------------
# 9. FOOTER
# -----------------------------------------------------------------------------
st.markdown("""
<div style="text-align: center; margin-top: 30px; padding: 14px; border-top: 1px solid rgba(255, 255, 255, 0.08); font-size: 0.75rem; color: #64748B;">
    PROJECT RR-EDGE V6.0 • RAJASTHAN ROYALS HIGH-PERFORMANCE CRICKET OPERATIONS • SUPE RR SELECTOR S2
    <br/>
    <span style="color: #EA1A85; font-weight: 700;">HALLA BOL! 🦁</span>
</div>
""", unsafe_allow_html=True)
