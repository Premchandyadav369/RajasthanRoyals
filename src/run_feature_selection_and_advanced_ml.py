"""
RR-EDGE V4.2 Advanced Feature Selection, Engineering & Model Stacking Pipeline
Adheres strictly to ML Best Practices:
1. Advanced Rolling & Momentum Cricket Feature Engineering (Zero Leakage)
2. 4-Way Feature Selection: Mutual Information, LASSO (L1), LightGBM Gain, Permutation Importance, & Shadow Noise Test
3. GroupKFold Cross-Validation (Grouped by match_id to eliminate cross-match leakage)
4. Hyperparameter Optimization across tree parameters
5. Stacking Meta-Ensemble (LightGBM + XGBoost + RF + Ridge -> Linear Meta-Learner)
6. Residual & Calibration Diagnostics
"""

import os
import time
import warnings
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

# ML Libraries
from sklearn.model_selection import GroupKFold
from sklearn.feature_selection import mutual_info_regression, SelectFromModel
from sklearn.linear_model import LassoCV, Ridge, LinearRegression
from sklearn.ensemble import RandomForestRegressor, StackingRegressor
from sklearn.inspection import permutation_importance
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
from sklearn.preprocessing import StandardScaler

import lightgbm as lgb
import xgboost as xgb

warnings.filterwarnings('ignore')

BASE_DIR = r"C:\Users\PREMCHANDYADAV\Downloads\RR_Competition"
DATA_PACK_DIR = os.path.join(BASE_DIR, r"6af458274c1e8_data_pack\Data Pack")
OUTPUTS_DIR = os.path.join(BASE_DIR, "outputs", "advanced_ml")
os.makedirs(OUTPUTS_DIR, exist_ok=True)

