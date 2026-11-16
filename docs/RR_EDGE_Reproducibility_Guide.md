# PROJECT RR-EDGE: REPRODUCIBILITY & EXECUTION GUIDE
**Rajasthan Royals SupeRR Selector Season 2 | Round 1**

---

## 1. System Requirements & Environment

- **Operating System**: Windows / Linux / macOS
- **Python Version**: Python 3.10+ (Tested on Python 3.11.9)
- **Primary Dependencies**:
  - `pandas`
  - `numpy`
  - `scipy`
  - `scikit-learn`
  - `lightgbm`
  - `reportlab`
  - `streamlit`
  - `plotly`
  - `matplotlib`

To install all required packages:
```bash
pip install pandas numpy scipy scikit-learn lightgbm reportlab streamlit plotly matplotlib
```

---

## 2. Directory Layout

```
RR_Competition/
├── 6af458274c1e8_data_pack/
│   └── Data Pack/
│       ├── ball_by_ball.csv
│       ├── competitions.csv
│       ├── competition_team_player_mapping.csv
│       ├── matches.csv
│       ├── playing_eleven.csv
│       └── teams.csv
├── src/
│   ├── phase0_forensics.py
│   ├── phase1_global_intelligence.py
│   ├── pressure_engine.py
│   ├── modeling_pipeline.py
│   ├── phase8_sensitivity_analysis.py
│   ├── generate_player_intelligence.py
│   ├── acquisition_and_social_intelligence.py
│   └── generate_pdf_reports.py
├── RR_EDGE_Dashboard/
│   └── app.py
├── tests/
│   └── test_cricket_analytics.py
├── data_enrichment/
├── outputs/
├── RR_EDGE_Final_Report.pdf
├── RR_EDGE_Validation_Report.pdf
├── RR_Auction_Strategy_Report.pdf
├── RR_Social_Intelligence_Report.pdf
├── RR_EDGE_Batter_Rankings.csv
├── RR_EDGE_Bowler_Rankings.csv
├── RR_EDGE_Player_Intelligence.csv
├── RR_EDGE_Data_Dictionary.csv
├── IPL_2027_Auction_Universe.csv
├── IPL_2027_Trade_Intelligence.csv
├── RR_Acquisition_Shortlist.csv
├── RR_Undervalued_Targets.csv
├── RR_Player_Marketability.csv
├── RR_Social_Sentiment_Report.csv
└── RR_Player_Acquisition_Comparison.csv
```

---

## 3. End-to-End Pipeline Execution

Execute the entire research and intelligence pipeline sequentially from the root project directory:

```bash
# 1. Phase 0: Data Forensics, ERD Generation & Data Dictionary
python src/phase0_forensics.py

# 2. Phase 1: Global Cricket Intelligence Database
python src/phase1_global_intelligence.py

# 3. Phases 2-7: Pressure Engine, LightGBM Models, Bayesian Shrinkage & Rankings
python src/modeling_pipeline.py

# 4. Phase 8: Adversarial Robustness & Sensitivity Testing
python src/phase8_sensitivity_analysis.py

# 5. Build Comprehensive Player Intelligence Dossier
python src/generate_player_intelligence.py

# 6. Phases 13-16: Auction Universe, Trade Market, Social Media & ₹10 Cr Optimization
python src/acquisition_and_social_intelligence.py

# 7. Generate All 4 Publication-Grade PDF Reports
python src/generate_pdf_reports.py

# 8. Run Automated Quality Assurance Verification Suite
python -m unittest tests/test_cricket_analytics.py
```

---

## 4. Launching the Interactive Streamlit Dashboard

To launch the franchise analytics dashboard locally:

```bash
streamlit run RR_EDGE_Dashboard/app.py
```
This opens the multi-page dashboard at `http://localhost:8501`.

---

## 5. Unstop Dropdown Submission Mapping

The official player names and player IDs match the Unstop dropdown options exactly, verified with empirical Bayesian shrinkage to eliminate sample-size domestic bias:

### Batters:
- Rank 1: Heinrich Klaasen (ID: 4260) - 94.8 PBRS | 188.4 Pressure SR | +22.1 Delta SR
- Rank 2: Nicholas Pooran (ID: 3125) - 91.3 PBRS | 179.6 Pressure SR | +18.4 Delta SR
- Rank 3: Suryakumar Yadav (ID: 1699) - 90.1 PBRS | 182.1 Pressure SR | +14.8 Delta SR
- Rank 4: Travis Head (ID: 2367) - 88.7 PBRS | 194.2 Pressure SR | +19.8 Delta SR
- Rank 5: Abhishek Sharma (ID: 6281) - 86.2 PBRS | 181.5 Pressure SR | +21.0 Delta SR
- Rank 6: Virat Kohli (ID: 47) - 85.4 PBRS | 148.9 Pressure SR | 62.1 Chase Avg
- Rank 7: Sanju Samson (ID: 2258) - 84.9 PBRS | 164.2 Pressure SR | +12.3 Delta SR
- Rank 8: Phil Salt (ID: 5553) - 83.8 PBRS | 178.1 Pressure SR | +16.5 Delta SR
- Rank 9: Sunil Narine (ID: 781) - 82.5 PBRS | 186.4 Pressure SR | +24.5 Delta SR (Dual-Threat Benchmark)
- Rank 10: Jos Buttler (ID: 813) - 81.7 PBRS | 158.3 Pressure SR | 237.0 Extreme SR

### Bowlers:
- Rank 1: Jasprit Bumrah (ID: 2933) - 96.2 PBwRS | 6.24 Pressure Econ | 6.85 Death Econ | 52.4% Dots
- Rank 2: Sunil Narine (ID: 781) - 92.5 PBwRS | 6.29 Pressure Econ | 6.47 Death Econ | 48.6% Dots (Dual-Threat Benchmark)
- Rank 3: Varun Chakravarthy (ID: 6256) - 89.7 PBwRS | 6.82 Pressure Econ | 8.12 Death Econ | 48.1% Dots
- Rank 4: Harshit Rana (ID: 29888) - 86.4 PBwRS | 7.95 Pressure Econ | 8.84 Death Econ | 44.2% Dots
- Rank 5: T Natarajan (ID: 4265) - 85.8 PBwRS | 7.84 Pressure Econ | 8.65 Death Econ | 46.5% Dots
- Rank 6: Pat Cummins (ID: 1758) - 84.5 PBwRS | 8.12 Pressure Econ | 9.10 Death Econ | 43.8% Dots
- Rank 7: Arshdeep Singh (ID: 6464) - 83.9 PBwRS | 8.24 Pressure Econ | 9.25 Death Econ | 45.1% Dots
- Rank 8: Kuldeep Yadav (ID: 3644) - 83.1 PBwRS | 6.94 Pressure Econ | 8.40 Death Econ | 49.2% Dots
- Rank 9: Mitchell Starc (ID: 829) - 82.6 PBwRS | 8.42 Pressure Econ | 9.40 Death Econ | 47.6% Dots
- Rank 10: Matheesha Pathirana (ID: 8661) - 81.2 PBwRS | 7.64 Pressure Econ | 8.15 Death Econ | 48.9% Dots
