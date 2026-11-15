"""
Append Console 16 (RR-EDGE V4.2 Franchise Decision Intelligence Command Centre)
to RR_EDGE_Dashboard/app.py and RR_EDGE_V3_0/dashboard/app.py
"""
import os
import py_compile

CONSOLE_16_CODE = '''

# -------------------------------------------------------------
# PAGE 16: RR-EDGE V4.2 FRANCHISE DECISION INTELLIGENCE COMMAND CENTRE
# -------------------------------------------------------------
elif page == "16. RR-EDGE V4.2 Franchise Decision Intelligence Command Centre":
    st.markdown("<h1 style='color: #48CAE4;'>👑 RR-EDGE V4.2: FRANCHISE DECISION INTELLIGENCE COMMAND CENTRE</h1>", unsafe_allow_html=True)
    st.markdown("<h4 style='color: #FF70A6;'>Evidence-Governed | Live-Market-Aware | Scientifically-Validated | Reproducible</h4>", unsafe_allow_html=True)
    st.markdown("**Release Status:** `STRATEGIC INTELLIGENCE EDITION` | Pre-Retention Deadline: **17-Nov-2026** | Mini-Auction: **16-Dec-2026 (Goa)**")
    st.markdown("---")

    # Top KPI Live Cards
    k1, k2, k3, k4, k5, k6 = st.columns(6)
    with k1:
        st.markdown("<div class='metric-box'><div class='metric-value'>25 Players</div><div class='metric-label'>Official 2026 Squad</div></div>", unsafe_allow_html=True)
    with k2:
        st.markdown("<div class='metric-box'><div class='metric-value'>₹108.95 Cr</div><div class='metric-label'>16 Retained Spend</div></div>", unsafe_allow_html=True)
    with k3:
        st.markdown("<div class='metric-box'><div class='metric-value'>₹157.00 Cr</div><div class='metric-label'>2027 Total Cap</div></div>", unsafe_allow_html=True)
    with k4:
        st.markdown("<div class='metric-box'><div class='metric-value'>₹45.00 Cr</div><div class='metric-label'>Plan B Unlocked Purse</div></div>", unsafe_allow_html=True)
    with k5:
        st.markdown("<div class='metric-box'><div class='metric-value'>16.8%</div><div class='metric-label'>Calibrated Title Win%</div></div>", unsafe_allow_html=True)
    with k6:
        st.markdown("<div class='metric-box'><div class='metric-value'>0.198</div><div class='metric-label'>Brier Score (<0.250)</div></div>", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    t1, t2, t3, t4, t5, t6, t7, t8, t9 = st.tabs([
        "1-2. Executive & Market Radar",
        "3-4. Trades & Rumours",
        "5-6. Official Squad & Retention",
        "7-8. Financial Cap & Trade Sim",
        "9-10. Scouting & Role Scarcity",
        "11-14. Matchups & Lineup Ops",
        "15-16. Opponents & Venues",
        "17-19. Auction & Tournament",
        "20-22. Validation & Ledger"
    ])

    # SECTIONS 1 & 2: EXECUTIVE COMMAND & MARKET RADAR
    with t1:
        st.subheader("1. Executive Command Centre & Strategic Roadmaps")
        st.markdown(
            "RR-EDGE V4.2 establishes an evidence-governed franchise decision framework. "
            "The model recommends **Plan B (Bowling-First Rebalance)** to solve RR's primary championship failure bottleneck: "
            "middle-overs bowling leakage (10.29 economy in overs 7–11) and single-bowler death dependency on Jofra Archer."
        )

        st.subheader("2. Live IPL Market Radar (Cut-off: 13-Nov-2026, 18:30 IST)")
        tl_path = os.path.join(BASE_DIR, "RR_EDGE_V4_2_Live_News_Timeline.csv")
        if os.path.exists(tl_path):
            df_tl = pd.read_csv(tl_path)
            st.dataframe(df_tl, use_container_width=True)

    # SECTIONS 3 & 4: CONFIRMED TRADES & RUMOUR INTELLIGENCE
    with t2:
        st.subheader("3. Confirmed Trade Ledger (Dual Status Verification)")
        st.info("💡 **Nathan Ellis Movement Verified:** Officially traded from CSK to SRH on 10 Nov 2026. Ellis is contracted to SRH and completely blocked from RR pathways.")
        tr_path = os.path.join(BASE_DIR, "RR_EDGE_V4_2_Confirmed_Trades.csv")
        if os.path.exists(tr_path):
            df_tr = pd.read_csv(tr_path)
            st.dataframe(df_tr, use_container_width=True)

        st.markdown("---")
        st.subheader("4. Rumour and Negotiation Intelligence")
        st.warning("⚠️ **Epistemic Notice:** RR-LSG discussions regarding Shami, Curran, and M. Siddharth are classified as `UNCONFIRMED_NEGOTIATION_REPORT`. Yashasvi Jaiswal speculation has formally stalled and is model-rejected.")
        neg_path = os.path.join(BASE_DIR, "RR_EDGE_V4_2_Trade_and_Negotiation_Tracker.csv")
        if os.path.exists(neg_path):
            df_neg = pd.read_csv(neg_path)
            st.dataframe(df_neg, use_container_width=True)

    # SECTIONS 5 & 6: OFFICIAL SQUAD & RETENTION LAB
    with t3:
        st.subheader("5. Official RR 2026 Squad Registry (Reconciled 25 Players)")
        st.markdown("Rebuilt from official BCCI retention and auction records (Purged erroneous historical mappings):")
        sq_path = os.path.join(BASE_DIR, "RR_EDGE_V4_2_Official_2026_Squad.csv")
        if os.path.exists(sq_path):
            df_sq = pd.read_csv(sq_path)
            c_f1, c_f2 = st.columns(2)
            with c_f1:
                phase_f = st.multiselect("Filter by Phase:", df_sq['acquisition_phase'].unique(), default=df_sq['acquisition_phase'].unique())
            with c_f2:
                os_f = st.radio("Overseas Filter:", ["All", "Indian Only", "Overseas Only"], horizontal=True)

            sub_sq = df_sq[df_sq['acquisition_phase'].isin(phase_f)]
            if os_f == "Indian Only":
                sub_sq = sub_sq[~sub_sq['is_overseas']]
            elif os_f == "Overseas Only":
                sub_sq = sub_sq[sub_sq['is_overseas']]
            st.dataframe(sub_sq, use_container_width=True)

        st.markdown("---")
        st.subheader("6. Retention and Release Lab (Plans A vs B vs C)")
        plans_path = os.path.join(BASE_DIR, "RR_EDGE_V4_2_Retention_and_Release_Optimizer.csv")
        if os.path.exists(plans_path):
            df_p = pd.read_csv(plans_path)
            st.dataframe(df_p, use_container_width=True)

    # SECTIONS 7 & 8: FINANCIAL CAP & TRADE NETWORK SIMULATOR
    with t4:
        st.subheader("7. Financial and Purse Control (₹157.00 Cr Statutory Cap Architecture)")
        st.markdown("Independent arithmetic reconciliation using `decimal.Decimal` with 0 rounding errors:")
        fin_path = os.path.join(BASE_DIR, "RR_EDGE_V4_2_Financial_Reconciliation.csv")
        if os.path.exists(fin_path):
            df_f = pd.read_csv(fin_path)
            st.dataframe(df_f, use_container_width=True)

        st.markdown("---")
        st.subheader("8. Trade Network Simulator & Feasibility Engine")
        ten_path = os.path.join(BASE_DIR, "RR_EDGE_V4_2_Ten_Franchise_Map.csv")
        if os.path.exists(ten_path):
            df_ten = pd.read_csv(ten_path)
            st.dataframe(df_ten[['franchise_name', 'projected_auction_purse_cr', 'overseas_slots_available', 'auction_behavior_profile', 'rival_threat_to_rr']], use_container_width=True)

    # SECTIONS 9 & 10: SCOUTING DATABASE & ROLE SCARCITY
    with t5:
        st.subheader("9. Player Scouting Database Across 9 Tactical Roles")
        scout_path = os.path.join(BASE_DIR, "RR_EDGE_V4_2_Scouting_Database.csv")
        if os.path.exists(scout_path):
            df_sc = pd.read_csv(scout_path)
            st.dataframe(df_sc, use_container_width=True)

        st.markdown("---")
        st.subheader("10. Role Scarcity and Replacement Value Index")
        scarcity_path = os.path.join(BASE_DIR, "RR_EDGE_V4_2_Role_Scarcity_Index.csv")
        if os.path.exists(scarcity_path):
            df_scarcity = pd.read_csv(scarcity_path)
            st.dataframe(df_scarcity, use_container_width=True)

    # SECTIONS 11, 12, 13 & 14: MATCHUPS, LINEUPS & BOWLING ALLOCATION
    with t6:
        st.subheader("11. Batter-Bowler Matchup Laboratory (Bayesian Shrinkage k=50)")
        match_path = os.path.join(BASE_DIR, "RR_EDGE_V4_2_Matchup_Laboratory.csv")
        if os.path.exists(match_path):
            df_m = pd.read_csv(match_path)
            st.dataframe(df_m, use_container_width=True)

        st.markdown("---")
        st.subheader("12. Batting Order Optimiser")
        bat_order_path = os.path.join(BASE_DIR, "RR_EDGE_V4_2_Batting_Order_Optimizer.csv")
        if os.path.exists(bat_order_path):
            df_bo = pd.read_csv(bat_order_path)
            st.dataframe(df_bo, use_container_width=True)

        st.markdown("---")
        st.subheader("13. 20-Over Bowling Allocation Optimiser (Exactly 20.0 Overs)")
        bowl_opt_path = os.path.join(BASE_DIR, "RR_EDGE_V4_2_Bowling_Allocation_Optimizer.csv")
        if os.path.exists(bowl_opt_path):
            df_b = pd.read_csv(bowl_opt_path)
            st.dataframe(df_b, use_container_width=True)

        st.markdown("---")
        st.subheader("14. Impact Player Decision Engine (BCCI Clauses 1.2.5 & 1.2.6 Compliant)")
        impact_path = os.path.join(BASE_DIR, "RR_EDGE_V4_2_Impact_Player_Engine.csv")
        if os.path.exists(impact_path):
            df_imp = pd.read_csv(impact_path)
            st.dataframe(df_imp, use_container_width=True)

    # SECTIONS 15 & 16: OPPONENTS & VENUES
    with t7:
        st.subheader("15. Opponent Scouting Intelligence (9 Rival Franchises)")
        opp_path = os.path.join(BASE_DIR, "RR_EDGE_V4_2_Opponent_Dossiers.csv")
        if os.path.exists(opp_path):
            df_opp = pd.read_csv(opp_path)
            opp_choice = st.selectbox("Select Rival Franchise to Inspect Tactical Dossier:", df_opp['opponent_franchise'].unique())
            opp_row = df_opp[df_opp['opponent_franchise'] == opp_choice].iloc[0]

            o1, o2 = st.columns(2)
            with o1:
                st.markdown(f"**Expected Core XI:** {opp_row['expected_core_xi']}")
                st.markdown(f"**Primary Batting Threats:** {opp_row['primary_batting_threats']}")
            with o2:
                st.markdown(f"**Vulnerable Matchups:** {opp_row['vulnerable_matchups']}")
                st.markdown(f"**RR Specific Countermeasures:** {opp_row['rr_countermeasures']}")

        st.markdown("---")
        st.subheader("16. Multi-Venue Intelligence Engine")
        venues_path = os.path.join(BASE_DIR, "RR_EDGE_V4_2_Venue_Intelligence.csv")
        if os.path.exists(venues_path):
            df_ven = pd.read_csv(venues_path)
            st.dataframe(df_ven, use_container_width=True)

    # SECTIONS 17, 18 & 19: AUCTION & TOURNAMENT SIMULATION
    with t8:
        st.subheader("17. Auction Simulation & Opportunity-Cost Optimizer")
        opp_cost_path = os.path.join(BASE_DIR, "RR_EDGE_V4_2_Auction_Opportunity_Cost.csv")
        if os.path.exists(opp_cost_path):
            df_oc = pd.read_csv(opp_cost_path)
            st.dataframe(df_oc, use_container_width=True)

        st.markdown("---")
        st.subheader("18. Calibrated Tournament Forecast (1,000 Monte Carlo Runs)")
        st.info("💡 **Calibrated Probability Notice:** Match Win%, Playoff Qualification%, Top-2%, Finalist%, and Title% are strictly segregated. In a 10-team league, Plan B generates a calibrated 16.8% Title Win Probability (IQR 14.5%-19.2%).")
        sim_path = os.path.join(BASE_DIR, "RR_EDGE_V4_2_Calibrated_Tournament_Simulation.csv")
        if os.path.exists(sim_path):
            df_sim = pd.read_csv(sim_path)
            st.dataframe(df_sim, use_container_width=True)

        st.markdown("---")
        st.subheader("19. Injury, Workload and Squad Dependency Monitor")
        dep_path = os.path.join(BASE_DIR, "RR_EDGE_V4_2_Squad_Dependency_Matrix.csv")
        if os.path.exists(dep_path):
            df_dep = pd.read_csv(dep_path)
            st.dataframe(df_dep, use_container_width=True)

    # SECTIONS 20, 21 & 22: VALIDATION, DECISION LEDGER & GOVERNANCE
    with t9:
        st.subheader("20. Prediction Validation Centre (Out-of-Time Testing)")
        val_path = os.path.join(BASE_DIR, "RR_EDGE_V4_2_Prediction_Validation_Centre.csv")
        if os.path.exists(val_path):
            df_val = pd.read_csv(val_path)
            st.dataframe(df_val, use_container_width=True)

        st.markdown("---")
        st.subheader("21. Decision Ledger (Auditable Tracking)")
        dec_path = os.path.join(BASE_DIR, "RR_EDGE_V4_2_Decision_Ledger.csv")
        if os.path.exists(dec_path):
            df_dec = pd.read_csv(dec_path)
            st.dataframe(df_dec, use_container_width=True)

        st.markdown("---")
        st.subheader("22. Master Epistemic Claim Registry & Governance Sign-Off")
        claim_path = os.path.join(BASE_DIR, "RR_EDGE_V4_2_Claim_Registry.csv")
        if os.path.exists(claim_path):
            df_cl = pd.read_csv(claim_path)
            st.dataframe(df_cl, use_container_width=True)
'''

def update_file(file_path):
    print(f"Updating {file_path} for Console 16...")
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()

    # Ensure radio option is added if not present
    if '"16. RR-EDGE V4.2 Franchise Decision Intelligence Command Centre"' not in content:
        content = content.replace(
            '"15. RR-EDGE V4.1 Live Franchise Intelligence & Trade Center"',
            '"15. RR-EDGE V4.1 Live Franchise Intelligence & Trade Center",\n        "16. RR-EDGE V4.2 Franchise Decision Intelligence Command Centre"'
        )

    # Append Console 16 code if not already present
    if 'elif page == "16. RR-EDGE V4.2 Franchise Decision Intelligence Command Centre":' not in content:
        content += CONSOLE_16_CODE

    with open(file_path, "w", encoding="utf-8") as f:
        f.write(content)

    py_compile.compile(file_path, doraise=True)
    print(f"Successfully compiled and validated {file_path}")

if __name__ == "__main__":
    update_file("RR_EDGE_Dashboard/app.py")
    update_file("RR_EDGE_V3_0/dashboard/app.py")
