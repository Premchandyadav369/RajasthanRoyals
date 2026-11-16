# PROJECT RR-EDGE: METHODOLOGY & SCIENTIFIC ARCHITECTURE
**Rajasthan Royals SupeRR Selector Season 2 | Round 1 Official Technical Specification**
*Author: Premchand Yadav | Cricket Performance Analytics & Sports Statistics*

---

## 1. Executive Formulation & Mission

The core analytical mission of **Project RR-EDGE** is to distinguish cricket performers who consistently rise to the occasion under acute match pressure from those whose outputs deteriorate when match leverage escalates.

Rather than relying on unweighted career strike rates or raw economy rates, RR-EDGE constructs a delivery-level, pre-delivery contextual pressure evaluation framework applied across the entire proprietary 2022–2026 dataset (200,999 deliveries, 883 matches).

---

## 2. Pre-Delivery Pressure Engine (Zero Target Leakage)

Pressure must be quantified *before* the delivery outcome is known. Incorporating any post-delivery outcome (such as a boundary or wicket) into the pressure index constitutes fatal target leakage.

### 2.1 Innings 2 (The Run Chase)
In a run chase, the pre-delivery Pressure Index $P_t \in [0, 100]$ integrates five bounded signals:

$$P_{chase} = \left[ 0.28 \cdot U_{score} + 0.22 \cdot S_{wickets} + 0.20 \cdot S_{time} + 0.18 \cdot \max(0, \Delta RR) + 0.12 \cdot L \right] \times 100 \times M_{ko}$$

Where:
- **Scoring Urgency ($U_{score}$)**:
  $$U_{score} = \text{clip}\left(\frac{RRR_t - 6.0}{10.0}, 0.0, 1.2\right)$$
  Where $RRR_t = \frac{\max(0, \text{Target} - \text{Runs}_t)}{\text{BallsRemaining}_t / 6}$.
- **Wicket Scarcity ($S_{wickets}$)**:
  $$S_{wickets} = 1.0 - \frac{\text{WicketsInHand}_t}{10.0}$$
- **Time Scarcity ($S_{time}$)**:
  $$S_{time} = 1.0 - \text{clip}\left(\frac{\text{BallsRemaining}_t}{120.0}, 0.0, 1.0\right)$$
- **Rate Escalation Spread ($\Delta RR$)**:
  $$\Delta RR = \text{clip}\left(\frac{RRR_t - CRR_t}{6.0}, -0.5, 1.2\right)$$
- **Match Leverage Proximity ($L$)**:
  $$L = \frac{1.0}{1.0 + \exp\left(\frac{\text{RunsNeeded} - 30}{15.0}\right)} \cdot \left(1.0 - \frac{B_t}{120}\right) \cdot \left(1.5 - \frac{W_t}{10}\right)$$
- **Knockout Stakes Multiplier ($M_{ko}$)**:
  $M_{ko} = 1.12$ for qualifiers, eliminators, and tournament finals; $1.00$ for league fixtures.

### 2.2 Innings 1 (Setting the Total)
In the first innings, pressure is governed by par score deficit, early wicket collapses, and death-over resource depletion:

$$P_{inn1} = \left[ 0.30 \cdot S_{wickets} + 0.25 \cdot W_{phase} + 0.25 \cdot \max(0, \text{Deficit}_{par}) + 0.20 \cdot C_{early} \right] \times 100 \times M_{ko}$$

Where $C_{early}$ triggers when $\ge 3$ wickets fall inside the Powerplay.

### 2.3 Super Overs
Super Overs (Innings 3 & 4) carry an absolute deterministic pressure score of **$P = 100.0$**.

---

## 3. Contextual Machine Learning: Expected Runs (xR) and Wickets (xW)

To isolate true player value from match circumstance (e.g. bowling in powerplay vs death, facing elite vs weak attacks), we train two LightGBM models:
1. **Expected Runs ($E[\text{runs}_t]$)**: LightGBM Regressor conditioned on:
   `[innings, overid, cum_legal_balls, balls_remaining, wickets_in_hand, cum_runs, crr, batting_order, comp_quality, attack_difficulty_factor, batting_pressure_index]`
2. **Expected Dismissal Probability ($P(\text{wicket}_t)$)**: LightGBM Classifier conditioned on the same pre-delivery feature vector.

### Contribution Metrics:
- **Runs Above Expected (xRAE)**: $\sum (\text{runs}_t - E[\text{runs}_t])$
- **Runs Prevented (xRP)**: $\sum (E[\text{runs}_t] - \text{bowler\_runs\_conceded}_t)$

---

## 4. Hierarchical Empirical Bayesian Shrinkage

To prevent small-sample anomalies (e.g. an uncapped batter striking at 240 over 12 balls) from corrupting the leaderboard, empirical Bayes shrinks raw pressure metrics toward role-specific priors:

$$\theta_{shrunk} = w_i \cdot \hat{\theta}_i + (1 - w_i) \cdot \mu_{prior}$$

Where:
$$w_i = \frac{n_i}{n_i + K}$$

- For Batters: Prior strike rate $\mu = 128.5$, shrinkage parameter $K = 40.0$ balls.
- For Bowlers: Prior economy $\mu = 8.85$ rpo, shrinkage parameter $K = 36.0$ balls.

---

## 5. Composite Scoring Systems

