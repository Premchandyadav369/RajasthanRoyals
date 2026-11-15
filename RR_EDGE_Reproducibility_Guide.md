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

The official player names and player IDs match the Unstop dropdown options exactly:

### Batters:
- Rank 1: Jos Buttler (ID: 813)
- Rank 2: Ashutosh Sharma (ID: 8101)
- Rank 3: Shubham Dubey (ID: 25139)
- Rank 4: Naman Dhir (ID: 37052)
- Rank 5: Suryakumar Yadav (ID: 1699)
- Rank 6: Mark Chapman (ID: 3374)
- Rank 7: Dhruv Jurel (ID: 7260)
- Rank 8: David Miller (ID: 1077)
- Rank 9: Rishabh Pant (ID: 4703)
- Rank 10: Vipraj Nigam (ID: 46066)

### Bowlers:
- Rank 1: Jasprit Bumrah (ID: 2933)
- Rank 2: Sunil Narine (ID: 781)
- Rank 3: Matthew Humphreys (ID: 22471)
- Rank 4: Ehsan Khan (ID: 5750)
- Rank 5: Imad Wasim (ID: 3578)
- Rank 6: Matheesha Pathirana (ID: 8661)
- Rank 7: Mohammad Nawaz (ID: 2490)
- Rank 8: Nasum Ahmed (ID: 4658)
- Rank 9: George Linde (ID: 4229)
- Rank 10: Eshan Malinga (ID: 39657)
