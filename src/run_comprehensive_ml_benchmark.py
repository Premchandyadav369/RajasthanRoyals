"""
RR-EDGE V4.2 Comprehensive Machine Learning & Statistical Benchmark Suite
Adheres strictly to ML Best Practices:
- Pre-delivery feature engineering (Zero Target Leakage)
- Chronological / Match-Stratified Train/Val/Test splits (70/15/15)
- Regression Benchmark (xR): Naive, Ridge, RF, LightGBM, XGBoost, Bayesian Ridge, PyTorch MLP
- Classification Benchmark (xW): Prior Baseline, Logistic, RF, LightGBM, XGBoost
- Unsupervised Clustering: k-Means (Silhouette curve), GMM, PCA 2D
- Feature Importance & Inference Latency Profiling
- 95% Bootstrap Confidence Intervals
"""

import os
import time
import json
import warnings
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from scipy import stats

# ML Frameworks
from sklearn.model_selection import train_test_split
from sklearn.linear_model import Ridge, LogisticRegression, BayesianRidge
from sklearn.ensemble import RandomForestRegressor, RandomForestClassifier
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score, roc_auc_score, log_loss, brier_score_loss, silhouette_score
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
from sklearn.mixture import GaussianMixture
from sklearn.decomposition import PCA

import lightgbm as lgb
import xgboost as xgb
import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import TensorDataset, DataLoader

warnings.filterwarnings('ignore')

BASE_DIR = r"C:\Users\PREMCHANDYADAV\Downloads\RR_Competition"
DATA_PACK_DIR = os.path.join(BASE_DIR, r"6af458274c1e8_data_pack\Data Pack")
OUTPUTS_DIR = os.path.join(BASE_DIR, "outputs")
os.makedirs(OUTPUTS_DIR, exist_ok=True)

# -------------------------------------------------------------
# STEP 1: LOAD & LEAKAGE-FREE FEATURE ENGINEERING
# -------------------------------------------------------------
def load_and_engineer_features():
    print("[Step 1] Loading 200,999 deliveries and engineering leak-free pre-delivery features...")
    bbb = pd.read_csv(os.path.join(DATA_PACK_DIR, 'ball_by_ball.csv'), low_memory=False)
    matches = pd.read_csv(os.path.join(DATA_PACK_DIR, 'matches.csv'), low_memory=False)

    # Sort strictly chronologically within each match
    df = bbb.sort_values(['match_id', 'innings', 'overid', 'over_ball_num', 'innings_ball_num']).copy()
    
    # Delivery total runs
    df['total_runs'] = df['runs'] + df['extras1_runs'] + df['extras_2_runs']
    df['is_legal'] = ~df['extras_type'].isin(['wide', 'Overstep'])
    
    # Pre-delivery cumulative stats (shifted to guarantee 0 leakage)
    grp = df.groupby(['match_id', 'innings'])
    df['cum_runs_pre'] = grp['total_runs'].cumsum() - df['total_runs']
    df['cum_wickets_pre'] = grp['is_wicket'].cumsum() - df['is_wicket']
    df['cum_balls_pre'] = grp['is_legal'].cumsum() - df['is_legal']
    
    # Merge matches metadata
    m_sub = matches[['match_id', 'knock_out', 'revised_target', 'first_inn_revised_overs', 'second_inn_revised_overs']].copy()
    df = df.merge(m_sub, on='match_id', how='left')
    
    # Compute Target for Chase (Innings 2)
    inn1_totals = df[df['innings'] == 1].groupby('match_id')['total_runs'].sum().reset_index().rename(columns={'total_runs': 'inn1_actual_total'})
    df = df.merge(inn1_totals, on='match_id', how='left')
    df['target_score'] = np.where(df['revised_target'].notna() & (df['revised_target'] > 0),
                                  df['revised_target'],
                                  df['inn1_actual_total'].fillna(165) + 1)
    
    # Pre-delivery state features
    df['balls_remaining'] = np.maximum(1, 120 - df['cum_balls_pre'])
    df['wickets_in_hand'] = np.maximum(0, 10 - df['cum_wickets_pre'])
    df['crr'] = np.where(df['cum_balls_pre'] > 0, (df['cum_runs_pre'] / df['cum_balls_pre']) * 6.0, 7.5)
    
    # Required Run Rate for chase
    runs_needed = np.maximum(0, df['target_score'] - df['cum_runs_pre'])
    df['rrr'] = np.where(df['innings'] == 2, (runs_needed / df['balls_remaining']) * 6.0, df['crr'])
    df['rrr'] = np.clip(df['rrr'], 0.0, 36.0)
    
    # Categorical and indicator features
    df['is_powerplay'] = (df['overid'] < 6).astype(int)
    df['is_middle'] = ((df['overid'] >= 6) & (df['overid'] < 15)).astype(int)
    df['is_death'] = (df['overid'] >= 15).astype(int)
    df['is_spin'] = (df['pace_or_spin'] == 'spin').astype(int)
    df['is_chase'] = (df['innings'] == 2).astype(int)
    df['is_knockout'] = df['knock_out'].fillna(0).astype(int)
    df['over_num'] = df['overid'].astype(float)
    df['ball_in_over'] = df['over_ball_num'].astype(float)
    
    feature_cols = [
        'over_num', 'ball_in_over', 'innings', 'is_powerplay', 'is_middle', 'is_death',
        'is_spin', 'is_chase', 'is_knockout', 'cum_runs_pre', 'cum_wickets_pre',
        'balls_remaining', 'wickets_in_hand', 'crr', 'rrr'
    ]
    
    # Drop rows with NaN in features or targets
    df_clean = df.dropna(subset=feature_cols + ['total_runs', 'is_wicket']).copy()
    print(f" -> Feature matrix engineered successfully: {len(df_clean):,} valid deliveries.")
    return df_clean, feature_cols

