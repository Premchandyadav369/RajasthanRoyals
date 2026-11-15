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

### Top 10 Batters (PBRS)
1. **Jos Buttler** (100.0) | P.Balls: 651 | Press SR: 181.9 | Delta: +33.7 | xRAE: +166.4
2. **Ashutosh Sharma** (95.1) | P.Balls: 125 | Press SR: 167.2 | Delta: +39.0 | xRAE: +39.7
3. **Shubham Dubey** (94.7) | P.Balls: 70 | Press SR: 171.4 | Delta: +75.9 | xRAE: +35.5
4. **Naman Dhir** (92.4) | P.Balls: 89 | Press SR: 174.8 | Delta: +16.6 | xRAE: +23.8
5. **Suryakumar Yadav** (90.0) | P.Balls: 412 | Press SR: 173.5 | Delta: +14.8 | xRAE: +73.7
6. **Mark Chapman** (89.5) | P.Balls: 161 | Press SR: 163.5 | Delta: +32.3 | xRAE: +38.5
7. **Dhruv Jurel** (89.4) | P.Balls: 226 | Press SR: 163.5 | Delta: +25.3 | xRAE: +38.7
8. **David Miller** (88.4) | P.Balls: 432 | Press SR: 159.4 | Delta: +28.4 | xRAE: +71.6
9. **Rishabh Pant** (88.1) | P.Balls: 307 | Press SR: 159.9 | Delta: +27.4 | xRAE: +47.5
10. **Vipraj Nigam** (88.0) | P.Balls: 57 | Press SR: 161.8 | Delta: +28.4 | xRAE: +13.5

### Top 10 Bowlers (PBwRS)
1. **Jasprit Bumrah** (100.0) | P.Balls: 821 | Press Econ: 7.83 | Death Econ: 7.68 | xRP: +228.5
2. **Sunil Narine** (98.3) | P.Balls: 754 | Press Econ: 7.54 | Death Econ: 8.87 | xRP: +171.9
3. **Matthew Humphreys** (94.2) | P.Balls: 99 | Press Econ: 6.80 | Death Econ: 7.50 | xRP: +37.6
4. **Ehsan Khan** (87.7) | P.Balls: 100 | Press Econ: 7.99 | Death Econ: 8.24 | xRP: +17.2
5. **Imad Wasim** (86.4) | P.Balls: 124 | Press Econ: 6.74 | Death Econ: 7.85 | xRP: +17.1
6. **Matheesha Pathirana** (86.1) | P.Balls: 466 | Press Econ: 9.29 | Death Econ: 9.38 | xRP: +105.5
7. **Mohammad Nawaz** (83.0) | P.Balls: 337 | Press Econ: 7.03 | Death Econ: 9.80 | xRP: +56.9
8. **Nasum Ahmed** (82.4) | P.Balls: 157 | Press Econ: 7.06 | Death Econ: 11.20 | xRP: +36.8
9. **George Linde** (80.3) | P.Balls: 110 | Press Econ: 8.33 | Death Econ: 9.82 | xRP: +16.0
10. **Eshan Malinga** (80.1) | P.Balls: 88 | Press Econ: 8.75 | Death Econ: 8.25 | xRP: +13.8

---

## 7. The ₹10 Crore Rajasthan Royals Optimal Acquisition Portfolio

Solved via integer linear programming knapsack optimization across verified auction targets:
1. **Finisher**: Ashutosh Sharma (India) — ₹4.20 Cr | PBRS: 95.1 | RR Fit: 95/100
2. **Death Pacer**: Eshan Malinga (Sri Lanka) — ₹0.50 Cr | PBwRS: 80.1 | RR Fit: 88/100
3. **All-Rounder**: Naman Dhir (India) — ₹3.60 Cr | PBRS: 92.4 | RR Fit: 90/100

- **Total Spend**: ₹8.30 Cr / ₹10.00 Cr
- **Purse Surplus**: ₹1.70 Cr
- **Portfolio Pressure Value**: 267.6 / 300