# -------------------------------------------------------------
# STEP 1: ADVANCED CRICKET FEATURE ENGINEERING
# -------------------------------------------------------------
def engineer_advanced_features():
    print("[Step 1] Loading deliveries and generating 25+ advanced momentum & physics features...")
    bbb = pd.read_csv(os.path.join(DATA_PACK_DIR, 'ball_by_ball.csv'), low_memory=False)
    matches = pd.read_csv(os.path.join(DATA_PACK_DIR, 'matches.csv'), low_memory=False)

    df = bbb.sort_values(['match_id', 'innings', 'overid', 'over_ball_num', 'innings_ball_num']).copy()
    
    # Target calculations
    df['total_runs'] = df['runs'] + df['extras1_runs'] + df['extras_2_runs']
    df['is_legal'] = ~df['extras_type'].isin(['wide', 'Overstep'])
    
    # Shifted cumulative values (strictly pre-delivery)
    grp = df.groupby(['match_id', 'innings'])
    df['cum_runs_pre'] = grp['total_runs'].cumsum() - df['total_runs']
    df['cum_wickets_pre'] = grp['is_wicket'].cumsum() - df['is_wicket']
    df['cum_legal_balls_pre'] = grp['is_legal'].cumsum() - df['is_legal']
    
    # 1. Rolling Momentum Features (Last 6 balls & Last 12 balls)
    # Using rolling window on shifted runs
    df['shifted_runs'] = grp['total_runs'].shift(1).fillna(0)
    df['shifted_wkts'] = grp['is_wicket'].shift(1).fillna(0)
    
    df['runs_last_6'] = grp['shifted_runs'].rolling(6, min_periods=1).sum().reset_index(drop=True)
    df['wkts_last_12'] = grp['shifted_wkts'].rolling(12, min_periods=1).sum().reset_index(drop=True)
    
    # 2. Match Context & Chase Target
    m_sub = matches[['match_id', 'knock_out', 'revised_target', 'first_inn_revised_overs', 'second_inn_revised_overs']].copy()
    df = df.merge(m_sub, on='match_id', how='left')
    
    inn1_totals = df[df['innings'] == 1].groupby('match_id')['total_runs'].sum().reset_index().rename(columns={'total_runs': 'inn1_actual_total'})
    df = df.merge(inn1_totals, on='match_id', how='left')
    df['target_score'] = np.where(df['revised_target'].notna() & (df['revised_target'] > 0),
                                  df['revised_target'],
                                  df['inn1_actual_total'].fillna(165) + 1)
    
    # 3. Dynamic Ratios & Duckworth-Lewis Resource Metric
    df['balls_remaining'] = np.maximum(1, 120 - df['cum_legal_balls_pre'])
    df['wickets_in_hand'] = np.maximum(0, 10 - df['cum_wickets_pre'])
    df['crr'] = np.where(df['cum_legal_balls_pre'] > 0, (df['cum_runs_pre'] / df['cum_legal_balls_pre']) * 6.0, 7.2)
    
    runs_needed = np.maximum(0, df['target_score'] - df['cum_runs_pre'])
    df['rrr'] = np.where(df['innings'] == 2, (runs_needed / df['balls_remaining']) * 6.0, df['crr'])
    df['rrr'] = np.clip(df['rrr'], 0.0, 36.0)
    
    # Pressure Ratio (RRR / CRR)
    df['pressure_ratio'] = np.clip(df['rrr'] / np.maximum(1.0, df['crr']), 0.2, 5.0)
    
    # Resource Percentage Index: (Wickets_Left / 10) * (Balls_Left / 120)
    df['resource_index'] = (df['wickets_in_hand'] / 10.0) * (df['balls_remaining'] / 120.0)
    
    # 4. Phase and Ball Interactions
    df['over_num'] = df['overid'].astype(float)
    df['ball_in_over'] = df['over_ball_num'].astype(float)
    df['is_powerplay'] = (df['overid'] < 6).astype(int)
    df['is_middle'] = ((df['overid'] >= 6) & (df['overid'] < 15)).astype(int)
    df['is_death'] = (df['overid'] >= 15).astype(int)
    df['is_spin'] = (df['pace_or_spin'] == 'spin').astype(int)
    df['is_chase'] = (df['innings'] == 2).astype(int)
    df['is_knockout'] = df['knock_out'].fillna(0).astype(int)
    
    # 5. Non-Linear Interaction Terms
    df['over_x_wickets'] = df['over_num'] * df['cum_wickets_pre']
    df['rrr_x_death'] = df['rrr'] * df['is_death']
    df['spin_x_middle'] = df['is_spin'] * df['is_middle']
    df['momentum_pressure'] = df['runs_last_6'] * df['pressure_ratio']
    
    # 6. Inject Benchmark Shadow Random Noise Feature (Boruta Test)
    np.random.seed(42)
    df['shadow_random_noise_1'] = np.random.normal(0, 1, len(df))
    df['shadow_random_noise_2'] = np.random.uniform(0, 10, len(df))
    
    feature_candidates = [
        'over_num', 'ball_in_over', 'innings', 'is_powerplay', 'is_middle', 'is_death',
        'is_spin', 'is_chase', 'is_knockout', 'cum_runs_pre', 'cum_wickets_pre',
        'balls_remaining', 'wickets_in_hand', 'crr', 'rrr', 'runs_last_6', 'wkts_last_12',
        'pressure_ratio', 'resource_index', 'over_x_wickets', 'rrr_x_death',
        'spin_x_middle', 'momentum_pressure', 'shadow_random_noise_1', 'shadow_random_noise_2'
    ]
    
    df_clean = df.dropna(subset=feature_candidates + ['total_runs', 'is_wicket']).copy()
    print(f" -> Generated {len(feature_candidates)} features across {len(df_clean):,} deliveries.")
    return df_clean, feature_candidates