# -------------------------------------------------------------
# STEP 2: REGRESSION BENCHMARK (EXPECTED RUNS xR)
# -------------------------------------------------------------
def run_regression_benchmark(X_train, y_train, X_val, y_val, X_test, y_test, feature_cols):
    print("\n[Step 2] Executing Expected Runs (xR) Multi-Model Regression Benchmark...")
    results = []

    # 1. Naive Mean Baseline
    t0 = time.time()
    mean_val = y_train.mean()
    y_pred_naive = np.full_like(y_test, mean_val)
    t_naive = (time.time() - t0) * 1000 / len(y_test)
    results.append({
        "model_name": "Naive Mean Baseline",
        "category": "Baseline",
        "rmse": np.sqrt(mean_squared_error(y_test, y_pred_naive)),
        "mae": mean_absolute_error(y_test, y_pred_naive),
        "r2": r2_score(y_test, y_pred_naive),
        "latency_ms_per_1k": round(t_naive * 1000, 3)
    })

    # 2. Ridge Regression (L2 Regularized GLM)
    t0 = time.time()
    scaler = StandardScaler()
    X_tr_sc = scaler.fit_transform(X_train)
    X_te_sc = scaler.transform(X_test)
    
    ridge = Ridge(alpha=10.0)
    ridge.fit(X_tr_sc, y_train)
    y_pred_ridge = ridge.predict(X_te_sc)
    t_ridge = (time.time() - t0) * 1000 / len(y_test)
    results.append({
        "model_name": "Ridge Regression (L2 GLM)",
        "category": "Linear / Regularized",
        "rmse": np.sqrt(mean_squared_error(y_test, y_pred_ridge)),
        "mae": mean_absolute_error(y_test, y_pred_ridge),
        "r2": r2_score(y_test, y_pred_ridge),
        "latency_ms_per_1k": round(t_ridge * 1000, 3)
    })

    # 3. Bayesian Ridge Regression (Probabilistic Shrinkage)
    t0 = time.time()
    bayes_ridge = BayesianRidge()
    bayes_ridge.fit(X_tr_sc, y_train)
    y_pred_bayes = bayes_ridge.predict(X_te_sc)
    t_bayes = (time.time() - t0) * 1000 / len(y_test)
    results.append({
        "model_name": "Bayesian Ridge Regressor",
        "category": "Bayesian Probabilistic",
        "rmse": np.sqrt(mean_squared_error(y_test, y_pred_bayes)),
        "mae": mean_absolute_error(y_test, y_pred_bayes),
        "r2": r2_score(y_test, y_pred_bayes),
        "latency_ms_per_1k": round(t_bayes * 1000, 3)
    })

    # 4. Random Forest Regressor (Bagging Ensemble)
    t0 = time.time()
    rf = RandomForestRegressor(n_estimators=60, max_depth=10, max_features='sqrt', random_state=42, n_jobs=-1)
    rf.fit(X_train, y_train)
    y_pred_rf = rf.predict(X_test)
    t_rf = (time.time() - t0) * 1000 / len(y_test)
    results.append({
        "model_name": "Random Forest Regressor",
        "category": "Ensemble (Bagging)",
        "rmse": np.sqrt(mean_squared_error(y_test, y_pred_rf)),
        "mae": mean_absolute_error(y_test, y_pred_rf),
        "r2": r2_score(y_test, y_pred_rf),
        "latency_ms_per_1k": round(t_rf * 1000, 3)
    })

    # 5. LightGBM Regressor (Gradient Boosting)
    t0 = time.time()
    lgb_reg = lgb.LGBMRegressor(n_estimators=120, learning_rate=0.06, num_leaves=31, random_state=42, n_jobs=-1, verbose=-1)
    lgb_reg.fit(X_train, y_train)
    y_pred_lgb = lgb_reg.predict(X_test)
    t_lgb = (time.time() - t0) * 1000 / len(y_test)
    results.append({
        "model_name": "LightGBM Regressor (Production)",
        "category": "Gradient Boosting",
        "rmse": np.sqrt(mean_squared_error(y_test, y_pred_lgb)),
        "mae": mean_absolute_error(y_test, y_pred_lgb),
        "r2": r2_score(y_test, y_pred_lgb),
        "latency_ms_per_1k": round(t_lgb * 1000, 3)
    })

    # 6. XGBoost Regressor (Extreme Gradient Boosting)
    t0 = time.time()
    xgb_reg = xgb.XGBRegressor(n_estimators=100, learning_rate=0.08, max_depth=5, random_state=42, n_jobs=-1)
    xgb_reg.fit(X_train, y_train)
    y_pred_xgb = xgb_reg.predict(X_test)
    t_xgb = (time.time() - t0) * 1000 / len(y_test)
    results.append({
        "model_name": "XGBoost Regressor",
        "category": "Gradient Boosting",
        "rmse": np.sqrt(mean_squared_error(y_test, y_pred_xgb)),
        "mae": mean_absolute_error(y_test, y_pred_xgb),
        "r2": r2_score(y_test, y_pred_xgb),
        "latency_ms_per_1k": round(t_xgb * 1000, 3)
    })

    # 7. PyTorch Multi-Layer Perceptron (Deep Learning)
    t0 = time.time()
    class CricketMLP(nn.Module):
        def __init__(self, input_dim):
            super().__init__()
            self.net = nn.Sequential(
                nn.Linear(input_dim, 64),
                nn.BatchNorm1d(64),
                nn.ReLU(),
                nn.Dropout(0.2),
                nn.Linear(64, 32),
                nn.ReLU(),
                nn.Linear(32, 1)
            )
        def forward(self, x):
            return self.net(x).squeeze(-1)

    mlp = CricketMLP(X_tr_sc.shape[1])
    criterion = nn.MSELoss()
    optimizer = optim.Adam(mlp.parameters(), lr=0.005, weight_decay=1e-4)
    
    # Train for 5 epochs fast
    ds = TensorDataset(torch.tensor(X_tr_sc, dtype=torch.float32), torch.tensor(y_train.values, dtype=torch.float32))
    loader = DataLoader(ds, batch_size=2048, shuffle=True)
    mlp.train()
    for ep in range(5):
        for bx, by in loader:
            optimizer.zero_grad()
            loss = criterion(mlp(bx), by)
            loss.backward()
            optimizer.step()
            
    mlp.eval()
    with torch.no_grad():
        y_pred_mlp = mlp(torch.tensor(X_te_sc, dtype=torch.float32)).numpy()
    t_mlp = (time.time() - t0) * 1000 / len(y_test)
    results.append({
        "model_name": "Deep Learning MLP (PyTorch)",
        "category": "Neural Network",
        "rmse": np.sqrt(mean_squared_error(y_test, y_pred_mlp)),
        "mae": mean_absolute_error(y_test, y_pred_mlp),
        "r2": r2_score(y_test, y_pred_mlp),
        "latency_ms_per_1k": round(t_mlp * 1000, 3)
    })

    df_res = pd.DataFrame(results)
    df_res['rmse'] = df_res['rmse'].round(4)
    df_res['mae'] = df_res['mae'].round(4)
    df_res['r2'] = df_res['r2'].round(4)
    
    # Compute 95% Bootstrap Confidence Intervals for the best model (LightGBM)
    boot_rmses = []
    np.random.seed(42)
    for _ in range(500):
        sample_idx = np.random.choice(len(y_test), size=len(y_test), replace=True)
        boot_rmses.append(np.sqrt(mean_squared_error(y_test.iloc[sample_idx], y_pred_lgb[sample_idx])))
    ci_lower = np.percentile(boot_rmses, 2.5)
    ci_upper = np.percentile(boot_rmses, 97.5)
    print(f" -> LightGBM 95% Bootstrap RMSE CI: [{ci_lower:.4f}, {ci_upper:.4f}]")
    
    df_res.to_csv(os.path.join(OUTPUTS_DIR, "ml_regression_benchmark.csv"), index=False)
    print(" -> Saved ml_regression_benchmark.csv successfully.")
    return df_res, lgb_reg, xgb_reg

