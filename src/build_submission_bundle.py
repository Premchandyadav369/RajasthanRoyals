"""
Builds the definitive all-in-one submission bundle ZIP file:
RR_SupeRR_Selector_S2_Submission_Bundle.zip
Includes all publication-grade PDFs, PPTX decks, 4K slide assets, CSV models,
interactive HTML war rooms, social cards, and SHA-256 manifest.
"""

import os
import zipfile
import hashlib

BASE_DIR = r"C:\Users\PREMCHANDYADAV\Downloads\RR_Competition"
ZIP_PATH = os.path.join(BASE_DIR, "RR_SupeRR_Selector_S2_Submission_Bundle.zip")

FILES_TO_BUNDLE = [
    # Primary Master Dossiers & Editorial Decks
    "RR_EDGE_Franchise_Master_Dossier.pdf",
    "RR_EDGE_Judges_Fast_Track_Brief.pdf",
    "RR_EDGE_V6_0_Franchise_Master_Dossier.pdf",
    "RR_EDGE_V6_0_Executive_Presentation.pptx",
    "RR_EDGE_V5_0_Franchise_Master_Dossier.pdf",
    "RR_EDGE_V5_0_Executive_Presentation.pptx",
    "RR_EDGE_V4_2_Presentation.pptx",
    "RR_WAR_ROOM_EXECUTIVE_SUITE.html",
    "RR_High_Performance_Training_Prescription.pdf",
    "RR_EDGE_Board_Memorandum.pdf",
    "RR_Tactical_Coaching_Playbook.pdf",
    "RR_EDGE_V4_2_Executive_Dossier.pdf",
    "RR_EDGE_V4_2_Technical_Methodology_Report.pdf",
    "RR_EDGE_V4_2_Scouting_and_Auction_Blueprint.pdf",
    "RR_EDGE_V4_2_Automated_Test_Report.pdf",
    "RR_EDGE_V4_2_Financial_Reconciliation.xlsx",
    "auction_warroom_simulator.py",
    
    # 4K Presentation Visual Plates (PPT Image DESIGN.md)
    "slide_assets/hero_cover_plate.png",
    "slide_assets/bottleneck_comparison_plate.png",
    "slide_assets/pitch_telemetry_plate.png",
    "slide_assets/capital_allocation_plate.png",
    "slide_assets/championship_verdict_plate.png",
    "slide_assets/pareto_frontier_plate.png",
    "slide_assets/crisis_hazard_plate.png",

    # Competition Rankings & Data Registries
    "RR_EDGE_Batter_Rankings.csv",
    "RR_EDGE_Bowler_Rankings.csv",
    "RR_EDGE_V4_2_Official_2026_Squad.csv",
    "RR_EDGE_V4_2_Decision_Ledger.csv",
    "RR_EDGE_V4_2_Claim_Registry.csv",
    "RR_2027_Optimal_XI.csv",

    # Advanced Multi-Dimensional Datasets (15 Dimensions)
    "outputs/advanced_dimensions/stadium_aerodynamics_flight_model.csv",
    "outputs/advanced_dimensions/high_performance_training_prescriptions.csv",
    "outputs/advanced_dimensions/ball_tracking_physics_telemetry.csv",
    "outputs/advanced_dimensions/fielding_spatial_and_catch_wpa.csv",
    "outputs/advanced_dimensions/drs_bayesian_decision_policy.csv",
    "outputs/advanced_dimensions/psychometric_clutch_degradation.csv",
    "outputs/advanced_dimensions/squad_war_and_injury_resilience.csv",
    "outputs/advanced_dimensions/contract_surplus_and_pareto_frontiers.csv",
    "outputs/advanced_dimensions/contract_surplus_player_valuations.csv",
    "outputs/advanced_dimensions/cluster_collapse_hazard_models.csv",
    "outputs/advanced_dimensions/opponent_neutralization_matrix.csv",
    
    # Advanced Analytical Engines Datasets
    "outputs/optimal_20_over_bowling_allocation.csv",
    "outputs/optimal_bowler_spell_summary.csv",
    "outputs/optimal_batting_entry_matrix.csv",
    "outputs/wpa_ball_by_ball_simulation.csv",
    "outputs/pressure_collapse_scenarios.csv",
    "outputs/squad_innings_stabilizers.csv",
    "outputs/head_to_head_micro_simulations.csv",
    "outputs/auction_bid_elasticity_model.csv",
    "outputs/stadium_microclimate_dew_matrix.csv",

    # Advanced Machine Learning & Feature Selection
    "outputs/advanced_ml/feature_selection_comparison.csv",
    "outputs/advanced_ml/feature_selection_diagnostic_plot.png",
    "outputs/advanced_ml/hyperparameter_tuning_results.csv",
    "outputs/advanced_ml/stacking_ensemble_performance.csv",

    # Frontier Operations Research & Biomechanics
    "outputs/frontier_analytics/markov_chain_analytical_distributions.csv",
    "outputs/frontier_analytics/survival_hazard_curves.csv",
    "outputs/frontier_analytics/handedness_synergy_matrix.csv",
    "outputs/frontier_analytics/milp_globally_optimal_squad.csv",
    "outputs/frontier_analytics/archer_biomechanical_workload_schedule.csv",
    
    # Social Media Cards
    "social_cards/RR_Card_1_Top_10_Batsmen.png",
    "social_cards/RR_Card_2_Top_10_Bowlers.png",
    "social_cards/RR_Card_3_Overs_7_11_Leak_Diagnostic.png",
    "social_cards/RR_Card_4_Plan_B_Auction_Rebalance.png",
    "social_cards/RR_Card_5_Monte_Carlo_Tournament_Sim.png"
]