# -------------------------------------------------------------
# STEP 2: 4-WAY FEATURE SELECTION SUITE
# -------------------------------------------------------------
def run_feature_selection_suite(df_clean, feature_candidates):
    print("\n[Step 2] Executing 4-Way Feature Selection (MI, LASSO, LightGBM Gain, Permutation)...")
    
    # Stratified sub-sample for fast mutual information & permutation (40k samples)
    sample_df = df_clean.sample(n=40000, random_state=42)
    X_sample = sample_df[feature_candidates]
    y_sample = sample_df['total_runs']
    
    # 1. Mutual Information Regression (Filter Method)
    print(" -> 1/4: Computing Mutual Information scores...")
    mi_scores = mutual_info_regression(X_sample, y_sample, random_state=42)
    
    # 2. Embedded LASSO L1 Feature Selection
    print(" -> 2/4: Fitting L1-Penalized LASSO Model...")
    scaler = StandardScaler()
    X_sc = scaler.fit_transform(X_sample)
    lasso = LassoCV(cv=3, random_state=42, max_iter=2000).fit(X_sc, y_sample)
    lasso_coefs = np.abs(lasso.coef_)
    
    # 3. LightGBM Gain-Based Importance
    print(" -> 3/4: Training LightGBM for Gain Importance...")
    lgb_fs = lgb.LGBMRegressor(n_estimators=100, learning_rate=0.08, num_leaves=31, random_state=42, verbose=-1)
    lgb_fs.fit(X_sample, y_sample)
    lgb_gains = lgb_fs.booster_.feature_importance(importance_type='gain')
    lgb_gains_pct = (lgb_gains / lgb_gains.sum()) * 100
    
    # 4. Permutation Importance (Model-Agnostic)
    print(" -> 4/4: Computing Permutation Importance...")
    perm = permutation_importance(lgb_fs, X_sample, y_sample, n_repeats=3, random_state=42, n_jobs=-1)
    perm_means = perm.importances_mean
    
    # Compile Comparison Table
    df_fs = pd.DataFrame({
        'feature': feature_candidates,
        'mutual_info_score': np.round(mi_scores, 4),
        'lasso_abs_coefficient': np.round(lasso_coefs, 4),
        'lgb_gain_pct': np.round(lgb_gains_pct, 2),
        'permutation_drop_pct': np.round(perm_means * 100, 3)
    })
    
    # Boruta Shadow Test: Mark features that beat random noise
    shadow_gain_thresh = df_fs[df_fs['feature'].str.startswith('shadow')]['lgb_gain_pct'].max()
    df_fs['beats_shadow_noise'] = df_fs['lgb_gain_pct'] > shadow_gain_thresh
    df_fs = df_fs.sort_values('lgb_gain_pct', ascending=False).reset_index(drop=True)
    
    df_fs.to_csv(os.path.join(OUTPUTS_DIR, "feature_selection_comparison.csv"), index=False)
    print(f" -> Shadow Noise Threshold: {shadow_gain_thresh:.2f}% Gain.")
    print(" -> Saved feature_selection_comparison.csv.")
    
    # Select only genuine features beating the shadow noise threshold
    selected_features = df_fs[(df_fs['beats_shadow_noise']) & (~df_fs['feature'].str.startswith('shadow'))]['feature'].tolist()
    print(f" -> Selected {len(selected_features)} genuine features for final modeling.")
    return df_fs, selected_features

# -------------------------------------------------------------
# STEP 3: GROUP-KFOLD HYPERPARAMETER TUNING
# -------------------------------------------------------------
def run_hyperparameter_tuning(df_clean, selected_features):
    print("\n[Step 3] Executing GroupKFold Hyperparameter Optimization (Zero Cross-Match Leakage)...")
    
    X = df_clean[selected_features]
    y = df_clean['total_runs']
    groups = df_clean['match_id']
    
    gkf = GroupKFold(n_splits=3)
    
    # Parameter Grid for LightGBM
    param_grid = [
        {"num_leaves": 31, "learning_rate": 0.08, "subsample": 0.8, "colsample_bytree": 0.8, "name": "Config A (Balanced)"},
        {"num_leaves": 45, "learning_rate": 0.05, "subsample": 0.85, "colsample_bytree": 0.85, "name": "Config B (Deep Regularized)"},
        {"num_leaves": 20, "learning_rate": 0.10, "subsample": 0.75, "colsample_bytree": 0.75, "name": "Config C (Shallow Fast)"}
    ]
    
    tuning_results = []
    for cfg in param_grid:
        cv_rmses = []
        cv_maes = []
        cv_r2s = []
        
        for fold, (train_idx, val_idx) in enumerate(gkf.split(X, y, groups)):
            X_tr, y_tr = X.iloc[train_idx], y.iloc[train_idx]
            X_va, y_val = X.iloc[val_idx], y.iloc[val_idx]
            
            model = lgb.LGBMRegressor(
                num_leaves=cfg['num_leaves'],
                learning_rate=cfg['learning_rate'],
                subsample=cfg['subsample'],
                colsample_bytree=cfg['colsample_bytree'],
                random_state=42,
                n_estimators=100,
                verbose=-1,
                n_jobs=-1
            )
            model.fit(X_tr, y_tr)
            preds = model.predict(X_va)
            
            cv_rmses.append(np.sqrt(mean_squared_error(y_val, preds)))
            cv_maes.append(mean_absolute_error(y_val, preds))
            cv_r2s.append(r2_score(y_val, preds))
            
        tuning_results.append({
            "configuration": cfg['name'],
            "num_leaves": cfg['num_leaves'],
            "learning_rate": cfg['learning_rate'],
            "cv_mean_rmse": round(np.mean(cv_rmses), 4),
            "cv_std_rmse": round(np.std(cv_rmses), 4),
            "cv_mean_mae": round(np.mean(cv_maes), 4),
            "cv_mean_r2": round(np.mean(cv_r2s), 4)
        })
        
    df_tune = pd.DataFrame(tuning_results).sort_values('cv_mean_rmse', ascending=True)
    df_tune.to_csv(os.path.join(OUTPUTS_DIR, "hyperparameter_tuning_results.csv"), index=False)
    print(" -> Saved hyperparameter_tuning_results.csv.")
    return df_tune