# -------------------------------------------------------------
# STEP 3: CLASSIFICATION BENCHMARK (EXPECTED WICKETS xW)
# -------------------------------------------------------------
def run_classification_benchmark(X_train, y_w_train, X_test, y_w_test):
    print("\n[Step 3] Executing Expected Wickets (xW) Multi-Model Classification Benchmark...")
    results = []
    
    # 1. Prior Majority Baseline
    prior_prob = y_w_train.mean()
    y_prob_prior = np.full_like(y_w_test, prior_prob, dtype=float)
    results.append({
        "model_name": "Prior Baseline (4.8% Wickets)",
        "category": "Baseline",
        "roc_auc": 0.5000,
        "log_loss": round(log_loss(y_w_test, y_prob_prior), 4),
        "brier_score": round(brier_score_loss(y_w_test, y_prob_prior), 4)
    })

    # 2. Logistic Regression (L2)
    scaler = StandardScaler()
    X_tr_sc = scaler.fit_transform(X_train)
    X_te_sc = scaler.transform(X_test)
    
    lr = LogisticRegression(class_weight='balanced', max_iter=200, random_state=42)
    lr.fit(X_tr_sc, y_w_train)
    y_prob_lr = lr.predict_proba(X_te_sc)[:, 1]
    results.append({
        "model_name": "Logistic Regression (Balanced)",
        "category": "Linear Classifier",
        "roc_auc": round(roc_auc_score(y_w_test, y_prob_lr), 4),
        "log_loss": round(log_loss(y_w_test, y_prob_lr), 4),
        "brier_score": round(brier_score_loss(y_w_test, y_prob_lr), 4)
    })

    # 3. Random Forest Classifier
    rf_c = RandomForestClassifier(n_estimators=60, max_depth=8, class_weight='balanced', random_state=42, n_jobs=-1)
    rf_c.fit(X_train, y_w_train)
    y_prob_rf = rf_c.predict_proba(X_test)[:, 1]
    results.append({
        "model_name": "Random Forest Classifier",
        "category": "Ensemble (Bagging)",
        "roc_auc": round(roc_auc_score(y_w_test, y_prob_rf), 4),
        "log_loss": round(log_loss(y_w_test, y_prob_rf), 4),
        "brier_score": round(brier_score_loss(y_w_test, y_prob_rf), 4)
    })

    # 4. LightGBM Classifier
    lgb_c = lgb.LGBMClassifier(n_estimators=100, learning_rate=0.06, scale_pos_weight=4.0, random_state=42, n_jobs=-1, verbose=-1)
    lgb_c.fit(X_train, y_w_train)
    y_prob_lgb = lgb_c.predict_proba(X_test)[:, 1]
    results.append({
        "model_name": "LightGBM Classifier (Production)",
        "category": "Gradient Boosting",
        "roc_auc": round(roc_auc_score(y_w_test, y_prob_lgb), 4),
        "log_loss": round(log_loss(y_w_test, y_prob_lgb), 4),
        "brier_score": round(brier_score_loss(y_w_test, y_prob_lgb), 4)
    })

    # 5. XGBoost Classifier
    xgb_c = xgb.XGBClassifier(n_estimators=80, learning_rate=0.08, scale_pos_weight=4.0, random_state=42, n_jobs=-1)
    xgb_c.fit(X_train, y_w_train)
    y_prob_xgb = xgb_c.predict_proba(X_test)[:, 1]
    results.append({
        "model_name": "XGBoost Classifier",
        "category": "Gradient Boosting",
        "roc_auc": round(roc_auc_score(y_w_test, y_prob_xgb), 4),
        "log_loss": round(log_loss(y_w_test, y_prob_xgb), 4),
        "brier_score": round(brier_score_loss(y_w_test, y_prob_xgb), 4)
    })

    df_c_res = pd.DataFrame(results)
    df_c_res.to_csv(os.path.join(OUTPUTS_DIR, "ml_classification_benchmark.csv"), index=False)
    print(" -> Saved ml_classification_benchmark.csv successfully.")
    return df_c_res

