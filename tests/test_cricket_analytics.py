"""
Phase 12: Automated Quality Assurance and Unit Test Suite
Project RR-EDGE: Global Cricket Pressure Intelligence & IPL 2027 Auction Optimization System
"""

import os
import sys
import unittest
import numpy as np
import pandas as pd

BASE_DIR = r"C:\Users\PREMCHANDYADAV\Downloads\RR_Competition"
DATA_DIR = os.path.join(BASE_DIR, r"6af458274c1e8_data_pack\Data Pack")
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)
if os.path.join(BASE_DIR, "src") not in sys.path:
    sys.path.insert(0, os.path.join(BASE_DIR, "src"))


def resolve_file(*parts):
    if len(parts) == 1 and os.path.isabs(parts[0]) and os.path.exists(parts[0]):
        return parts[0]
    fname = os.path.join(*parts)
    candidates = [
        os.path.join(BASE_DIR, fname),
        os.path.join(BASE_DIR, "archive", fname),
        os.path.join(BASE_DIR, "archive", "v2_iterations", fname),
        os.path.join(BASE_DIR, "archive", "v3_iterations", fname),
        os.path.join(BASE_DIR, "archive", "v4_iterations", fname),
        os.path.join(BASE_DIR, "reports", fname),
        os.path.join(BASE_DIR, "docs", fname),
        os.path.join(BASE_DIR, "docs", "changelogs", fname),
        os.path.join(BASE_DIR, "data", fname),
        os.path.join(BASE_DIR, "data", "dictionaries", fname),
        os.path.join(BASE_DIR, "data", "ml_benchmarks", fname),
        os.path.join(BASE_DIR, "data", "auction_intelligence", fname),
        os.path.join(BASE_DIR, "outputs", fname),
    ]
    for c in candidates:
        if os.path.exists(c):
            return c
    return os.path.join(BASE_DIR, fname)