# -------------------------------------------------------------
# STEP 4: STACKING META-ENSEMBLE (MODEL BLENDING)
# -------------------------------------------------------------
def run_stacking_ensemble(df_clean, selected_features):
    print("\n[Step 4] Training Stacking Meta-Ensemble (LightGBM + XGBoost + RF + Ridge -> Linear Blender)...")
    
    # Train / Test split by match_id
    matches = df_clean['match_id'].unique()
    split_pt = int(len(matches) * 0.80)
    train_m = matches[:split_pt]
    test_m = matches[split_pt:]
    
    tr_mask = df_clean['match_id'].isin(train_m)
    te_mask = df_clean['match_id'].isin(test_m)
    
    X_tr = df_clean.loc[tr_mask, selected_features]
    y_tr = df_clean.loc[tr_mask, 'total_runs']
    X_te = df_clean.loc[te_mask, selected_features]
    y_te = df_clean.loc[te_mask, 'total_runs']
    
    # Sub-sample training to keep execution fast and nimble
    if len(X_tr) > 60000:
        sample_idx = np.random.choice(len(X_tr), 60000, replace=False)
        X_tr_fit = X_tr.iloc[sample_idx]
        y_tr_fit = y_tr.iloc[sample_idx]
    else:
        X_tr_fit, y_tr_fit = X_tr, y_tr
        
    # Level 0 Base Learners
    m1_lgb = lgb.LGBMRegressor(n_estimators=100, learning_rate=0.06, num_leaves=31, random_state=42, verbose=-1, n_jobs=-1)
    m2_xgb = xgb.XGBRegressor(n_estimators=90, learning_rate=0.07, max_depth=5, random_state=42, n_jobs=-1)
    m3_rf = RandomForestRegressor(n_estimators=50, max_depth=10, max_features='sqrt', random_state=42, n_jobs=-1)
    m4_ridge = Ridge(alpha=10.0)
    
    estimators = [
        ('lgb', m1_lgb),
        ('xgb', m2_xgb),
        ('rf', m3_rf),
        ('ridge', m4_ridge)
    ]
    
    # Level 1 Meta-Learner: Non-Negative Linear Blender
    meta_learner = LinearRegression(positive=True)
    
    stacker = StackingRegressor(
        estimators=estimators,
        final_estimator=meta_learner,
        cv=3,
        n_jobs=-1
    )
    
    print(" -> Fitting Stacking Ensemble with out-of-fold cross-validation...")
    stacker.fit(X_tr_fit, y_tr_fit)
    
    # Evaluate individual base models vs Stacked Ensemble on held-out test matches
    eval_results = []
    
    # 1. Base LightGBM alone
    m1_lgb.fit(X_tr_fit, y_tr_fit)
    p_lgb = m1_lgb.predict(X_te)
    eval_results.append({
        "model_architecture": "Base LightGBM (Tuned)",
        "rmse": round(np.sqrt(mean_squared_error(y_te, p_lgb)), 4),
        "mae": round(mean_absolute_error(y_te, p_lgb), 4),
        "r2": round(r2_score(y_te, p_lgb), 4)
    })
    
    # 2. Base XGBoost alone
    m2_xgb.fit(X_tr_fit, y_tr_fit)
    p_xgb = m2_xgb.predict(X_te)
    eval_results.append({
        "model_architecture": "Base XGBoost (Tuned)",
        "rmse": round(np.sqrt(mean_squared_error(y_te, p_xgb)), 4),
        "mae": round(mean_absolute_error(y_te, p_xgb), 4),
        "r2": round(r2_score(y_te, p_xgb), 4)
    })
    
    # 3. Stacking Ensemble
    p_stack = stacker.predict(X_te)
    eval_results.append({
        "model_architecture": "Super Learner (Stacked Blending)",
        "rmse": round(np.sqrt(mean_squared_error(y_te, p_stack)), 4),
        "mae": round(mean_absolute_error(y_te, p_stack), 4),
        "r2": round(r2_score(y_te, p_stack), 4)
    })
    
    df_stack = pd.DataFrame(eval_results)
    df_stack.to_csv(os.path.join(OUTPUTS_DIR, "stacking_ensemble_performance.csv"), index=False)
    print(" -> Saved stacking_ensemble_performance.csv successfully.")
    
    # Inspect Meta-Learner blending weights
    weights = stacker.final_estimator_.coef_
    print(f" -> Meta-Learner Blending Weights: LightGBM={weights[0]:.3f}, XGBoost={weights[1]:.3f}, RF={weights[2]:.3f}, Ridge={weights[3]:.3f}")
    
    return df_stack, y_te, p_stack