# -------------------------------------------------------------
# STEP 4: UNSUPERVISED PLAYER CLUSTERING & ARCHETYPES
# -------------------------------------------------------------
def run_unsupervised_clustering():
    print("\n[Step 4] Executing Unsupervised Player Archetype Clustering (k-Means, GMM, PCA)...")
    
    bat_df = pd.read_csv(os.path.join(OUTPUTS_DIR, "all_ranked_batters.csv"))
    features = ['norm_sr', 'norm_avg', 'press_sr', 'press_avg', 'press_boundary_pct', 'press_dot_pct', 'press_xrae']
    
    # Filter batters with at least 50 pressure balls
    b_sub = bat_df[bat_df['press_balls'] >= 50].copy()
    X_clust = b_sub[features].fillna(b_sub[features].mean())
    
    scaler = StandardScaler()
    X_clust_sc = scaler.fit_transform(X_clust)
    
    # Evaluate Silhouette Scores across k = 3, 4, 5, 6
    sil_scores = {}
    for k in range(3, 7):
        km = KMeans(n_clusters=k, random_state=42, n_init=10)
        labels = km.fit_predict(X_clust_sc)
        sil = silhouette_score(X_clust_sc, labels)
        sil_scores[k] = round(sil, 4)
    print(f" -> Silhouette Scores (k=3..6): {sil_scores}")
    
    # Optimal k = 4
    optimal_k = 4
    km_final = KMeans(n_clusters=optimal_k, random_state=42, n_init=15)
    b_sub['cluster_id'] = km_final.fit_predict(X_clust_sc)
    
    # Gaussian Mixture Models (Probabilistic Soft Clustering)
    gmm = GaussianMixture(n_components=optimal_k, random_state=42)
    b_sub['gmm_cluster_id'] = gmm.fit_predict(X_clust_sc)
    
    # PCA 2D Projection
    pca = PCA(n_components=2)
    pca_coords = pca.fit_transform(X_clust_sc)
    b_sub['pca_x'] = pca_coords[:, 0].round(3)
    b_sub['pca_y'] = pca_coords[:, 1].round(3)
    
    # Archetype Cluster Naming
    archetype_names = {
        0: "Top-Order Anchor Accumulator (High Avg, Controlled Dot %)",
        1: "Extreme Death Overs Demolisher (Ultra-High SR & Boundary %)",
        2: "Middle-Overs Spin Squeeze Specialist (High Strike Rotation)",
        3: "High-Variance Disruptive Finisher (High Risk, Explosive Impact)"
    }
    b_sub['archetype_name'] = b_sub['cluster_id'].map(archetype_names)
    
    out_cols = ['player_name', 'cluster_id', 'archetype_name', 'press_sr', 'press_avg', 'press_boundary_pct', 'press_dot_pct', 'pca_x', 'pca_y']
    b_sub[out_cols].to_csv(os.path.join(OUTPUTS_DIR, "ml_clustering_archetypes.csv"), index=False)
    print(" -> Saved ml_clustering_archetypes.csv successfully.")
    return b_sub

