"""
Append Console 15 to RR_EDGE_Dashboard/app.py and RR_EDGE_V3_0/dashboard/app.py
"""
import os
import py_compile

CONSOLE_15_CODE = '''

# -------------------------------------------------------------
# PAGE 15: RR-EDGE V4.1 LIVE FRANCHISE INTELLIGENCE & TRADE CENTER
# -------------------------------------------------------------
elif page == "15. RR-EDGE V4.1 Live Franchise Intelligence & Trade Center":
    st.markdown("<h1 style='color: #48CAE4;'>📡 RR-EDGE V4.1: LIVE FRANCHISE INTELLIGENCE CENTER</h1>", unsafe_allow_html=True)
    st.markdown("<h4 style='color: #FF70A6;'>Date-Stamped Market Radar | Pre-Retention Decision Trees | Reconciled 2026 Telemetry | Nov 2026</h4>", unsafe_allow_html=True)
    st.markdown("---")

    # Top KPI Metric Cards
    m1, m2, m3, m4, m5, m6 = st.columns(6)
    with m1:
        st.markdown("<div class='metric-box'><div class='metric-value'>17-NOV-2026</div><div class='metric-label'>Retention Deadline</div></div>", unsafe_allow_html=True)
    with m2:
        st.markdown("<div class='metric-box'><div class='metric-value'>16-DEC-2026</div><div class='metric-label'>Mini-Auction (Goa)</div></div>", unsafe_allow_html=True)
    with m3:
        st.markdown("<div class='metric-box'><div class='metric-value'>10 Trades</div><div class='metric-label'>Confirmed in League</div></div>", unsafe_allow_html=True)
    with m4:
        st.markdown("<div class='metric-box'><div class='metric-value'>25 Players</div><div class='metric-label'>Reconciled 2026 Squad</div></div>", unsafe_allow_html=True)
    with m5:
        st.markdown("<div class='metric-box'><div class='metric-value'>181 Sixes</div><div class='metric-label'>#1 Tournament High</div></div>", unsafe_allow_html=True)
    with m6:
        st.markdown("<div class='metric-box'><div class='metric-value'>₹33.65 Cr</div><div class='metric-label'>Plan B Unlocked Purse</div></div>", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    t1, t2, t3, t4, t5, t6 = st.tabs([
        "🕒 Live Radar & Confirmed Trades",
        "📋 Player Registry & RR-LSG Simulator",
        "🛡️ Reconciled Squad & 10-Phase Telemetry",
        "🌲 Pre-Retention Decision Trees",
        "🎯 Scouting Shortlists & Auction Engine",
        "🏟️ Multi-Venue Lineups & Governance"
    ])

    # ---------------------------------------------------------
    # TAB 1: LIVE RADAR & CONFIRMED TRADES
    # ---------------------------------------------------------
    with t1:
        st.subheader("🕒 Date-Stamped Live Intelligence Radar (Cut-off: 13-Nov-2026, 16:37 IST)")
        st.markdown(
            "This console provides an **evidence-governed intelligence pipeline** tracking real-world movements "
            "prior to the 17 November 2026 retention deadline and 16 December 2026 Mini-Auction in Goa."
        )

        timeline_path = os.path.join(BASE_DIR, "RR_EDGE_V4_1_Live_News_Timeline.csv")
        if os.path.exists(timeline_path):
            df_tl = pd.read_csv(timeline_path)
            status_filter = st.multiselect(
                "Filter Timeline by Epistemic Classification:",
                options=df_tl['status_classification'].unique(),
                default=df_tl['status_classification'].unique()
            )
            filtered_tl = df_tl[df_tl['status_classification'].isin(status_filter)]
            st.dataframe(filtered_tl, use_container_width=True)

        st.markdown("---")
        st.subheader("🤝 League-Wide Confirmed Trade Ledger (10 Verified Player Transfers)")
        st.info("💡 **Critical Market Reality:** Nathan Ellis was officially traded from CSK to SRH on 10 Nov 2026 in the 4-player deal. He is completely unavailable to RR.")

        trades_v4_path = os.path.join(BASE_DIR, "RR_EDGE_V4_1_Confirmed_Trades.csv")
        if os.path.exists(trades_v4_path):
            df_ct = pd.read_csv(trades_v4_path)
            st.dataframe(df_ct, use_container_width=True)

    # ---------------------------------------------------------
    # TAB 2: PLAYER REGISTRY & RR-LSG SIMULATOR
    # ---------------------------------------------------------
    with t2:
        st.subheader("📋 2027 Player Status & Availability Registry (40 Total Tracked Players)")
        status_path = os.path.join(BASE_DIR, "RR_EDGE_V4_1_2027_Player_Status_Registry.csv")
        if os.path.exists(status_path):
            df_stat = pd.read_csv(status_path)
            c_f1, c_f2 = st.columns(2)
            with c_f1:
                team_filter = st.multiselect("Filter by 2026 Franchise:", options=df_stat['franchise_2026'].unique(), default=['Rajasthan Royals', 'CSK', 'LSG', 'RCB', 'GT'])
            with c_f2:
                search_player = st.text_input("Search Player by Name:")

            sub_stat = df_stat[df_stat['franchise_2026'].isin(team_filter)]
            if search_player:
                sub_stat = sub_stat[sub_stat['player_name'].str.contains(search_player, case=False, na=False)]
            st.dataframe(sub_stat[['player_name', 'nationality', 'primary_role', 'franchise_2026', 'contract_salary_2026_cr', 'status_2027', 'trade_eligibility', 'auction_eligibility', 'injury_availability_notes']], use_container_width=True)

        st.markdown("---")
        st.subheader("🔄 RR-LSG Trade Negotiation Scenarios & Counterparty Simulator")
        st.warning("⚠️ **Epistemic Classification**: Classified strictly as `UNCONFIRMED_NEGOTIATION_REPORT`. Media reports confirm Shami/Curran talks, while Jaiswal-to-LSG trade speculation has formally stalled and is model-rejected.")

        scen_path = os.path.join(BASE_DIR, "RR_EDGE_V4_1_RR_LSG_Trade_Scenarios.csv")
        if os.path.exists(scen_path):
            df_scen = pd.read_csv(scen_path)
            selected_scen_id = st.selectbox("Select Trade Negotiation Scenario:", df_scen['scenario_id'] + " - " + df_scen['scenario_name'])
            scen_row = df_scen[df_scen['scenario_id'] == selected_scen_id.split(" - ")[0]].iloc[0]

            sc1, sc2, sc3 = st.columns(3)
            with sc1:
                st.markdown(f"**Trade In Players:** {scen_row['trade_in_players']}")
                st.markdown(f"**Trade Out Players:** {scen_row['trade_out_players']}")
            with sc2:
                st.markdown(f"**Net Purse Impact:** ₹{scen_row['net_purse_change_cr']:.2f} Cr")
                st.markdown(f"**Overseas Slot Delta:** {scen_row['overseas_slot_impact']}")
            with sc3:
                st.markdown(f"**Title Competitiveness:** `{scen_row['estimated_title_competitiveness']}`")
                st.markdown(f"**Epistemic Status:** `{scen_row.get('epistemic_classification', 'UNCONFIRMED_NEGOTIATION_REPORT')}`")

            st.markdown(f"**Tactical Evaluation:** {scen_row['tactical_evaluation']}")
            st.markdown(f"**Counterparty Incentive:** *{scen_row['counterparty_incentive']}*")

        st.markdown("#### Empirical Trade Valuation Model:")
        trade_val_path = os.path.join(BASE_DIR, "RR_EDGE_V4_1_Trade_Valuation.csv")
        if os.path.exists(trade_val_path):
            df_tv = pd.read_csv(trade_val_path)
            st.dataframe(df_tv, use_container_width=True)

    # ---------------------------------------------------------
    # TAB 3: RECONCILED SQUAD & 10-PHASE TELEMETRY
    # ---------------------------------------------------------
    with t3:
        st.subheader("🛡️ Reconciled Official 2026 Squad Baseline (25 Registered Players + 2 Reserves)")
        st.markdown("Audited against official 2026 auction purchases and retention declarations:")

        squad_path = os.path.join(BASE_DIR, "RR_EDGE_V4_1_Official_2026_Squad.csv")
        if os.path.exists(squad_path):
            df_sq = pd.read_csv(squad_path)
            acq_filter = st.radio("Filter Squad by Acquisition Source:", ["All 27 Entries", "Retained Core (16)", "2026 Auction Additions (9)", "Reserves (2)"], horizontal=True)
            if "Retained Core" in acq_filter:
                df_sq_show = df_sq[df_sq['acquisition_type'] == 'Retained Pre-2026']
            elif "Auction" in acq_filter:
                df_sq_show = df_sq[df_sq['acquisition_type'] == 'Auction 2026']
            elif "Reserves" in acq_filter:
                df_sq_show = df_sq[df_sq['acquisition_type'] == 'Reserve Pool']
            else:
                df_sq_show = df_sq
            st.dataframe(df_sq_show[['canonical_id', 'player_name', 'role', 'nationality', 'acquisition_type', 'official_2026_salary_cr', 'source']], use_container_width=True)

        st.markdown("---")
        st.subheader("📊 10-Phase Empirical Performance Diagnosis (3,788 Deliveries Across 16 Matches)")
        st.markdown("Grounded in official ball-by-ball tournament telemetry (`comp_id == 3298`):")

        perf_path = os.path.join(BASE_DIR, "RR_EDGE_V4_1_2026_Performance_Diagnosis.csv")
        if os.path.exists(perf_path):
            df_pd = pd.read_csv(perf_path)
            st.dataframe(df_pd, use_container_width=True)

            st.error("🚨 **The Root Cause Bottleneck:** While RR dominated the powerplay (11.06 RR, #1) and six-hitting (181 sixes, #1), they conceded 10.29 RPO in overs 7–11 (#10 / worst in IPL) and lacked death support for Archer (who took 27.6% of team wickets).")

    # ---------------------------------------------------------
    # TAB 4: PRE-RETENTION DECISION TREES
    # ---------------------------------------------------------
    with t4:
        st.subheader("🌲 Pre-Retention Decision Trees (Deadline: 17 November 2026)")
        st.markdown(
            "Comparative evaluation of pre-retention strategic plans before submitting lists to the BCCI:"
        )

        plan_summary_cards = [
            {"Plan": "Plan A (Conservative)", "Retained": 17, "Released": 8, "Committed": "₹108.95 Cr", "Purse": "₹19.65 Cr", "Win%": "56.5%", "Verdict": "Restricts liquidity; leaves bowling bottleneck unresolved."},
            {"Plan": "Plan B (Rebalance) [RECOMMENDED]", "Retained": 14, "Released": 11, "Committed": "₹94.95 Cr", "Purse": "₹33.65 Cr", "Win%": "64.8%", "Verdict": "Optimal balance: releases Hetmyer (₹11.0 Cr), Deshpande (₹6.5 Cr), Milne (₹2.2 Cr) to fund elite death pacer + control spinner."},
            {"Plan": "Plan C (Trade Scenario)", "Retained": "14 + 1 Traded", "Released": 10, "Committed": "₹101.45 Cr", "Purse": "₹27.15 Cr", "Win%": "61.2%", "Verdict": "High tactical upside via Shami/Curran trade, but dependent on rival counterparty consent."}
        ]
        st.dataframe(pd.DataFrame(plan_summary_cards), use_container_width=True)

        st.markdown("#### Detailed Retention & Release Ledgers:")
        c_r1, c_r2 = st.columns(2)
        with c_r1:
            st.markdown("**Retention Recommendations:**")
            ret_path = os.path.join(BASE_DIR, "RR_EDGE_V4_1_Retention_Analysis.csv")
            if os.path.exists(ret_path):
                df_ret = pd.read_csv(ret_path)
                st.dataframe(df_ret[['player_name', 'role', 'contract_salary_cr', 'decision_plan_a', 'decision_plan_b']], use_container_width=True)
        with c_r2:
            st.markdown("**Release & Purse Recovery:**")
            rel_path = os.path.join(BASE_DIR, "RR_EDGE_V4_1_Release_Analysis.csv")
            if os.path.exists(rel_path):
                df_rel = pd.read_csv(rel_path)
                st.dataframe(df_rel, use_container_width=True)

    # ---------------------------------------------------------
    # TAB 5: SCOUTING SHORTLISTS & AUCTION ENGINE
    # ---------------------------------------------------------
    with t5:
        st.subheader("🎯 Role-Based Scouting Shortlists Across 9 Specialized Categories")
        scout_path = os.path.join(BASE_DIR, "RR_EDGE_V4_1_Scouting_Shortlist.csv")
        if os.path.exists(scout_path):
            df_sc = pd.read_csv(scout_path)
            cat_choice = st.selectbox("Select Tactical Scouting Category:", ["All Categories"] + list(df_sc['scouting_category'].unique()))
            if cat_choice != "All Categories":
                df_sc_show = df_sc[df_sc['scouting_category'] == cat_choice]
            else:
                df_sc_show = df_sc
            st.dataframe(df_sc_show[['scouting_category', 'candidate_name', 'current_status', 'target_route', 'projected_cost_cr', 'recent_t20_performance', 'tactical_fit_score', 'governance_note']], use_container_width=True)

        st.markdown("---")
        st.subheader("🔨 Probabilistic Mini-Auction Simulator & Walk-Away Ceilings (Goa, 16 Dec 2026)")
        st.markdown(
            "Modeled across 500 simulated ascending auction iterations against rival purse distributions (PBKS ₹110.5 Cr, KKR ₹64.3 Cr, SRH ₹45.8 Cr, RR ₹33.65 Cr):"
        )
        auc_path = os.path.join(BASE_DIR, "RR_EDGE_V4_1_Auction_Scenarios.csv")
        if os.path.exists(auc_path):
            df_auc = pd.read_csv(auc_path)
            st.dataframe(df_auc, use_container_width=True)

    # ---------------------------------------------------------
    # TAB 6: MULTI-VENUE LINEUPS & GOVERNANCE
    # ---------------------------------------------------------
    with t6:
        st.subheader("🏟️ Multi-Venue Validated Starting Blueprints & Impact Deployments")
        st.markdown("Full compliance with BCCI Clauses 1.2.5 & 1.2.6 (Max 4 Overseas players on field at any point):")

        sheets_path = os.path.join(BASE_DIR, "RR_EDGE_V4_1_Validated_Team_Sheets.csv")
        if os.path.exists(sheets_path):
            df_vsh = pd.read_csv(sheets_path)
            venue_sel = st.selectbox("Select IPL Venue Blueprint:", df_vsh['lineup_name'].unique())
            vrow = df_vsh[df_vsh['lineup_name'] == venue_sel].iloc[0]

            vc1, vc2 = st.columns(2)
            with vc1:
                st.markdown(f"**Scenario Type:** `{vrow['scenario_type']}`")
                st.markdown(f"**Captain:** {vrow['captain']} | **Wicketkeeper:** {vrow['wicketkeeper']}")
                st.markdown(f"**Starting Overseas Count:** {vrow['starting_overseas_count']} OS")
                st.markdown(f"**Starting XI:** {vrow['starting_11']}")
            with vc2:
                st.markdown(f"**Impact Sub IN:** {vrow['impact_player_in']}")
                st.markdown(f"**Impact Sub OUT:** {vrow['impact_player_out']}")
                st.markdown(f"**BCCI Compliance:** `{vrow['bcci_clause_compliance']}`")
                st.markdown(f"**20 Overs Allocation:** {vrow['bowling_allocation_20_overs']}")

        st.markdown("---")
        st.subheader("💰 Multi-Tab Financial Reconciliation & Decimal Integrity")
        fin_path = os.path.join(BASE_DIR, "RR_EDGE_V4_1_Financial_Reconciliation.csv")
        if os.path.exists(fin_path):
            df_f = pd.read_csv(fin_path)
            st.dataframe(df_f, use_container_width=True)

        st.markdown("---")
        st.subheader("🏛️ Corporate Governance & Ownership Note")
        st.markdown(
            "**CCI Approval Governance:** On 17 September 2026, the Competition Commission of India approved the acquisition "
            "of controlling interest in EMSH (parent entity of Rajasthan Royals) by Westview Cricket (~75%) and Poonawalla Sports (~18%). "
            "While this establishes an enterprise valuation of approximately $1.65 Billion, BCCI IPL Governance Rules strictly enforce a "
            "standardized salary cap (₹120.00 Cr - ₹125.00 Cr for IPL 2027). Under no circumstances does corporate restructuring allow "
            "the franchise to exceed auction spend limits. All financial planning models strictly adhere to BCCI salary cap limits."
        )

        st.markdown("---")
        st.subheader("📑 Master Epistemic Claim Registry & Evidence Citations")
        claim_path = os.path.join(BASE_DIR, "RR_EDGE_V4_1_Claim_Registry.csv")
        if os.path.exists(claim_path):
            df_cl = pd.read_csv(claim_path)
            st.dataframe(df_cl, use_container_width=True)
'''

def update_file(file_path):
    print(f"Updating {file_path}...")
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()

    # Ensure radio option is added if not present
    if '"15. RR-EDGE V4.1 Live Franchise Intelligence & Trade Center"' not in content:
        content = content.replace(
            '"14. RR-EDGE V4.0.1 Definitive Intelligence & Governance Center"',
            '"14. RR-EDGE V4.0.1 Definitive Intelligence & Governance Center",\n        "15. RR-EDGE V4.1 Live Franchise Intelligence & Trade Center"'
        )

    # Append Console 15 code if not already present
    if 'elif page == "15. RR-EDGE V4.1 Live Franchise Intelligence & Trade Center":' not in content:
        content += CONSOLE_15_CODE

    with open(file_path, "w", encoding="utf-8") as f:
        f.write(content)

    py_compile.compile(file_path, doraise=True)
    print(f"Successfully compiled and validated {file_path}")

if __name__ == "__main__":
    update_file("RR_EDGE_Dashboard/app.py")
    update_file("RR_EDGE_V3_0/dashboard/app.py")