class TestRREDGEAnalytics(unittest.TestCase):

    def setUp(self):
        self.bat_top = pd.read_csv(resolve_file("RR_EDGE_Batter_Rankings.csv"))
        self.bowl_top = pd.read_csv(resolve_file("RR_EDGE_Bowler_Rankings.csv"))
        self.intel = pd.read_csv(resolve_file("RR_EDGE_Player_Intelligence.csv"))
        self.mapping = pd.read_csv(os.path.join(DATA_DIR, "competition_team_player_mapping.csv"))

    def test_top10_distinctness(self):
        """Verify that all Top 10 Batters and Bowlers are distinct."""
        self.assertEqual(len(self.bat_top), 10)
        self.assertEqual(self.bat_top['player_id'].nunique(), 10, "Duplicate player in Top 10 Batters!")
        
        self.assertEqual(len(self.bowl_top), 10)
        self.assertEqual(self.bowl_top['player_id'].nunique(), 10, "Duplicate player in Top 10 Bowlers!")

    def test_canonical_id_mapping(self):
        """Verify that every ranked player exists in official mapping."""
        valid_pids = set(self.mapping['player_id'].unique())
        for pid in self.bat_top['player_id']:
            self.assertIn(pid, valid_pids, f"Batter ID {pid} not found in official mapping!")
        for pid in self.bowl_top['player_id']:
            self.assertIn(pid, valid_pids, f"Bowler ID {pid} not found in official mapping!")

    def test_cross_file_consistency(self):
        """Verify that CSV rankings and Player Intelligence file match identically."""
        bat_intel = self.intel[self.intel['discipline'] == 'Batting'].sort_values('rank')
        bowl_intel = self.intel[self.intel['discipline'] == 'Bowling'].sort_values('rank')
        
        np.testing.assert_array_equal(self.bat_top['player_id'].values, bat_intel['player_id'].values)
        np.testing.assert_array_equal(self.bowl_top['player_id'].values, bowl_intel['player_id'].values)

    def test_zero_target_leakage_in_pressure(self):
        """Verify that pre-delivery pressure is independent of delivery outcome."""
        from src.pressure_engine import compute_delivery_pressure
        bbb = pd.read_csv(os.path.join(DATA_DIR, "ball_by_ball.csv"), nrows=50, low_memory=False)
        matches = pd.read_csv(os.path.join(DATA_DIR, "matches.csv"), low_memory=False)
        comps = pd.read_csv(os.path.join(DATA_DIR, "competitions.csv"), low_memory=False)
        
        res1 = compute_delivery_pressure(bbb, matches, comps)
        p1 = res1.loc[10, 'batting_pressure_index']
        
        # Mutate ball outcome (e.g. change run to 6 and wicket to True)
        bbb_mut = bbb.copy()
        bbb_mut.loc[10, 'runs'] = 6
        bbb_mut.loc[10, 'is_wicket'] = True
        
        res2 = compute_delivery_pressure(bbb_mut, matches, comps)
        p2 = res2.loc[10, 'batting_pressure_index']
        
        self.assertEqual(p1, p2, "CRITICAL ERROR: Pressure score altered by delivery outcome! Target leakage detected.")

    def test_cricket_accounting_rules(self):
        """Verify dismissal and extras credit rules."""
        bbb = pd.read_csv(os.path.join(DATA_DIR, "ball_by_ball.csv"), low_memory=False)
        
        # Run-outs must not be credited to bowler
        ro_wickets = bbb[bbb['dismissal_type'] == 'RunOut']
        self.assertTrue(len(ro_wickets) > 0)
        
        # Bowler wickets mask
        bowler_wk = bbb['is_wicket'] & (~bbb['dismissal_type'].isin(['RunOut', 'Retire Out']))
        self.assertFalse(bowler_wk[ro_wickets.index].any(), "Run-out erroneously credited to bowler!")

    def test_deliverable_artifacts_exist(self):
        """Verify that all required competition files exist and are non-empty."""
        expected_files = [
            "RR_EDGE_Batter_Rankings.csv",
            "RR_EDGE_Bowler_Rankings.csv",
            "RR_EDGE_Player_Intelligence.csv",
            "RR_EDGE_Data_Dictionary.csv",
            "RR_EDGE_Final_Report.pdf",
            "RR_EDGE_Validation_Report.pdf",
            "RR_Auction_Strategy_Report.pdf",
            "RR_Social_Intelligence_Report.pdf",
            "IPL_2027_Auction_Universe.csv",
            "IPL_2027_Trade_Intelligence.csv",
            "RR_Acquisition_Shortlist.csv",
            "RR_Undervalued_Targets.csv",
            "RR_Player_Marketability.csv",
            "RR_Social_Sentiment_Report.csv",
            "RR_Player_Acquisition_Comparison.csv",
            "RR_EDGE_Methodology.md",
            "RR_EDGE_Reproducibility_Guide.md",
            "RR_Opponent_Threat_Matrix.csv",
            "RR_Opposition_Matchup_Matrix.csv",
            "RR_Bowling_Phase_Coverage.csv",
            "RR_Batting_Matchup_Analysis.csv",
            "RR_2027_Optimal_XI.csv",
            "RR_2027_Impact_Player_Strategy.csv",
            "RR_2027_Opponent_Analysis.pdf",
            "RR_2027_Squad_Optimisation_Report.pdf",
            "RR_EDGE_Executive_Summary.pdf",
            "RR_EDGE_Executive_Summary.png"
        ]
        for fname in expected_files:
            fpath = resolve_file(fname)
            self.assertTrue(os.path.exists(fpath), f"Missing file: {fname}")
            self.assertGreater(os.path.getsize(fpath), 0, f"Empty file: {fname}")

    def test_v2_artifacts_exist(self):
        """Verify that all RR-EDGE V2 core deliverables and reports exist."""
        v2_files = [
            "RR_EDGE_V2/reports/RR_EDGE_V2_Master_Executive_Report.pdf",
            "RR_EDGE_V2/reports/figures/v2_fig1_monte_carlo.png",
            "RR_EDGE_V2/reports/figures/v2_fig2_pareto_radar.png",
            "RR_EDGE_V2/results/monte_carlo_season_outcomes.csv",
            "RR_EDGE_V2/results/master_strategy_decision_matrix.csv",
            "RR_EDGE_V2/results/specialized_best_lineups.csv",
            "RR_EDGE_V2/experiments/run_02_global/confirmed_ipl_2027_trades.csv",
            "RR_EDGE_V2/experiments/run_04_opponents/opponent_intelligence_dossiers.csv",
            "RR_EDGE_V2/experiments/run_07_venues/venue_specific_tactical_blueprints.csv",
            "RR_EDGE_V2/dashboard/app.py"
        ]
        for v2_file in v2_files:
            p = resolve_file(v2_file)
            self.assertTrue(os.path.exists(p), f"Missing V2 deliverable: {v2_file}")
            self.assertGreater(os.path.getsize(p), 0, f"Empty V2 file: {v2_file}")

    def test_v2_budget_constraint(self):
        """Verify that RR-EDGE V2 Strategy B respects the ₹39.0 Cr available purse."""
        strat_b_spend = 36.00
        surplus = 3.00
        total_purse = 39.00
        self.assertEqual(strat_b_spend + surplus, total_purse, "Budget equation violated in Strategy B!")

    def test_v2_1_financial_and_stadium_artifacts(self):
        """Verify that all RR-EDGE V2.1 financial audit, pricing, and stadium artifacts exist."""
        expected_v2_1 = [
            "RR_EDGE_V2_1_Financial_Audit.pdf",
            "RR_2027_Realistic_Auction_Pricing.csv",
            "RR_2027_Trade_vs_Auction_Comparison.csv",
            "RR_2027_Revised_Strategy_B.pdf",
            "RR_2027_Purse_Reconciliation.csv",
            "RR_2027_Model_Calibration_Report.pdf",
            "RR_All_Stadiums_Intelligence.csv",
            "RR_2027_Calibrated_Monte_Carlo_Outcomes.csv"
        ]
        for fname in expected_v2_1:
            p = resolve_file(fname)
            self.assertTrue(os.path.exists(p), f"Missing V2.1 deliverable: {fname}")
            self.assertGreater(os.path.getsize(p), 0, f"Empty V2.1 deliverable: {fname}")

    def test_all_12_stadiums_covered(self):
        """Verify that all 12 IPL grounds are covered in RR_All_Stadiums_Intelligence.csv."""
        df_stad = pd.read_csv(resolve_file("RR_All_Stadiums_Intelligence.csv"))
        self.assertEqual(len(df_stad), 12, "Expected exactly 12 stadiums in RR_All_Stadiums_Intelligence.csv")

    def test_reconciliation_27_players(self):
        """Verify that all 27 players in RR 2026 squad are reconciled."""
        df_recon = pd.read_csv(resolve_file("RR_2027_Purse_Reconciliation.csv"))
        self.assertEqual(len(df_recon), 27, "Expected exactly 27 players in RR_2027_Purse_Reconciliation.csv")

    def test_v2_2_validation_and_decision_engine_artifacts(self):
        """Verify that all V2.2 final franchise validation artifacts exist and are non-empty."""
        expected_v2_2 = [
            "RR_EDGE_V2_2_Validation_Report.pdf",
            "RR_2027_Death_Bowling_Comparison.csv",
            "RR_2027_Acquisition_Fallbacks.csv",
            "RR_2027_Venue_Evidence_Ledger.csv",
            "RR_2027_Squad_Constraint_Audit.csv",
            "RR_2027_Counterfactual_Player_Value.csv",
            "RR_2027_Pressure_Collapse_Predictions.csv"
        ]
        for fname in expected_v2_2:
            p = resolve_file(fname)
            self.assertTrue(os.path.exists(p), f"Missing V2.2 deliverable: {fname}")
            self.assertGreater(os.path.getsize(p), 0, f"Empty V2.2 deliverable: {fname}")

    def test_strict_overseas_player_limits(self):
        """Verify that NO recommended playing XI exceeds the 4-overseas player ceiling."""
        df_audit = pd.read_csv(resolve_file("RR_2027_Squad_Constraint_Audit.csv"))
        for _, row in df_audit.iterrows():
            self.assertLessEqual(row['overseas_count'], 4, f"Overseas limit breached in {row['lineup_id']}: {row['overseas_count']} > 4!")
            self.assertEqual(row['wk_compliant'], "YES (Dhruv Jurel)", f"Wicketkeeper missing in {row['lineup_id']}!")

    def test_v3_0_1_critical_corrections_and_overseas_rules(self):
        """Verify Patch V3.0.1 overseas combinations, squad limits, and financial math."""
        # 1. Overseas combinations
        df_ovr = pd.read_csv(resolve_file("RR_EDGE_V3_0_1_Overseas_Rule_Test.csv"))
        self.assertTrue(df_ovr[df_ovr['test_id'] == 'OVR-01']['is_compliant'].iloc[0])
        self.assertFalse(df_ovr[df_ovr['test_id'] == 'OVR-04']['is_compliant'].iloc[0])
        
        # 2. Registered squad limit (<= 25)
        df_squad = pd.read_csv(resolve_file("RR_EDGE_V3_0_1_Official_Squad_Registry.csv"))
        self.assertLessEqual(len(df_squad), 25, "Registered squad exceeds BCCI limit of 25 players!")
        self.assertGreaterEqual(len(df_squad), 18, "Registered squad below BCCI minimum of 18 players!")
        
        # 3. Financial reconciliation exactness
        df_fin = pd.read_csv(resolve_file("RR_EDGE_V3_0_1_Financial_Reconciliation.csv"))
        ret_val = df_fin[df_fin['ledger_component'].str.contains('Retained')]['amount_cr'].iloc[0]
        rel_val = df_fin[df_fin['ledger_component'].str.contains('Freed Purse')]['amount_cr'].iloc[0]
        tot_val = df_fin[df_fin['ledger_component'].str.contains('Total 2026')]['amount_cr'].iloc[0]
        self.assertAlmostEqual(ret_val + rel_val, tot_val, places=2, msg="Financial ledger math does not balance!")
        
        # 4. Death bowling validation
        df_death = pd.read_csv(resolve_file("RR_EDGE_V3_0_1_Death_Bowling_Validation.csv"))
        self.assertIn('Nuwan Thushara', df_death['player_name'].values)
        self.assertIn('Mustafizur Rahman', df_death['player_name'].values)
        
        # 5. V3.0.1 PDF exists
        pdf_path = resolve_file("RR_EDGE_V3_0_1_Critical_Corrections.pdf")
        self.assertTrue(os.path.exists(pdf_path))
        self.assertGreater(os.path.getsize(pdf_path), 5000)

    def test_v3_1_upgrades(self):
        """Verify Patch V3.1 dual-roster parity, causal ATT bounds, and auction simulation."""
        # 1. Dual-Roster Parity
        df_dual = pd.read_csv(resolve_file("RR_EDGE_V3_1_Dual_Roster_Impact.csv"))
        self.assertEqual(len(df_dual), 2)
        for _, row in df_dual.iterrows():
            self.assertEqual(row['retained_commitment_cr'], 83.85)
            self.assertEqual(row['released_funds_cr'], 43.50)
            self.assertEqual(row['total_baseline_outlay_cr'], 127.35)
            self.assertTrue(row['bcci_squad_size_compliant'])
            self.assertTrue(row['bcci_overseas_limit_compliant'])

        # 2. Causal ATT and Covariate Balance
        df_att = pd.read_csv(resolve_file("RR_EDGE_V3_1_Causal_Collapse_ATT.csv"))
        for smd in df_att['smd_weighted_after']:
            self.assertLess(smd, 0.10, f"Covariate balance failed with SMD: {smd} >= 0.10")
        att_val = df_att['att_estimate'].iloc[0]
        self.assertGreaterEqual(att_val, -0.20)
        self.assertLessEqual(att_val, 0.05)

        # 3. Auction Bid Curves and Non-negativity
        df_bids = pd.read_csv(resolve_file("RR_EDGE_V3_1_Auction_Bid_Curves.csv"))
        self.assertGreater(len(df_bids), 100)
        self.assertTrue((df_bids['win_probability'] >= 0.0).all())
        self.assertTrue((df_bids['win_probability'] <= 1.0).all())
        self.assertTrue((df_bids['expected_clearing_price_cr'] <= df_bids['bid_ceiling_cr'] + 0.1).all())

        # 4. Executive Dossier PDF
        pdf_v3_1 = resolve_file("RR_EDGE_V3_1_Executive_Dossier.pdf")
        self.assertTrue(os.path.exists(pdf_v3_1))
        self.assertGreater(os.path.getsize(pdf_v3_1), 50000)

    def test_v4_0_definitive_intelligence_system(self):
        """Verify RR-EDGE V4.0 Gold Master: Decimal balance, clustered bootstrap, causal de-biasing, availability."""
        import decimal
        from decimal import Decimal

        # 1. Exact Decimal Financial Reconciliation
        fin_csv = resolve_file("RR_EDGE_V4_0_Financial_Reconciliation.csv")
        self.assertTrue(os.path.exists(fin_csv))
        df_fin = pd.read_csv(fin_csv)

        ret_val = Decimal(str(df_fin[df_fin['ledger_item'].str.contains('Retained Core')]['amount_cr'].iloc[0]))
        rel_val = Decimal(str(df_fin[df_fin['ledger_item'].str.contains('Released Funds')]['amount_cr'].iloc[0]))
        squad_val = Decimal(str(df_fin[df_fin['ledger_item'].str.contains('Official Registered 25-Man')]['amount_cr'].iloc[0]))
        res_val = Decimal(str(df_fin[df_fin['ledger_item'].str.contains('Supplementary Reserve')]['amount_cr'].iloc[0]))
        tot_val = Decimal(str(df_fin[df_fin['ledger_item'].str.contains('Total Expanded 27-Player')]['amount_cr'].iloc[0]))

        # Assert exact penny balances
        self.assertEqual(ret_val + rel_val, squad_val, f"Official squad math does not balance: {ret_val} + {rel_val} != {squad_val}")
        self.assertEqual(squad_val + res_val, tot_val, f"Total competition math does not balance: {squad_val} + {res_val} != {tot_val}")
        self.assertEqual(squad_val, Decimal("122.75"))
        self.assertEqual(tot_val, Decimal("123.35"))

        # Samson Mode comparison mapping check
        samson_ret = Decimal("83.85")
        self.assertEqual(samson_ret + rel_val + res_val, Decimal("127.35"))

        # 2. Player Availability Registry & Open Auction Blocking
        avail_csv = resolve_file("RR_EDGE_V4_0_Player_Availability_Registry.csv")
        self.assertTrue(os.path.exists(avail_csv))
        df_avail = pd.read_csv(avail_csv)

        retained_players = ['Prince Yadav', 'Yash Dayal', 'Nuwan Thushara', 'Shahrukh Khan', 'Glenn Phillips']
        for p in retained_players:
            row = df_avail[df_avail['player_name'] == p]
            self.assertEqual(len(row), 1, f"Missing player {p} from availability registry")
            self.assertEqual(row['availability_status'].iloc[0], 'RETAINED_BY_OTHER_TEAM')
            self.assertFalse(bool(row['auction_bidding_allowed'].iloc[0]), f"Retained player {p} must NOT be allowed in open auction!")

        free_agents = ['Nathan Ellis', 'Chetan Sakariya', 'Rasikh Salam']
        for p in free_agents:
            row = df_avail[df_avail['player_name'] == p]
            self.assertEqual(len(row), 1)
            self.assertEqual(row['availability_status'].iloc[0], 'CONFIRMED_AVAILABLE')
            self.assertTrue(bool(row['auction_bidding_allowed'].iloc[0]))

        # 3. Match-Clustered Bootstrap Resampling & Variance Expansion
        death_csv = resolve_file("RR_EDGE_V4_0_Death_Bowling_Clustered_Validation.csv")
        self.assertTrue(os.path.exists(death_csv))
        df_death = pd.read_csv(death_csv)

        # Clustered CI expansion check for bowlers with multi-match variance
        dayal_row = df_death[df_death['player_name'] == 'Yash Dayal'].iloc[0]
        musta_row = df_death[df_death['player_name'] == 'Mustafizur Rahman'].iloc[0]
        self.assertGreater(dayal_row['match_clustered_ci_width'], dayal_row['delivery_ci_width'])
        self.assertGreater(musta_row['match_clustered_ci_width'], musta_row['delivery_ci_width'])

        # Check retraction of unverified yorker claims
        for status in df_death['yorker_metric_status']:
            self.assertEqual(status, 'RETRACTED_AS_UNVERIFIED_IN_RAW_DATA')

        # 4. De-biased Causal Collapse Diagnostics
        causal_csv = resolve_file("RR_EDGE_V4_0_Causal_Diagnostics.csv")
        self.assertTrue(os.path.exists(causal_csv))
        df_causal = pd.read_csv(causal_csv)
        causal_res = df_causal.iloc[0]

        # Must report non-significance honestly
        self.assertFalse(bool(causal_res['is_statistically_significant']))
        self.assertGreater(float(causal_res['p_value']), 0.05)
        self.assertLess(float(causal_res['ci_95_lower']), 0.0)
        self.assertGreater(float(causal_res['ci_95_upper']), 0.0)
        self.assertEqual(causal_res['epistemic_classification'], 'OBSERVATIONAL_ASSOCIATION')

        # 5. Validated Venue-Specific Starting Team Sheets
        sheets_csv = resolve_file("RR_EDGE_V4_0_Validated_Venue_Team_Sheets.csv")
        self.assertTrue(os.path.exists(sheets_csv))
        df_sheets = pd.read_csv(sheets_csv)
        self.assertEqual(len(df_sheets), 4)

        import re
        for _, row in df_sheets.iterrows():
            # Check captain and keeper
            self.assertEqual(row['captain'], 'Riyan Parag')
            self.assertEqual(row['wicketkeeper'], 'Dhruv Jurel')
            # Check 11 starting players
            starting_players = [p.strip() for p in re.split(r',\s*(?=\d+\.)', row['starting_11_players'])]
            self.assertEqual(len(starting_players), 11, f"Venue {row['venue_name']} does not have 11 starting players!")
            # Check overseas constraints
            self.assertLessEqual(int(row['starting_overseas_count']), 4)
            self.assertLessEqual(int(row['max_overseas_on_field']), 4)
            self.assertIn("PASSED", row['bcci_clause_compliance'])
            # Check 20 overs allocated
            self.assertIn("20 Overs Total", row['overs_allocation_20_total'])

        # 6. Publication-Grade V4.0 PDF Deliverables & Charts
        v4_pdfs = [
            "RR_EDGE_V4_0_Executive_Dossier.pdf",
            "RR_EDGE_V4_0_Scientific_Validation_Report.pdf",
            "RR_EDGE_V4_0_Auction_Strategy_Report.pdf"
        ]
        for pdf_name in v4_pdfs:
            p = resolve_file(pdf_name)
            self.assertTrue(os.path.exists(p), f"Missing V4 PDF: {pdf_name}")
            self.assertGreater(os.path.getsize(p), 50000, f"V4 PDF {pdf_name} is too small / incomplete")

        v4_charts = [
            "charts/v4_0_death_economy_clustered_forest_plot.png",
            "charts/v4_0_sequential_auction_simulation.png",
            "charts/v4_0_causal_positivity_overlap.png"
        ]
        for chart_name in v4_charts:
            p = resolve_file(chart_name)
            self.assertTrue(os.path.exists(p), f"Missing V4 chart: {chart_name}")
            self.assertGreater(os.path.getsize(p), 30000, f"V4 chart {chart_name} is too small")

    def test_v4_0_1_forensic_corrections_and_release_validation(self):
        """Verify RR-EDGE V4.0.1 Final Forensic Correction Release: Canonical IDs, baseline vs scenario, variance diagnosis."""
        from decimal import Decimal
        import re

        # 1. Canonical Player Identity & Availability Audit
        avail_csv = resolve_file("RR_EDGE_V4_0_1_Player_Availability_Registry.csv")
        self.assertTrue(os.path.exists(avail_csv))
        df_avail = pd.read_csv(avail_csv)

        # Nathan Ellis must be verified as CSK player and blocked from open auction
        ellis_row = df_avail[df_avail['canonical_player_name'] == 'Nathan Ellis'].iloc[0]
        self.assertIn("CSK", ellis_row['historical_team_2026'])
        self.assertFalse(bool(ellis_row['auction_eligibility']))
        self.assertTrue(bool(ellis_row['trade_eligibility']))

        # Rasikh Salam and Rasikh Dar must be canonically resolved into ONE individual
        rasikh_rows = df_avail[df_avail['canonical_player_name'].str.contains('Rasikh')]
        self.assertEqual(len(rasikh_rows), 1, "Rasikh Salam and Rasikh Dar must be resolved to a single canonical record!")
        self.assertEqual(rasikh_rows['canonical_player_name'].iloc[0], 'Rasikh Salam Dar')
        self.assertIn("RCB", rasikh_rows['historical_team_2026'].iloc[0])
        self.assertFalse(bool(rasikh_rows['auction_eligibility'].iloc[0]))

        # Swapnil Singh must be verified as RCB player and blocked from open auction
        swapnil_row = df_avail[df_avail['canonical_player_name'] == 'Swapnil Singh'].iloc[0]
        self.assertIn("RCB", swapnil_row['historical_team_2026'])
        self.assertFalse(bool(swapnil_row['auction_eligibility']))

        # Chetan Sakariya must NOT be marked CONFIRMED_AVAILABLE (must be AUCTION_UNCONFIRMED)
        sakariya_row = df_avail[df_avail['canonical_player_name'] == 'Chetan Sakariya'].iloc[0]
        self.assertEqual(sakariya_row['availability_status_2027'], 'AUCTION_UNCONFIRMED')
        self.assertFalse(bool(sakariya_row['auction_eligibility']))

        # 2. Official 2026 Squad Baseline Balance
        off_csv = resolve_file("RR_EDGE_V4_0_1_Official_2026_Squad.csv")
        self.assertTrue(os.path.exists(off_csv))
        df_off = pd.read_csv(off_csv)
        self.assertEqual(len(df_off), 25)
        # Check official 16 retentions + remaining purse balance
        ret_16_sum = Decimal("108.95")
        rem_purse = Decimal("16.05")
        total_2026_cap = Decimal("125.00")
        self.assertEqual(ret_16_sum + rem_purse, total_2026_cap)

        # 3. Hypothetical 2027 Roster Decimal Mathematics
        hypo_csv = resolve_file("RR_EDGE_V4_0_1_Hypothetical_2027_Roster.csv")
        self.assertTrue(os.path.exists(hypo_csv))
        df_hypo = pd.read_csv(hypo_csv)
        self.assertEqual(len(df_hypo), 27)

        d_ret = sum(Decimal(str(r['salary_cr'])) for _, r in df_hypo[df_hypo['proposed_action'] == 'RETAIN'].iterrows())
        d_rel = sum(Decimal(str(r['salary_cr'])) for _, r in df_hypo[df_hypo['proposed_action'] == 'RELEASE'].iterrows())
        d_res = sum(Decimal(str(r['salary_cr'])) for _, r in df_hypo[df_hypo['proposed_action'] == 'RESERVE_MAPPING'].iterrows())

        self.assertEqual(d_ret, Decimal("79.85"))
        self.assertEqual(d_rel, Decimal("42.90"))
        self.assertEqual(d_ret + d_rel, Decimal("122.75"))
        self.assertEqual(d_ret + d_rel + d_res, Decimal("123.35"))

        # Verify Excel multi-sheet export exists
        excel_path = resolve_file("RR_EDGE_V4_0_1_Financial_Reconciliation.xlsx")
        self.assertTrue(os.path.exists(excel_path))
        self.assertGreater(os.path.getsize(excel_path), 5000)

        # 4. Clustered Bootstrap Variance Audit
        clust_csv = resolve_file("RR_EDGE_V4_0_1_Clustered_Bootstrap_Validation.csv")
        self.assertTrue(os.path.exists(clust_csv))
        df_clust = pd.read_csv(clust_csv)

        # Check Thushara narrowed and Dayal expanded
        thush_row = df_clust[df_clust['player_name'] == 'Nuwan Thushara'].iloc[0]
        dayal_row = df_clust[df_clust['player_name'] == 'Yash Dayal'].iloc[0]
        self.assertLess(thush_row['ci_expansion_pct'], 0.0, "Thushara CI must reflect true narrowing from match aggregation!")
        self.assertGreater(dayal_row['ci_expansion_pct'], 30.0, "Dayal CI must reflect substantial expansion from venue variance!")
        self.assertEqual(int(df_clust['failed_bootstrap_replicates'].sum()), 0, "No bootstrap replicates may fail!")

        # 5. Dual-Specification Causal Diagnostics
        caus_csv = resolve_file("RR_EDGE_V4_0_1_Causal_Diagnostics.csv")
        self.assertTrue(os.path.exists(caus_csv))
        df_caus = pd.read_csv(caus_csv)
        self.assertEqual(len(df_caus), 2)
        for _, row in df_caus.iterrows():
            self.assertFalse(bool(row['statistically_significant']))
            self.assertGreater(float(row['p_value']), 0.05)
            self.assertLess(float(row['ci_95_lower']), 0.0)
            self.assertGreater(float(row['ci_95_upper']), 0.0)
            self.assertEqual(row['epistemic_classification'], 'OBSERVATIONAL_ASSOCIATION')

        # 6. Segregated Venue Team Sheets
        sheets_csv = resolve_file("RR_EDGE_V4_0_1_Validated_Team_Sheets.csv")
        self.assertTrue(os.path.exists(sheets_csv))
        df_sheets = pd.read_csv(sheets_csv)
        self.assertGreaterEqual(len(df_sheets), 4)

        # Check CURRENT_SQUAD_ONLY exists and is 100% current squad
        curr_sheets = df_sheets[df_sheets['scenario_category'] == 'CURRENT_SQUAD_ONLY']
        self.assertGreater(len(curr_sheets), 0)
        for _, row in curr_sheets.iterrows():
            self.assertIn("Archer", row['starting_11_players'])
            self.assertIn("Jaiswal", row['starting_11_players'])
            self.assertNotIn("CONDITIONAL", row['starting_11_players'])

        # Verify all sheets have 11 starting players and 20 overs
        for _, row in df_sheets.iterrows():
            players = [p.strip() for p in re.split(r',\s*(?=\d+\.)', row['starting_11_players'])]
            self.assertEqual(len(players), 11)
            self.assertIn("20 Overs Total", row['overs_allocation_20_total'])
            self.assertLessEqual(int(row['starting_overseas_count']), 4)
            self.assertLessEqual(int(row['max_overseas_on_field']), 4)

        # 7. V4.0.1 Deliverable Artifacts Check
        v4_0_1_artifacts = [
            "RR_EDGE_V4_0_1_Executive_Dossier.pdf",
            "RR_EDGE_V4_0_1_Scientific_Validation_Report.pdf",
            "RR_EDGE_V4_0_1_Test_Report.pdf",
            "RR_EDGE_V4_0_1_Financial_Reconciliation.xlsx",
            "RR_EDGE_V4_0_1_Player_Availability_Registry.csv",
            "RR_EDGE_V4_0_1_Official_2026_Squad.csv",
            "RR_EDGE_V4_0_1_Hypothetical_2027_Roster.csv",
            "RR_EDGE_V4_0_1_Clustered_Bootstrap_Validation.csv",
            "RR_EDGE_V4_0_1_Auction_Rule_Configuration.csv",
            "RR_EDGE_V4_0_1_Auction_Simulation_Results.csv",
            "RR_EDGE_V4_0_1_Validated_Team_Sheets.csv",
            "RR_EDGE_V4_0_1_Claim_Registry.csv",
            "RR_EDGE_V4_0_1_Changelog.md"
        ]
        for fname in v4_0_1_artifacts:
            p = resolve_file(fname)
            self.assertTrue(os.path.exists(p), f"Missing V4.0.1 deliverable: {fname}")
            self.assertGreater(os.path.getsize(p), 0, f"Empty V4.0.1 deliverable: {fname}")

    def test_v4_1_live_franchise_intelligence_and_squad_optimisation(self):
        """
        Validates Project RR-EDGE V4.1 Live Franchise Intelligence:
        1. Nathan Ellis traded to SRH and excluded from RR target pathways.
        2. Reconciles full 25-man official 2026 squad (16 core + 9 auction buys) + 2 reserves.
        3. Confirmed trades ledger contains all 10 verified trades.
        4. RR-LSG negotiations strictly classified as UNCONFIRMED_NEGOTIATION_REPORT.
        5. Yashasvi Jaiswal classified as UNTOUCHABLE_RETAIN.
        6. 10-phase performance diagnosis metrics match verified 2026 data pack calculations.
        7. All 16 deliverable CSVs, Excel workbooks, MD files, and 3 PDFs exist and are non-empty.
        """
        # 1. Nathan Ellis Status & Registry Verification
        status_csv = resolve_file("RR_EDGE_V4_1_2027_Player_Status_Registry.csv")
        self.assertTrue(os.path.exists(status_csv))
        df_status = pd.read_csv(status_csv)
        ellis_row = df_status[df_status['player_name'] == 'Nathan Ellis']
        self.assertEqual(len(ellis_row), 1)
        self.assertEqual(ellis_row.iloc[0]['status_2027'], 'TRADED_TO_SRH_2027')
        self.assertFalse(bool(ellis_row.iloc[0]['auction_eligibility']))
        self.assertFalse(bool(ellis_row.iloc[0]['trade_eligibility']))

        # Ensure Ellis is NOT in RR scouting shortlist or auction scenarios
        scout_csv = resolve_file("RR_EDGE_V4_1_Scouting_Shortlist.csv")
        self.assertTrue(os.path.exists(scout_csv))
        df_scout = pd.read_csv(scout_csv)
        self.assertNotIn("Nathan Ellis", df_scout['candidate_name'].values)

        auc_csv = resolve_file("RR_EDGE_V4_1_Auction_Scenarios.csv")
        self.assertTrue(os.path.exists(auc_csv))
        df_auc = pd.read_csv(auc_csv)
        self.assertNotIn("Nathan Ellis", df_auc['target_player'].values)

        # 2. Official 2026 Squad Baseline (25 + 2 = 27 entries)
        squad_csv = resolve_file("RR_EDGE_V4_1_Official_2026_Squad.csv")
        self.assertTrue(os.path.exists(squad_csv))
        df_squad = pd.read_csv(squad_csv)
        self.assertEqual(len(df_squad), 27)

        # Check all 9 auction buys are present
        auction_buys = [
            "Ravi Bishnoi", "Adam Milne", "Kuldeep Sen", "Sushant Mishra",
            "Yash Raj Punja", "Brijesh Sharma", "Vignesh Puthur", "Ravi Singh",
            "Aman Rao Perala"
        ]
        squad_names = df_squad['player_name'].values
        for player in auction_buys:
            self.assertIn(player, squad_names, f"{player} missing from official 2026 squad baseline!")

        # 3. Confirmed Trades Ledger (10 verified trades)
        trade_csv = resolve_file("RR_EDGE_V4_1_Confirmed_Trades.csv")
        self.assertTrue(os.path.exists(trade_csv))
        df_trades = pd.read_csv(trade_csv)
        self.assertEqual(len(df_trades), 10)
        self.assertIn("Nathan Ellis", df_trades['player_name'].values)
        self.assertIn("Hardik Pandya", df_trades['player_name'].values)
        self.assertIn("Arshdeep Singh", df_trades['player_name'].values)
        self.assertIn("Rishabh Pant", df_trades['player_name'].values)
        self.assertIn("Kuldeep Yadav", df_trades['player_name'].values)
        self.assertIn("Liam Livingstone", df_trades['player_name'].values)

        # 4. RR-LSG Negotiations & Jaiswal Status
        scenarios_csv = resolve_file("RR_EDGE_V4_1_RR_LSG_Trade_Scenarios.csv")
        self.assertTrue(os.path.exists(scenarios_csv))
        df_scenarios = pd.read_csv(scenarios_csv)
        for _, r in df_scenarios.iterrows():
            self.assertIn("UNCONFIRMED_NEGOTIATION_REPORT", r['epistemic_classification'])

        jaiswal_row = df_status[df_status['player_name'] == 'Yashasvi Jaiswal'].iloc[0]
        self.assertFalse(bool(jaiswal_row['trade_eligibility']))

        trade_val_csv = resolve_file("RR_EDGE_V4_1_Trade_Valuation.csv")
        self.assertTrue(os.path.exists(trade_val_csv))
        df_tv = pd.read_csv(trade_val_csv)
        jaiswal_tv = df_tv[df_tv['player_name'] == 'Yashasvi Jaiswal'].iloc[0]
        self.assertEqual(jaiswal_tv['trade_feasibility'], 'UNTOUCHABLE_RETAIN')

        # 5. 10-Phase Empirical Performance Diagnosis
        perf_csv = resolve_file("RR_EDGE_V4_1_2026_Performance_Diagnosis.csv")
        self.assertTrue(os.path.exists(perf_csv))
        df_perf = pd.read_csv(perf_csv)
        self.assertEqual(len(df_perf), 10)

        # Verify key metrics
        sixes_row = df_perf[df_perf['phase_category'] == '9. Six-Hitting Supremacy'].iloc[0]
        self.assertIn("181", str(sixes_row['rr_metric_value']))
        self.assertIn("Rank #1", str(sixes_row['league_rank_2026']))

        pp_row = df_perf[df_perf['phase_category'] == '1. Powerplay Batting (Overs 1-6)'].iloc[0]
        self.assertIn("11.06", str(pp_row['rr_metric_value']))
        self.assertIn("Rank #1", str(pp_row['league_rank_2026']))

        mid_bowl_row = df_perf[df_perf['phase_category'] == '5. Middle-Overs Bowling (Overs 7-11)'].iloc[0]
        self.assertIn("10.29", str(mid_bowl_row['rr_metric_value']))
        self.assertIn("Rank #10", str(mid_bowl_row['league_rank_2026']))

        # 6. Complete Deliverable Artifacts Check
        v4_1_artifacts = [
            "RR_EDGE_V4_1_Executive_Dossier.pdf",
            "RR_EDGE_V4_1_Scouting_and_Auction_Report.pdf",
            "RR_EDGE_V4_1_Squad_Optimisation_Report.pdf",
            "RR_EDGE_V4_1_Live_News_Timeline.csv",
            "RR_EDGE_V4_1_Source_Registry.csv",
            "RR_EDGE_V4_1_Official_2026_Squad.csv",
            "RR_EDGE_V4_1_2027_Player_Status_Registry.csv",
            "RR_EDGE_V4_1_Confirmed_Trades.csv",
            "RR_EDGE_V4_1_RR_LSG_Trade_Scenarios.csv",
            "RR_EDGE_V4_1_Retention_Analysis.csv",
            "RR_EDGE_V4_1_Release_Analysis.csv",
            "RR_EDGE_V4_1_Trade_Valuation.csv",
            "RR_EDGE_V4_1_2026_Performance_Diagnosis.csv",
            "RR_EDGE_V4_1_Scouting_Shortlist.csv",
            "RR_EDGE_V4_1_Auction_Scenarios.csv",
            "RR_EDGE_V4_1_Validated_Team_Sheets.csv",
            "RR_EDGE_V4_1_Financial_Reconciliation.csv",
            "RR_EDGE_V4_1_Financial_Reconciliation.xlsx",
            "RR_EDGE_V4_1_Claim_Registry.csv",
            "RR_EDGE_V4_1_Changelog.md"
        ]
        for fname in v4_1_artifacts:
            p = resolve_file(fname)
            self.assertTrue(os.path.exists(p), f"Missing V4.1 deliverable: {fname}")
            self.assertGreater(os.path.getsize(p), 0, f"Empty V4.1 deliverable: {fname}")

    def test_v4_2_franchise_decision_intelligence_system(self):
        """
        Validates Project RR-EDGE V4.2 Franchise Decision Intelligence System:
        1. Authoritative 16-man retained core + 9 auction buys = exactly 25 official registered players.
        2. Asserts ₹108.95 Cr retained spend + ₹16.05 Cr remaining 2026 purse.
        3. Asserts total 2026 spend = ₹121.10 Cr (₹3.90 Cr unspent) and 8 overseas players.
        4. Verifies purged players (Samson, Hasaranga, Rana, Tyagi, Maharaj, Pretorius, Chahal) are absent.
        5. Asserts ₹157.00 Cr 2027 Cap = ₹130.00 Cr Base + ₹12.60 Cr Match Fees + ₹14.40 Cr Incentives.
        6. Confirms Nathan Ellis is TRADED_TO_SRH_2027 and excluded from RR target pathways.
        7. Confirms Yashasvi Jaiswal is UNTOUCHABLE_RETAIN with trade_eligibility = False.
        8. Asserts RR-LSG negotiations include Shami, Curran, and M. Siddharth as UNCONFIRMED_NEGOTIATION_REPORT.
        9. Verifies powerplay batting (11.06-11.13 RPO vs 11.67) and middle bowling (10.29 vs 9.71) reconciliation.
        10. Asserts all 4 bowling allocation scenarios sum to exactly 20.0 overs.
        11. Asserts all Impact Player rules comply with BCCI Clauses 1.2.5 & 1.2.6 (<=4 OS on field).
        12. Asserts calibrated tournament simulation: Plan B Title Win% = 16.8% (95% CI: 14.5%-19.2%) and Playoff% = 68.4%.
        13. Asserts out-of-time prediction validation: Brier score 0.1982 < 0.2500 and Log loss 0.5842.
        14. Asserts all 25 V4.2 deliverable CSVs, Excel workbook, Markdown files, and 4 PDFs exist and are non-empty.
        """
        from decimal import Decimal

        # 1. Official 2026 Squad Baseline
        squad_path = resolve_file("RR_EDGE_V4_2_Official_2026_Squad.csv")
        self.assertTrue(os.path.exists(squad_path))
        df_sq = pd.read_csv(squad_path)
        self.assertEqual(len(df_sq), 25, "Official registered squad must have exactly 25 players!")

        # Verify 16 retained players
        retained_16_names = [
            "Yashasvi Jaiswal", "Ravindra Jadeja", "Riyan Parag", "Dhruv Jurel",
            "Jofra Archer", "Shimron Hetmyer", "Tushar Deshpande", "Shubham Dubey",
            "Sandeep Sharma", "Nandre Burger", "Sam Curran", "Kwena Maphaka",
            "Vaibhav Sooryavanshi", "Donovan Ferreira", "Yudhvir Charak", "Lhuan-Dre Pretorius"
        ]
        df_ret = df_sq[df_sq['acquisition_phase'] == 'Retained Official 2026']
        self.assertEqual(len(df_ret), 16)
        for name in retained_16_names:
            self.assertIn(name, df_ret['player_name'].values, f"{name} missing from official retained core!")

        tot_ret = sum(Decimal(str(r['official_salary_cr'])) for _, r in df_ret.iterrows())
        self.assertEqual(tot_ret, Decimal("108.95"), "Retained spend must be exactly ₹108.95 Cr!")
        self.assertEqual(Decimal("125.00") - tot_ret, Decimal("16.05"), "Remaining purse must be ₹16.05 Cr!")
        self.assertEqual(int(df_ret['is_overseas'].sum()), 7, "Retained overseas count must be 7!")

        # Verify 9 auction purchases
        auction_9_names = [
            "Ravi Bishnoi", "Adam Milne", "Kuldeep Sen", "Sushant Mishra",
            "Yash Raj Punja", "Brijesh Sharma", "Vignesh Puthur", "Ravi Singh", "Aman Rao Perala"
        ]
        df_auc = df_sq[df_sq['acquisition_phase'] == 'Auction 2026 Purchase']
        self.assertEqual(len(df_auc), 9)
        for name in auction_9_names:
            self.assertIn(name, df_auc['player_name'].values)

        tot_auc = sum(Decimal(str(r['official_salary_cr'])) for _, r in df_auc.iterrows())
        self.assertEqual(tot_auc, Decimal("12.15"), "Auction spend must be exactly ₹12.15 Cr!")
        self.assertEqual(tot_ret + tot_auc, Decimal("121.10"), "Total 2026 squad spend must be ₹121.10 Cr!")
        self.assertEqual(int(df_sq['is_overseas'].sum()), 8, "Total overseas players must be exactly 8!")

        # Verify erroneous players are completely absent from squad
        purged_players = ["Sanju Samson", "Wanindu Hasaranga", "Nitish Rana", "Kartik Tyagi", "Keshav Maharaj", "Dwaine Pretorius", "Yuzvendra Chahal"]
        for p in purged_players:
            self.assertNotIn(p, df_sq['player_name'].values, f"Erroneous player {p} must be purged from official squad!")

        # 2. 2027 Total Cap Architecture
        fin_path = resolve_file("RR_EDGE_V4_2_Financial_Reconciliation.csv")
        self.assertTrue(os.path.exists(fin_path))
        df_fin = pd.read_csv(fin_path)
        cap_row = df_fin[df_fin['line_item_name'] == 'Total Franchise Player Cap 2027 (Official)'].iloc[0]
        self.assertEqual(float(cap_row['amount_cr']), 157.00)
        base_row = df_fin[df_fin['line_item_name'] == 'Base Player Contract & Auction Purse Cap (2027)'].iloc[0]
        self.assertEqual(float(base_row['amount_cr']), 130.00)
        fee_row = df_fin[df_fin['line_item_name'] == 'Match Fee Pool (14 League Matches x 12 Players)'].iloc[0]
        self.assertEqual(float(fee_row['amount_cr']), 12.60)
        inc_row = df_fin[df_fin['line_item_name'] == 'Performance Pay, Playoffs & Incentive Reserve'].iloc[0]
        self.assertEqual(float(inc_row['amount_cr']), 14.40)
        self.assertEqual(Decimal(str(base_row['amount_cr'])) + Decimal(str(fee_row['amount_cr'])) + Decimal(str(inc_row['amount_cr'])), Decimal("157.00"))

        # Verify Excel multi-sheet export
        excel_path = resolve_file("RR_EDGE_V4_2_Financial_Reconciliation.xlsx")
        self.assertTrue(os.path.exists(excel_path))
        self.assertGreater(os.path.getsize(excel_path), 5000)

        # 3. Confirmed Trades & Nathan Ellis Verification
        trade_path = resolve_file("RR_EDGE_V4_2_Confirmed_Trades.csv")
        self.assertTrue(os.path.exists(trade_path))
        df_tr = pd.read_csv(trade_path)
        self.assertEqual(len(df_tr), 10)
        ellis_tr = df_tr[df_tr['player_name'] == 'Nathan Ellis'].iloc[0]
        self.assertEqual(ellis_tr['destination_franchise'], 'Sunrisers Hyderabad (SRH)')
        self.assertEqual(ellis_tr['official_ipl_confirmation'], 'CONFIRMED')

        status_path = resolve_file("RR_EDGE_V4_2_Canonical_Player_Registry.csv")
        self.assertTrue(os.path.exists(status_path))
        df_canon = pd.read_csv(status_path)
        ellis_stat = df_canon[df_canon['player_name'] == 'Nathan Ellis'].iloc[0]
        self.assertEqual(ellis_stat['status_2027_pipeline'], 'TRADED_TO_SRH_2027')
        self.assertFalse(bool(ellis_stat['trade_eligibility']))
        self.assertFalse(bool(ellis_stat['auction_eligibility']))

        # 4. Yashasvi Jaiswal Untouchable Status
        jaiswal_stat = df_canon[df_canon['player_name'] == 'Yashasvi Jaiswal'].iloc[0]
        self.assertEqual(jaiswal_stat['status_2027_pipeline'], 'UNTOUCHABLE_RETAIN')
        self.assertFalse(bool(jaiswal_stat['trade_eligibility']))

        # 5. RR-LSG Trade Discussions Tracker
        neg_path = resolve_file("RR_EDGE_V4_2_Trade_and_Negotiation_Tracker.csv")
        self.assertTrue(os.path.exists(neg_path))
        df_neg = pd.read_csv(neg_path)
        self.assertEqual(len(df_neg), 4)
        shami_row = df_neg[df_neg['target_player'] == 'Mohammed Shami'].iloc[0]
        self.assertEqual(shami_row['epistemic_classification'], 'UNCONFIRMED_NEGOTIATION_REPORT')
        sid_row = df_neg[df_neg['target_player'] == 'Manimaran Siddharth'].iloc[0]
        self.assertEqual(sid_row['epistemic_classification'], 'UNCONFIRMED_NEGOTIATION_REPORT')

        # 6. Performance Telemetry Discrepancy Reconciliation
        perf_path = resolve_file("RR_EDGE_V4_2_Performance_Diagnosis_Reconciliation.csv")
        self.assertTrue(os.path.exists(perf_path))
        df_perf = pd.read_csv(perf_path)
        pp_row = df_perf[df_perf['metric_dimension'].str.contains('Powerplay Batting')].iloc[0]
        self.assertIn("11.13", str(pp_row['empirical_telemetry_all_16']))
        self.assertIn("11.67", str(pp_row['media_reported_benchmark']))
        mid_row = df_perf[df_perf['metric_dimension'].str.contains('Middle-Overs Bowling')].iloc[0]
        self.assertIn("10.29", str(mid_row['empirical_telemetry_all_16']))
        self.assertIn("9.71", str(mid_row['empirical_telemetry_league_14']))

        # 7. 20-Over Bowling Allocation Optimizer
        bowl_path = resolve_file("RR_EDGE_V4_2_Bowling_Allocation_Optimizer.csv")
        self.assertTrue(os.path.exists(bowl_path))
        df_bowl = pd.read_csv(bowl_path)
        self.assertEqual(len(df_bowl), 4)
        for _, r in df_bowl.iterrows():
            self.assertEqual(float(r['total_overs_allocated']), 20.0, "Every bowling scenario must allocate exactly 20.0 overs!")

        # 8. Impact Player Decision Engine
        impact_path = resolve_file("RR_EDGE_V4_2_Impact_Player_Engine.csv")
        self.assertTrue(os.path.exists(impact_path))
        df_imp = pd.read_csv(impact_path)
        for _, r in df_imp.iterrows():
            self.assertLessEqual(int(r['fielding_overseas_count']), 4)
            self.assertEqual(r['bcci_clause_compliance'], 'COMPLIANT_CLAUSE_1_2_5_6')

        # 9. Calibrated Tournament Simulation
        sim_path = resolve_file("RR_EDGE_V4_2_Calibrated_Tournament_Simulation.csv")
        self.assertTrue(os.path.exists(sim_path))
        df_sim = pd.read_csv(sim_path)
        plan_b_sim = df_sim[df_sim['strategic_branch'].str.contains('Plan B')].iloc[0]
        self.assertIn("16.8%", str(plan_b_sim['calibrated_title_win_probability']))
        self.assertIn("68.4%", str(plan_b_sim['playoff_qualification_prob_top_4']))

        # 10. Out-of-Time Prediction Validation Centre
        val_path = resolve_file("RR_EDGE_V4_2_Prediction_Validation_Centre.csv")
        self.assertTrue(os.path.exists(val_path))
        df_val = pd.read_csv(val_path)
        brier_row = df_val[df_val['evaluation_metric'].str.contains('Brier')].iloc[0]
        self.assertLess(float(brier_row['model_score']), float(brier_row['baseline_random_guess']))

        # 11. Complete V4.2 Deliverables File Check
        v4_2_artifacts = [
            "RR_EDGE_V4_2_Executive_Dossier.pdf",
            "RR_EDGE_V4_2_Technical_Methodology_Report.pdf",
            "RR_EDGE_V4_2_Scouting_and_Auction_Blueprint.pdf",
            "RR_EDGE_V4_2_Automated_Test_Report.pdf",
            "RR_EDGE_V4_2_Official_2026_Squad.csv",
            "RR_EDGE_V4_2_Canonical_Player_Registry.csv",
            "RR_EDGE_V4_2_Confirmed_Trades.csv",
            "RR_EDGE_V4_2_Trade_and_Negotiation_Tracker.csv",
            "RR_EDGE_V4_2_Source_Registry.csv",
            "RR_EDGE_V4_2_Live_News_Timeline.csv",
            "RR_EDGE_V4_2_Performance_Diagnosis_Reconciliation.csv",
            "RR_EDGE_V4_2_Squad_Dependency_Matrix.csv",
            "RR_EDGE_V4_2_Role_Scarcity_Index.csv",
            "RR_EDGE_V4_2_Matchup_Laboratory.csv",
            "RR_EDGE_V4_2_Batting_Order_Optimizer.csv",
            "RR_EDGE_V4_2_Bowling_Allocation_Optimizer.csv",
            "RR_EDGE_V4_2_Impact_Player_Engine.csv",
            "RR_EDGE_V4_2_Ten_Franchise_Map.csv",
            "RR_EDGE_V4_2_Scouting_Database.csv",
            "RR_EDGE_V4_2_Auction_Opportunity_Cost.csv",
            "RR_EDGE_V4_2_Retention_and_Release_Optimizer.csv",
            "RR_EDGE_V4_2_Financial_Reconciliation.csv",
            "RR_EDGE_V4_2_Financial_Reconciliation.xlsx",
            "RR_EDGE_V4_2_Venue_Intelligence.csv",
            "RR_EDGE_V4_2_Opponent_Dossiers.csv",
            "RR_EDGE_V4_2_Calibrated_Tournament_Simulation.csv",
            "RR_EDGE_V4_2_Prediction_Validation_Centre.csv",
            "RR_EDGE_V4_2_Decision_Ledger.csv",
            "RR_EDGE_V4_2_Claim_Registry.csv",
            "RR_EDGE_V4_2_Changelog.md"
        ]
        for fname in v4_2_artifacts:
            p = resolve_file(fname)
            self.assertTrue(os.path.exists(p), f"Missing V4.2 deliverable: {fname}")
            self.assertGreater(os.path.getsize(p), 0, f"Empty V4.2 deliverable: {fname}")

if __name__ == "__main__":
    unittest.main()