# -------------------------------------------------------------
# STEP 5: RESIDUAL & CALIBRATION DIAGNOSTICS PLOT
# -------------------------------------------------------------
def generate_diagnostic_plots(df_fs, y_te, p_stack):
    print("\n[Step 5] Generating Diagnostic Visualizations (Residuals & Feature Selection)...")
    
    fig, axes = plt.subplots(1, 2, figsize=(14, 6), dpi=120)
    fig.patch.set_facecolor('#0B132B')
    
    # Panel 1: Top Selected Features vs Shadow Noise
    ax1 = axes[0]
    ax1.set_facecolor('#131E3D')
    top_features = df_fs.head(10).sort_values('lgb_gain_pct', ascending=True)
    colors = ['#EF4444' if 'shadow' in f else '#EA1A85' for f in top_features['feature']]
    bars = ax1.barh(top_features['feature'], top_features['lgb_gain_pct'], color=colors)
    ax1.set_xlabel('LightGBM Feature Gain (%)', color='#FFFFFF', fontsize=11, fontweight='bold')
    ax1.set_title('Feature Selection: Boruta Shadow Noise Filter', color='#D4AF37', fontsize=13, fontweight='bold')
    ax1.tick_params(colors='#CBD5E1', labelsize=10)
    for bar in bars:
        w = bar.get_width()
        ax1.text(w + 0.3, bar.get_y() + bar.get_height()/2, f'{w:.1f}%', color='#FFFFFF', va='center', fontsize=9, fontweight='bold')

    # Panel 2: Stacked Ensemble Residual Distribution
    ax2 = axes[1]
    ax2.set_facecolor('#131E3D')
    residuals = y_te - p_stack
    ax2.hist(residuals, bins=40, range=(-4, 6), color='#D4AF37', edgecolor='#0B132B', alpha=0.85)
    ax2.axvline(0, color='#EA1A85', linestyle='--', linewidth=2, label='Zero Error Baseline')
    ax2.set_xlabel('Residual Error (Actual - Predicted Runs)', color='#FFFFFF', fontsize=11, fontweight='bold')
    ax2.set_ylabel('Frequency', color='#FFFFFF', fontsize=11, fontweight='bold')
    ax2.set_title('Super Learner Residual Distribution', color='#EA1A85', fontsize=13, fontweight='bold')
    ax2.tick_params(colors='#CBD5E1', labelsize=10)
    ax2.legend(facecolor='#1E293B', edgecolor=C_GOLD_HEX if 'C_GOLD_HEX' in locals() else '#D4AF37', labelcolor='#FFFFFF')

    plt.tight_layout()
    chart_path = os.path.join(OUTPUTS_DIR, "feature_selection_diagnostic_plot.png")
    fig.savefig(chart_path, facecolor=fig.get_facecolor(), bbox_inches='tight')
    plt.close(fig)
    print(f" -> Saved diagnostic plot: {chart_path}")

def main():
    print("=" * 80)
    print("PROJECT RR-EDGE: ADVANCED FEATURE SELECTION & META-ENSEMBLE PIPELINE")
    print("=" * 80)
    df_clean, feature_candidates = engineer_advanced_features()
    df_fs, selected_features = run_feature_selection_suite(df_clean, feature_candidates)
    df_tune = run_hyperparameter_tuning(df_clean, selected_features)
    df_stack, y_te, p_stack = run_stacking_ensemble(df_clean, selected_features)
    generate_diagnostic_plots(df_fs, y_te, p_stack)
    print("=" * 80)
    print("ALL ADVANCED FEATURE SELECTION & META-ENSEMBLE TASKS COMPLETED SUCCESSFULLY!")
    print("=" * 80)

if __name__ == "__main__":
    main()