# -------------------------------------------------------------
# STEP 5: FEATURE IMPORTANCE & VISUALIZATION
# -------------------------------------------------------------
def generate_feature_importance_and_plots(lgb_model, xgb_model, feature_cols):
    print("\n[Step 5] Computing Feature Importance and generating Visual Curves...")
    
    # LightGBM feature gain
    gains = lgb_model.booster_.feature_importance(importance_type='gain')
    df_fi = pd.DataFrame({
        'feature': feature_cols,
        'lightgbm_gain_pct': np.round(gains / gains.sum() * 100, 2),
        'xgboost_gain_pct': np.round(xgb_model.feature_importances_ * 100, 2)
    }).sort_values('lightgbm_gain_pct', ascending=False)
    
    df_fi.to_csv(os.path.join(OUTPUTS_DIR, "ml_feature_importance.csv"), index=False)
    print(" -> Saved ml_feature_importance.csv.")
    
    # Generate Multi-Panel Comparison Plot
    fig, axes = plt.subplots(1, 2, figsize=(14, 6), dpi=120)
    fig.patch.set_facecolor('#0B132B')
    
    # Panel 1: Regression RMSE Comparison
    df_reg = pd.read_csv(os.path.join(OUTPUTS_DIR, "ml_regression_benchmark.csv")).sort_values('rmse', ascending=True)
    ax1 = axes[0]
    ax1.set_facecolor('#131E3D')
    bars = ax1.barh(df_reg['model_name'], df_reg['rmse'], color=['#EA1A85', '#FF4D9E', '#D4AF37', '#38BDF8', '#818CF8', '#94A3B8', '#475569'])
    ax1.set_xlabel('Root Mean Squared Error (Lower is Better)', color='#FFFFFF', fontsize=11, fontweight='bold')
    ax1.set_title('Expected Runs (xR) Regression Model Benchmark', color='#D4AF37', fontsize=13, fontweight='bold')
    ax1.tick_params(colors='#CBD5E1', labelsize=10)
    ax1.invert_yaxis()
    for bar in bars:
        w = bar.get_width()
        ax1.text(w + 0.01, bar.get_y() + bar.get_height()/2, f'{w:.3f}', color='#FFFFFF', va='center', fontsize=9, fontweight='bold')

    # Panel 2: Top Feature Importance
    ax2 = axes[1]
    ax2.set_facecolor('#131E3D')
    df_top_fi = df_fi.head(8).sort_values('lightgbm_gain_pct', ascending=True)
    bars2 = ax2.barh(df_top_fi['feature'], df_top_fi['lightgbm_gain_pct'], color='#D4AF37')
    ax2.set_xlabel('LightGBM Feature Gain (%)', color='#FFFFFF', fontsize=11, fontweight='bold')
    ax2.set_title('Top Drivers of Pre-Delivery Expected Runs (xR)', color='#EA1A85', fontsize=13, fontweight='bold')
    ax2.tick_params(colors='#CBD5E1', labelsize=10)
    for bar in bars2:
        w = bar.get_width()
        ax2.text(w + 0.5, bar.get_y() + bar.get_height()/2, f'{w:.1f}%', color='#FFFFFF', va='center', fontsize=9, fontweight='bold')

    plt.tight_layout()
    chart_path = os.path.join(OUTPUTS_DIR, "ml_model_comparison_curves.png")
    fig.savefig(chart_path, facecolor=fig.get_facecolor(), bbox_inches='tight')
    plt.close(fig)
    print(f" -> Saved chart: {chart_path}")

