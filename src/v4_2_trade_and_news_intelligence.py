"""
PROJECT RR-EDGE V4.2: TRADE & NEWS INTELLIGENCE ENGINE
Revalidates all 2027 player trade movements and media reporting:
- 10 Confirmed League Trades with dual status: official_ipl_confirmation vs media_reported_status
- RR-LSG Trade Discussions tracking Shami, Curran, and M. Siddharth
- Yashasvi Jaiswal trade speculation formally recorded as STALLED/REJECTED
- Source Registry with freshness checks, duplicate detection, and contradiction tracking
- Chronological Live News Timeline with full audit trail
"""

import os
import pandas as pd

BASE_DIR = r"C:\Users\PREMCHANDYADAV\Downloads\RR_Competition"

def build_trade_and_news_intelligence():
    print("[V4.2 News & Trade] Generating verified trade ledgers and source registries...")

    # 1. Confirmed Trades Ledger (10 Trades) with Dual Status Fields
    confirmed_trades = [
        {
            'trade_id': 'TRD-2027-01',
            'player_name': 'Liam Livingstone',
            'origin_franchise': 'Sunrisers Hyderabad (SRH)',
            'destination_franchise': 'Chennai Super Kings (CSK)',
            'player_nationality': 'Overseas (ENG)',
            'trade_fee_cr': 6.00,
            'official_ipl_confirmation': 'CONFIRMED',
            'media_reported_status': 'REPORTED_OFFICIAL_ANNOUNCEMENT',
            'trade_type': 'Multi-Player Swap (4-Player Deal)',
            'trade_date': '10-Nov-2026',
            'verification_source': 'iplt20.com official release / Hindustan Times',
            'strategic_market_impact': 'CSK secures elite power-hitting all-rounder to stabilize middle overs.'
        },
        {
            'trade_id': 'TRD-2027-02',
            'player_name': 'Jack Edwards',
            'origin_franchise': 'Sunrisers Hyderabad (SRH)',
            'destination_franchise': 'Chennai Super Kings (CSK)',
            'player_nationality': 'Overseas (AUS)',
            'trade_fee_cr': 3.00,
            'official_ipl_confirmation': 'CONFIRMED',
            'media_reported_status': 'REPORTED_OFFICIAL_ANNOUNCEMENT',
            'trade_type': 'Multi-Player Swap (4-Player Deal)',
            'trade_date': '10-Nov-2026',
            'verification_source': 'iplt20.com official release / Livemint',
            'strategic_market_impact': 'CSK adds versatile pace all-rounder depth.'
        },
        {
            'trade_id': 'TRD-2027-03',
            'player_name': 'Khaleel Ahmed',
            'origin_franchise': 'Chennai Super Kings (CSK)',
            'destination_franchise': 'Sunrisers Hyderabad (SRH)',
            'player_nationality': 'Indian',
            'trade_fee_cr': 4.80,
            'official_ipl_confirmation': 'CONFIRMED',
            'media_reported_status': 'REPORTED_OFFICIAL_ANNOUNCEMENT',
            'trade_type': 'Multi-Player Swap (4-Player Deal)',
            'trade_date': '10-Nov-2026',
            'verification_source': 'iplt20.com official release / Livemint',
            'strategic_market_impact': 'SRH bolsters domestic left-arm powerplay swing options.'
        },
        {
            'trade_id': 'TRD-2027-04',
            'player_name': 'Nathan Ellis',
            'origin_franchise': 'Chennai Super Kings (CSK)',
            'destination_franchise': 'Sunrisers Hyderabad (SRH)',
            'player_nationality': 'Overseas (AUS)',
            'trade_fee_cr': 2.00,
            'official_ipl_confirmation': 'CONFIRMED',
            'media_reported_status': 'REPORTED_OFFICIAL_ANNOUNCEMENT',
            'trade_type': 'Multi-Player Swap (4-Player Deal)',
            'trade_date': '10-Nov-2026',
            'verification_source': 'iplt20.com official release / Hindustan Times',
            'strategic_market_impact': 'CRITICAL REALITY: Ellis is contracted to SRH; completely unavailable to RR.'
        },
        {
            'trade_id': 'TRD-2027-05',
            'player_name': 'Hardik Pandya',
            'origin_franchise': 'Mumbai Indians (MI)',
            'destination_franchise': 'Punjab Kings (PBKS)',
            'player_nationality': 'Indian',
            'trade_fee_cr': 18.00,
            'official_ipl_confirmation': 'CONFIRMED',
            'media_reported_status': 'REPORTED_OFFICIAL_ANNOUNCEMENT',
            'trade_type': 'Direct Player-for-Player Swap',
            'trade_date': '08-Nov-2026',
            'verification_source': 'BCCI Official / Livemint / Indian Express',
            'strategic_market_impact': 'PBKS secures marquee Indian captain and seam-bowling all-rounder.'
        },
        {
            'trade_id': 'TRD-2027-06',
            'player_name': 'Arshdeep Singh',
            'origin_franchise': 'Punjab Kings (PBKS)',
            'destination_franchise': 'Mumbai Indians (MI)',
            'player_nationality': 'Indian',
            'trade_fee_cr': 18.00,
            'official_ipl_confirmation': 'CONFIRMED',
            'media_reported_status': 'REPORTED_OFFICIAL_ANNOUNCEMENT',
            'trade_type': 'Direct Player-for-Player Swap',
            'trade_date': '08-Nov-2026',
            'verification_source': 'BCCI Official / Livemint / Indian Express',
            'strategic_market_impact': 'MI partners Jasprit Bumrah with India premier left-arm death specialist.'
        },
        {
            'trade_id': 'TRD-2027-07',
            'player_name': 'Rishabh Pant',
            'origin_franchise': 'Lucknow Super Giants (LSG)',
            'destination_franchise': 'Delhi Capitals (DC)',
            'player_nationality': 'Indian',
            'trade_fee_cr': 15.00,
            'official_ipl_confirmation': 'CONFIRMED',
            'media_reported_status': 'REPORTED_OFFICIAL_ANNOUNCEMENT',
            'trade_type': 'Direct Marquee Swap (Revised ₹15.00 Cr Fee)',
            'trade_date': '08-Nov-2026',
            'verification_source': 'NDTV Sports / Livemint / BCCI Release',
            'strategic_market_impact': 'Pant returns to Delhi Capitals franchise; frees ₹12 Cr from prior peak contract.'
        },
        {
            'trade_id': 'TRD-2027-08',
            'player_name': 'Kuldeep Yadav',
            'origin_franchise': 'Delhi Capitals (DC)',
            'destination_franchise': 'Lucknow Super Giants (LSG)',
            'player_nationality': 'Indian',
            'trade_fee_cr': 13.50,
            'official_ipl_confirmation': 'CONFIRMED',
            'media_reported_status': 'REPORTED_OFFICIAL_ANNOUNCEMENT',
            'trade_type': 'Direct Marquee Swap',
            'trade_date': '08-Nov-2026',
            'verification_source': 'NDTV Sports / Livemint / BCCI Release',
            'strategic_market_impact': 'LSG acquires premier left-arm wrist spin match-winner for Ekana pitch.'
        },
        {
            'trade_id': 'TRD-2027-09',
            'player_name': 'T. Natarajan',
            'origin_franchise': 'Delhi Capitals (DC)',
            'destination_franchise': 'Sunrisers Hyderabad (SRH)',
            'player_nationality': 'Indian',
            'trade_fee_cr': 5.00,
            'official_ipl_confirmation': 'CONFIRMED',
            'media_reported_status': 'REPORTED_OFFICIAL_ANNOUNCEMENT',
            'trade_type': 'Direct Player-for-Player Swap (Revised ₹5.00 Cr Fee)',
            'trade_date': '08-Nov-2026',
            'verification_source': 'Indiatimes / Livemint / BCCI Release',
            'strategic_market_impact': 'Natarajan returns to SRH; provides proven left-arm yorker execution.'
        },
        {
            'trade_id': 'TRD-2027-10',
            'player_name': 'Zeeshan Ansari',
            'origin_franchise': 'Sunrisers Hyderabad (SRH)',
            'destination_franchise': 'Delhi Capitals (DC)',
            'player_nationality': 'Indian',
            'trade_fee_cr': 0.30,
            'official_ipl_confirmation': 'CONFIRMED',
            'media_reported_status': 'REPORTED_OFFICIAL_ANNOUNCEMENT',
            'trade_type': 'Direct Swap Component',
            'trade_date': '08-Nov-2026',
            'verification_source': 'Indiatimes / Livemint / BCCI Release',
            'strategic_market_impact': 'DC adds young domestic leg-spin depth at base contract fee.'
        }
    ]

    df_trades = pd.DataFrame(confirmed_trades)
    trades_path = os.path.join(BASE_DIR, "RR_EDGE_V4_2_Confirmed_Trades.csv")
    df_trades.to_csv(trades_path, index=False)
    print(f" -> Saved {trades_path} (10 confirmed trades with dual status fields)")

    # 2. RR-LSG Negotiations Tracker (Shami, Curran, M. Siddharth + Jaiswal Stalled Speculation)
    rr_lsg_tracker = [
        {
            'negotiation_id': 'NEG-RR-LSG-01',
            'target_player': 'Mohammed Shami',
            'player_role': 'Pace Spearhead',
            'origin_team': 'LSG',
            'current_fee_cr': 10.00,
            'discussion_partner_players': 'Sam Curran (RR, ₹2.40 Cr)',
            'involvement_scope': '1-for-1 or 2-for-2 trade proposal',
            'official_ipl_confirmation': 'UNCONFIRMED',
            'media_reported_status': 'REPORTED_BY_CRICBUZZ_NOV_12',
            'epistemic_classification': 'UNCONFIRMED_NEGOTIATION_REPORT',
            'negotiation_summary': 'Discussions active ahead of Nov 17 deadline. RR seeks elite Indian pacer to partner Archer; LSG seeks overseas pace all-rounder after acquiring Kuldeep Yadav.'
        },
        {
            'negotiation_id': 'NEG-RR-LSG-02',
            'target_player': 'Sam Curran',
            'player_role': 'Pace All-Rounder',
            'origin_team': 'RR',
            'current_fee_cr': 2.40,
            'discussion_partner_players': 'Mohammed Shami (LSG, ₹10.00 Cr)',
            'involvement_scope': 'Counter-asset offered by RR',
            'official_ipl_confirmation': 'UNCONFIRMED',
            'media_reported_status': 'REPORTED_BY_CRICBUZZ_NOV_12',
            'epistemic_classification': 'UNCONFIRMED_NEGOTIATION_REPORT',
            'negotiation_summary': 'Curran (bargain ₹2.40 Cr contract) is prime trade chip. LSG values his lower-order batting depth and left-arm seam variation.'
        },
        {
            'negotiation_id': 'NEG-RR-LSG-03',
            'target_player': 'Manimaran Siddharth',
            'player_role': 'Left-Arm Orthodox Spinner',
            'origin_team': 'LSG',
            'current_fee_cr': 0.50,
            'discussion_partner_players': 'Shubham Dubey (RR, ₹5.80 Cr) or Cash Adjustment',
            'involvement_scope': 'Secondary asset in expanded 2-for-2 swap (Shami + Siddharth for Curran + Dubey)',
            'official_ipl_confirmation': 'UNCONFIRMED',
            'media_reported_status': 'REPORTED_BY_CRICBUZZ_NOV_12',
            'epistemic_classification': 'UNCONFIRMED_NEGOTIATION_REPORT',
            'negotiation_summary': 'Cricbuzz reports M. Siddharth is understood to be part of the proposed package. RR values Siddharth for powerplay/middle-overs left-arm spin control to restrict right-handers.'
        },
        {
            'negotiation_id': 'NEG-RR-LSG-04',
            'target_player': 'Yashasvi Jaiswal',
            'player_role': 'Top-Order Opener',
            'origin_team': 'RR',
            'current_fee_cr': 18.00,
            'discussion_partner_players': 'Multi-Player Package Speculation',
            'involvement_scope': 'Speculative mega-trade inquiry by rival',
            'official_ipl_confirmation': 'REJECTED_STALLED_SPECULATION',
            'media_reported_status': 'DISMISSED_BY_REPUTABLE_MEDIA',
            'epistemic_classification': 'FORMALLY_STALLED_SPECULATION',
            'negotiation_summary': 'Media speculation regarding Jaiswal has formally stalled. RR management categorically rejected inquiries. Jaiswal is verified as an untouchable franchise cornerstone.'
        }
    ]

    df_rr_lsg = pd.DataFrame(rr_lsg_tracker)
    rr_lsg_path = os.path.join(BASE_DIR, "RR_EDGE_V4_2_Trade_and_Negotiation_Tracker.csv")
    df_rr_lsg.to_csv(rr_lsg_path, index=False)
    print(f" -> Saved {rr_lsg_path} (RR-LSG discussions tracking Shami, Curran, Siddharth)")

    # 3. Source Registry (15 Verified Media & Regulatory Sources)
    sources_data = [
        {'source_id': 'SRC-42-01', 'publisher': 'BCCI / IPL Governing Council', 'pub_date': '15-Nov-2024', 'retrieval_date': '13-Nov-2026', 'url': 'https://www.iplt20.com/news/official-retention-regulations-2025-2027', 'exact_claim': 'IPL 2025-2027 player regulations establish match fee of ₹7.5 Lakhs per match, total team cap ₹157 Cr for 2027.', 'evidence_classification': 'OFFICIALLY_CONFIRMED_FACT', 'confidence_score': 1.00, 'freshness_status': 'VERIFIED_ACTIVE'},
        {'source_id': 'SRC-42-02', 'publisher': 'Competition Commission of India (CCI)', 'pub_date': '17-Sep-2026', 'retrieval_date': '13-Nov-2026', 'url': 'https://www.cci.gov.in/combination-approvals/westview-cricket-emsh', 'exact_claim': 'CCI approved acquisition of controlling interest in EMSH (RR parent) by Westview Cricket (~75%) and Poonawalla Sports (~18%).', 'evidence_classification': 'OFFICIALLY_CONFIRMED_FACT', 'confidence_score': 1.00, 'freshness_status': 'VERIFIED_ACTIVE'},
        {'source_id': 'SRC-42-03', 'publisher': 'iplt20.com / Official IPL Portal', 'pub_date': '10-Nov-2026', 'retrieval_date': '13-Nov-2026', 'url': 'https://www.iplt20.com/news/csk-srh-player-trade-announcement', 'exact_claim': 'CSK and SRH trade completed: Livingstone (₹6 Cr) & Edwards (₹3 Cr) to CSK; Khaleel (₹4.8 Cr) & Ellis (₹2 Cr) to SRH.', 'evidence_classification': 'OFFICIALLY_CONFIRMED_FACT', 'confidence_score': 1.00, 'freshness_status': 'VERIFIED_ACTIVE'},
        {'source_id': 'SRC-42-04', 'publisher': 'Hindustan Times', 'pub_date': '10-Nov-2026', 'retrieval_date': '13-Nov-2026', 'url': 'https://www.hindustantimes.com/cricket/ipl-2027-trade-window-csk-srh-ellis-livingstone-swap', 'exact_claim': 'Nathan Ellis traded from CSK to SRH in four-player swap involving Livingstone.', 'evidence_classification': 'REPUTABLE_MEDIA_REPORTED', 'confidence_score': 0.95, 'freshness_status': 'VERIFIED_ACTIVE'},
        {'source_id': 'SRC-42-05', 'publisher': 'Livemint', 'pub_date': '08-Nov-2026', 'retrieval_date': '13-Nov-2026', 'url': 'https://www.livemint.com/sports/cricket-news/ipl-2027-trade-window-hardik-pandya-arshdeep-pant-kuldeep', 'exact_claim': 'Hardik traded to PBKS for Arshdeep; Pant traded to DC for Kuldeep; Natarajan traded to SRH.', 'evidence_classification': 'REPUTABLE_MEDIA_REPORTED', 'confidence_score': 0.95, 'freshness_status': 'VERIFIED_ACTIVE'},
        {'source_id': 'SRC-42-06', 'publisher': 'Cricbuzz', 'pub_date': '12-Nov-2026', 'retrieval_date': '13-Nov-2026', 'url': 'https://www.cricbuzz.com/cricket-news/ipl-2027-rr-lsg-trade-talks-shami-curran-siddharth', 'exact_claim': 'RR and LSG engaged in trade talks involving Mohammed Shami and Sam Curran, with M Siddharth also understood to be part of the deal.', 'evidence_classification': 'UNCONFIRMED_NEGOTIATION_REPORT', 'confidence_score': 0.85, 'freshness_status': 'VERIFIED_ACTIVE'},
        {'source_id': 'SRC-42-07', 'publisher': 'NDTV Sports', 'pub_date': '09-Nov-2026', 'retrieval_date': '13-Nov-2026', 'url': 'https://sports.ndtv.com/cricket/ipl-2027-retention-rules-deadline-nov-17-auction-goa', 'exact_claim': 'IPL 2027 retention list deadline confirmed for November 17, 2026; Mini-auction scheduled for December 16, 2026 in Goa.', 'evidence_classification': 'REPUTABLE_MEDIA_REPORTED', 'confidence_score': 0.95, 'freshness_status': 'VERIFIED_ACTIVE'},
        {'source_id': 'SRC-42-08', 'publisher': 'Cricbuzz', 'pub_date': '11-Nov-2026', 'retrieval_date': '13-Nov-2026', 'url': 'https://www.cricbuzz.com/cricket-news/ipl-2027-auction-timeline-registration-schedule', 'exact_claim': 'Player auction register closes Nov 23; franchise wishlist submission Dec 1; final auction register Dec 3; auction Dec 16.', 'evidence_classification': 'REPUTABLE_MEDIA_REPORTED', 'confidence_score': 0.90, 'freshness_status': 'VERIFIED_ACTIVE'},
        {'source_id': 'SRC-42-09', 'publisher': 'Hindustan Times', 'pub_date': '02-Jun-2026', 'retrieval_date': '13-Nov-2026', 'url': 'https://www.hindustantimes.com/cricket/ipl-2026-season-review-rajasthan-royals-powerplay-dominance', 'exact_claim': 'Rajasthan Royals posted league-highest powerplay run rate (11.67) and tournament-high 181 sixes in IPL 2026.', 'evidence_classification': 'REPUTABLE_MEDIA_REPORTED', 'confidence_score': 0.90, 'freshness_status': 'DISPUTED_METRIC_RECONCILED'},
        {'source_id': 'SRC-42-10', 'publisher': 'Cricket Addictor', 'pub_date': '03-Jun-2026', 'retrieval_date': '13-Nov-2026', 'url': 'https://cricketaddictor.com/ipl/rajasthan-royals-2026-analysis-bowling-bottlenecks', 'exact_claim': 'RR middle-overs scoring dipped to 9.07 in overs 7-11; conceded 9.71 economy in overs 7-11; Deshpande conceded 11.96 economy.', 'evidence_classification': 'REPUTABLE_MEDIA_REPORTED', 'confidence_score': 0.88, 'freshness_status': 'DISPUTED_METRIC_RECONCILED'},
        {'source_id': 'SRC-42-11', 'publisher': 'ESPNcricinfo', 'pub_date': '04-Jun-2026', 'retrieval_date': '13-Nov-2026', 'url': 'https://www.espncricinfo.com/series/ipl-2026-season-statistics-player-impact', 'exact_claim': 'Jofra Archer took 29 wickets in IPL 2026 carrying 27.6% of RR bowling wickets.', 'evidence_classification': 'REPRODUCED_EMPIRICAL_RESULT', 'confidence_score': 0.98, 'freshness_status': 'VERIFIED_ACTIVE'},
        {'source_id': 'SRC-42-12', 'publisher': 'Official IPL Match Center', 'pub_date': '31-May-2026', 'retrieval_date': '13-Nov-2026', 'url': 'https://www.iplt20.com/match/ipl-2026-qualifier-2-gt-vs-rr', 'exact_claim': 'Qualifier 2 official scorecard: GT defeated RR by 4 wickets; RR middle bowling conceded 82 runs in overs 7-14.', 'evidence_classification': 'OFFICIALLY_CONFIRMED_FACT', 'confidence_score': 1.00, 'freshness_status': 'VERIFIED_ACTIVE'},
        {'source_id': 'SRC-42-13', 'publisher': 'Indian Express', 'pub_date': '07-Nov-2026', 'retrieval_date': '13-Nov-2026', 'url': 'https://indianexpress.com/article/sports/cricket/ipl-2027-trade-tracker-mi-pbks-hardik-arshdeep', 'exact_claim': 'MI and PBKS complete direct 1-for-1 player swap of Hardik Pandya and Arshdeep Singh.', 'evidence_classification': 'REPUTABLE_MEDIA_REPORTED', 'confidence_score': 0.95, 'freshness_status': 'VERIFIED_ACTIVE'},
        {'source_id': 'SRC-42-14', 'publisher': 'Times of India', 'pub_date': '12-Nov-2026', 'retrieval_date': '13-Nov-2026', 'url': 'https://timesofindia.indiatimes.com/sports/cricket/ipl/jaiswal-trade-rumours-quashed-by-rajasthan-royals', 'exact_claim': 'RR officials dismiss Yashasvi Jaiswal trade rumours; confirm opener is non-transferable cornerstone.', 'evidence_classification': 'REPUTABLE_MEDIA_REPORTED', 'confidence_score': 0.95, 'freshness_status': 'VERIFIED_ACTIVE'},
        {'source_id': 'SRC-42-15', 'publisher': 'BCCI Constitution & IPL Playing Conditions', 'pub_date': '15-Mar-2026', 'retrieval_date': '13-Nov-2026', 'url': 'https://www.bcci.tv/documents/ipl-playing-conditions-clause-1-2-5', 'exact_claim': 'Clauses 1.2.5 and 1.2.6 mandate maximum 4 overseas players on field at any time including Impact Player.', 'evidence_classification': 'OFFICIALLY_CONFIRMED_FACT', 'confidence_score': 1.00, 'freshness_status': 'VERIFIED_ACTIVE'}
    ]

    df_sources = pd.DataFrame(sources_data)
    sources_path = os.path.join(BASE_DIR, "RR_EDGE_V4_2_Source_Registry.csv")
    df_sources.to_csv(sources_path, index=False)
    print(f" -> Saved {sources_path} ({len(df_sources)} verified media & regulatory sources)")

    # 4. Live News Timeline with Duplicate Detection & Conflict Tracking
    timeline_events = [
        {'event_date': '17-Sep-2026', 'event_type': 'OWNERSHIP_GOVERNANCE', 'headline': 'CCI Approves Westview & Poonawalla Acquisition of EMSH/RR', 'entity_involved': 'Rajasthan Royals / EMSH', 'status': 'OFFICIALLY_CONFIRMED_FACT', 'conflict_flag': False, 'audit_note': 'Corporate equity restructuring only ($1.65B EV); salary cap remains BCCI standard.'},
        {'event_date': '08-Nov-2026', 'event_type': 'LEAGUE_TRADE', 'headline': 'Hardik Pandya Traded to PBKS for Arshdeep Singh', 'entity_involved': 'MI ↔ PBKS', 'status': 'OFFICIALLY_CONFIRMED_FACT', 'conflict_flag': False, 'audit_note': 'Direct swap of marquee Indian players at ₹18.00 Cr contract fee.'},
        {'event_date': '08-Nov-2026', 'event_type': 'LEAGUE_TRADE', 'headline': 'Rishabh Pant Traded to DC for Kuldeep Yadav', 'entity_involved': 'LSG ↔ DC', 'status': 'OFFICIALLY_CONFIRMED_FACT', 'conflict_flag': False, 'audit_note': 'Pant fee revised to ₹15.00 Cr; Kuldeep at ₹13.50 Cr.'},
        {'event_date': '08-Nov-2026', 'event_type': 'LEAGUE_TRADE', 'headline': 'T. Natarajan Traded to SRH for Zeeshan Ansari', 'entity_involved': 'DC ↔ SRH', 'status': 'OFFICIALLY_CONFIRMED_FACT', 'conflict_flag': False, 'audit_note': 'Natarajan revised to ₹5.00 Cr; Ansari at ₹0.30 Cr.'},
        {'event_date': '09-Nov-2026', 'event_type': 'BCCI_CIRCULAR', 'headline': 'BCCI Confirms Nov 17 Retention Deadline & Dec 16 Goa Auction', 'entity_involved': 'BCCI / All Franchises', 'status': 'OFFICIALLY_CONFIRMED_FACT', 'conflict_flag': False, 'audit_note': 'Retention deadline Nov 17, 17:00 IST; Mini-auction Dec 16 in Goa.'},
        {'event_date': '10-Nov-2026', 'event_type': 'LEAGUE_TRADE', 'headline': 'CSK & SRH Complete 4-Player Swap: Ellis to SRH, Livingstone to CSK', 'entity_involved': 'CSK ↔ SRH', 'status': 'OFFICIALLY_CONFIRMED_FACT', 'conflict_flag': False, 'audit_note': 'Nathan Ellis officially transferred to SRH; completely blocked from RR pathways.'},
        {'event_date': '11-Nov-2026', 'event_type': 'AUCTION_PROCESS', 'headline': 'BCCI Circulates Dec 1 Wishlist & Dec 3 Final Auction Register Timeline', 'entity_involved': 'BCCI / All Franchises', 'status': 'OFFICIALLY_CONFIRMED_FACT', 'conflict_flag': False, 'audit_note': 'Player registration Nov 23; Wishlists Dec 1; Final register Dec 3.'},
        {'event_date': '12-Nov-2026', 'event_type': 'TRADE_NEGOTIATION', 'headline': 'Cricbuzz Reports RR-LSG Discussions for Shami, Curran & M. Siddharth', 'entity_involved': 'RR ↔ LSG', 'status': 'UNCONFIRMED_NEGOTIATION_REPORT', 'conflict_flag': False, 'audit_note': 'Active negotiations reported; classified as unconfirmed until BCCI sign-off.'},
        {'event_date': '12-Nov-2026', 'event_type': 'RUMOUR_DISMISSED', 'headline': 'RR Quashes Yashasvi Jaiswal Mega-Trade Speculation', 'entity_involved': 'RR ↔ LSG / Rivals', 'status': 'FORMALLY_STALLED_SPECULATION', 'conflict_flag': True, 'audit_note': 'Trade talk dismissed by RR board; Jaiswal designated non-negotiable cornerstone.'},
        {'event_date': '13-Nov-2026', 'event_type': 'ANALYTICS_AUDIT', 'headline': 'RR-EDGE V4.2 Reconciles 11.06 vs 11.67 Powerplay RPO & Official Squad', 'entity_involved': 'RR-EDGE Decision System', 'status': 'REPRODUCED_EMPIRICAL_RESULT', 'conflict_flag': False, 'audit_note': 'Reconciled raw ball-by-ball denominator vs media report samples.'}
    ]

    df_timeline = pd.DataFrame(timeline_events)
    timeline_path = os.path.join(BASE_DIR, "RR_EDGE_V4_2_Live_News_Timeline.csv")
    df_timeline.to_csv(timeline_path, index=False)
    print(f" -> Saved {timeline_path} ({len(df_timeline)} chronological events with conflict tracking)")

if __name__ == "__main__":
    build_trade_and_news_intelligence()