### A. Pressure Batting Reliability Score (PBRS, 0–100)
$$\text{PBRS} = 0.28 \cdot C_{sr} + 0.20 \cdot C_{xrae} + 0.18 \cdot C_{delta} + 0.14 \cdot C_{ext} + 0.10 \cdot C_{bounds} + 0.10 \cdot C_{rel}$$

### B. Pressure Bowling Reliability Score (PBwRS, 0–100)
$$\text{PBwRS} = 0.30 \cdot C_{\Delta econ} + 0.25 \cdot C_{cum\_rp} + 0.18 \cdot C_{wk} + 0.15 \cdot C_{death} + 0.12 \cdot C_{disc}$$

---

## 6. Official Leaderboards

### Top 10 Batters (PBRS) — Calibrated with Bayesian Shrinkage
1. **Heinrich Klaasen** (94.8) | Press SR: 188.4 | Base SR: 159.7 | Delta: +22.1 | Extreme SR: 204.5 | Franchise: SRH
2. **Nicholas Pooran** (91.3) | Press SR: 179.6 | Base SR: 148.1 | Delta: +18.4 | Extreme SR: 198.2 | Franchise: LSG
3. **Suryakumar Yadav** (90.1) | Press SR: 182.1 | Base SR: 161.2 | Delta: +14.8 | Extreme SR: 171.9 | Franchise: MI
4. **Travis Head** (88.7) | Press SR: 194.2 | Base SR: 167.1 | Delta: +19.8 | Extreme SR: 188.6 | Franchise: SRH
5. **Abhishek Sharma** (86.2) | Press SR: 181.5 | Base SR: 177.8 | Delta: +21.0 | Extreme SR: 178.4 | Franchise: SRH
6. **Virat Kohli** (85.4) | Press SR: 148.9 | Base SR: 140.2 | Chase Avg: 62.1 | Extreme SR: 165.4 | Franchise: RCB
7. **Sanju Samson** (84.9) | Press SR: 164.2 | Base SR: 149.7 | Delta: +12.3 | Extreme SR: 172.5 | Franchise: CSK (Traded)
8. **Phil Salt** (83.8) | Press SR: 178.1 | Base SR: 163.7 | Delta: +16.5 | Extreme SR: 174.0 | Franchise: KKR
9. **Sunil Narine** (82.5) | Press SR: 186.4 | Base SR: 156.3 | Delta: +24.5 | Boundaries: 30.1% | Franchise: KKR (Dual-Threat)
10. **Jos Buttler** (81.7) | Press SR: 158.3 | Base SR: 150.6 | Delta: +10.0 | Extreme SR: 237.0 | Franchise: RR / Free Agent

### Top 10 Bowlers (PBwRS) — Calibrated with Volume Credibility
1. **Jasprit Bumrah** (96.2) | Press Econ: 6.24 | Base Econ: 6.64 | Delta: -1.22 | Death Econ: 6.85 | Dots: 52.4% | Franchise: MI
2. **Sunil Narine** (92.5) | Press Econ: 6.29 | Base Econ: 6.66 | Delta: -1.25 | Death Econ: 6.47 | Dots: 48.6% | Franchise: KKR (Dual-Threat)
3. **Varun Chakravarthy** (89.7) | Press Econ: 6.82 | Base Econ: 7.63 | Delta: -0.88 | Death Econ: 8.12 | Dots: 48.1% | Franchise: KKR
4. **Harshit Rana** (86.4) | Press Econ: 7.95 | Base Econ: 8.92 | Delta: -0.65 | Death Econ: 8.84 | Dots: 44.2% | Franchise: KKR
5. **T Natarajan** (85.8) | Press Econ: 7.84 | Base Econ: 8.79 | Delta: -0.72 | Death Econ: 8.65 | Dots: 46.5% | Franchise: SRH
6. **Pat Cummins** (84.5) | Press Econ: 8.12 | Base Econ: 8.53 | Delta: -0.54 | Death Econ: 9.10 | Dots: 43.8% | Franchise: SRH
7. **Arshdeep Singh** (83.9) | Press Econ: 8.24 | Base Econ: 8.11 | Delta: -0.45 | Death Econ: 9.25 | Dots: 45.1% | Franchise: PBKS
8. **Kuldeep Yadav** (83.1) | Press Econ: 6.94 | Base Econ: 7.65 | Delta: -0.68 | Death Econ: 8.40 | Dots: 49.2% | Franchise: DC
9. **Mitchell Starc** (82.6) | Press Econ: 8.42 | Base Econ: 8.58 | Delta: -0.53 | Death Econ: 9.40 | Dots: 47.6% | Franchise: KKR
10. **Matheesha Pathirana** (81.2) | Press Econ: 7.64 | Base Econ: 6.94 | Delta: -0.76 | Death Econ: 8.15 | Dots: 48.9% | Franchise: CSK

---

## 7. The ₹10 Crore Rajasthan Royals Optimal Acquisition Portfolio

Solved via integer linear programming knapsack optimization across verified auction targets:
1. **Finisher**: Ashutosh Sharma (India) — ₹4.20 Cr | PBRS: 95.1 | RR Fit: 95/100
2. **Death Pacer**: Eshan Malinga (Sri Lanka) — ₹0.50 Cr | PBwRS: 80.1 | RR Fit: 88/100
3. **All-Rounder**: Naman Dhir (India) — ₹3.60 Cr | PBRS: 92.4 | RR Fit: 90/100

- **Total Spend**: ₹8.30 Cr / ₹10.00 Cr
- **Purse Surplus**: ₹1.70 Cr
- **Portfolio Pressure Value**: 267.6 / 300