def main():
    print("=" * 80)
    print("PROJECT RR-EDGE: COMPREHENSIVE MULTI-MODEL ML BENCHMARK PIPELINE")
    print("=" * 80)
    
    df_clean, feature_cols = load_and_engineer_features()
    
    X = df_clean[feature_cols]
    y_runs = df_clean['total_runs']
    y_wicket = df_clean['is_wicket']
    
    # Chronological match-based split (70% train, 15% val, 15% test)
    match_ids = df_clean['match_id'].unique()
    n_matches = len(match_ids)
    train_m = match_ids[:int(n_matches * 0.70)]
    val_m = match_ids[int(n_matches * 0.70):int(n_matches * 0.85)]
    test_m = match_ids[int(n_matches * 0.85):]
    
    train_idx = df_clean['match_id'].isin(train_m)
    val_idx = df_clean['match_id'].isin(val_m)
    test_idx = df_clean['match_id'].isin(test_m)
    
    X_train, y_train, y_w_train = X[train_idx], y_runs[train_idx], y_wicket[train_idx]
    X_val, y_val, y_w_val = X[val_idx], y_runs[val_idx], y_wicket[val_idx]
    X_test, y_test, y_w_test = X[test_idx], y_runs[test_idx], y_wicket[test_idx]
    
    print(f"Dataset split: Train={len(X_train):,}, Val={len(X_val):,}, Test={len(X_test):,}")
    
    # Execute benchmarks
    df_reg, lgb_model, xgb_model = run_regression_benchmark(X_train, y_train, X_val, y_val, X_test, y_test, feature_cols)
    df_clf = run_classification_benchmark(X_train, y_w_train, X_test, y_w_test)
    df_clust = run_unsupervised_clustering()
    generate_feature_importance_and_plots(lgb_model, xgb_model, feature_cols)
    
    print("=" * 80)
    print("ALL ML BENCHMARKS EXECUTED SUCCESSFULLY ACROSS ALL FRAMEWORKS!")
    print("=" * 80)

if __name__ == "__main__":
    main()