def resolve_file(rel_path):
    candidates = [
        os.path.join(BASE_DIR, rel_path),
        os.path.join(BASE_DIR, "src", rel_path),
        os.path.join(BASE_DIR, "reports", rel_path),
        os.path.join(BASE_DIR, "archive", "v5_iterations", rel_path),
        os.path.join(BASE_DIR, "archive", "v4_iterations", rel_path),
        os.path.join(BASE_DIR, "archive", "v3_iterations", rel_path),
        os.path.join(BASE_DIR, "archive", "v2_iterations", rel_path),
        os.path.join(BASE_DIR, "archive", "legacy_versions", rel_path),
        os.path.join(BASE_DIR, "data", rel_path),
        os.path.join(BASE_DIR, "docs", rel_path),
    ]
    for c in candidates:
        if os.path.exists(c):
            return c
    return os.path.join(BASE_DIR, rel_path)

def get_sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        while chunk := f.read(8192):
            h.update(chunk)
    return h.hexdigest()

def create_bundle():
    print(f"Creating ZIP Bundle at {ZIP_PATH}...")
    manifest_lines = ["RR-EDGE V6.0 OFFICIAL SUBMISSION BUNDLE SHA-256 CHECKSUMS", "=" * 70]
    
    with zipfile.ZipFile(ZIP_PATH, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for rel_path in FILES_TO_BUNDLE:
            full_path = resolve_file(rel_path)
            if os.path.exists(full_path):
                zipf.write(full_path, arcname=rel_path)
                sha = get_sha256(full_path)
                manifest_lines.append(f"{sha}  {rel_path}")
                print(f"Added: {rel_path} ({os.path.getsize(full_path)} bytes)")
            else:
                print(f"WARNING: File not found: {rel_path}")

        # Add manifest to zip
        manifest_content = "\n".join(manifest_lines) + "\n"
        zipf.writestr("CHECKSUMS.txt", manifest_content)
        
        # Add summary instructions for judges
        readme_content = """# PROJECT RR-EDGE V6.0: OFFICIAL SUBMISSION BUNDLE
Shaping Rajasthan Royals' IPL 2027 Auction & Tactical Strategy

Included Master Artifacts:
1. RR_EDGE_Judges_Fast_Track_Brief.pdf: 1-Page Fast-Track Executive Brief for the 60-second jury scan.
2. RR_EDGE_V6_0_Franchise_Master_Dossier.pdf: 2-Page Executive Master Encyclopedia covering 15 analytical dimensions.
3. RR_EDGE_V5_0_Executive_Presentation.pptx: 12-Slide 16:9 Widescreen Editorial Deck with 7 4K plates (Zero AI Slop).
4. RR_WAR_ROOM_EXECUTIVE_SUITE.html: Standalone offline zero-dependency HTML5 war room application.
5. RR_High_Performance_Training_Prescription.pdf: Red Bull High Performance Academy Biomechanical Drill Directive.
6. RR_EDGE_Board_Memorandum.pdf: C-Suite Memorandum for Manoj Badale, Jake Lush McCrum, and Kumar Sangakkara.
7. RR_Tactical_Coaching_Playbook.pdf: Opposition Neutralization Playbook for 9 rival franchises.
8. slide_assets/: 7 full-resolution 3840x2160 (16:9 4K) presentation plates following PPT Image DESIGN.md.
9. outputs/advanced_dimensions/: CSV datasets covering physics, aerodynamics, DRS, fielding, clutch, WAR, surplus, and hazards.
10. social_cards/: 5 high-resolution 1080x1080 infographics for social video and community campaigns.

Halla Bol!
"""
        zipf.writestr("SUBMISSION_README.md", readme_content)

    # Write CHECKSUMS.txt to root workspace as well
    with open(os.path.join(BASE_DIR, "CHECKSUMS.txt"), "w", encoding="utf-8") as f:
        f.write(manifest_content)

    print(f"\nBundle created successfully: {ZIP_PATH}")
    print(f"Total size: {os.path.getsize(ZIP_PATH):,} bytes")

if __name__ == "__main__":
    create_bundle()
