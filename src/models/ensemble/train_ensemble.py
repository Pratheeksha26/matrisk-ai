import pandas as pd
import xgboost as xgb
import os
import sys

# Ensure the root directory is in the python path
sys.path.append(os.getcwd())
import lightgbm as lgb
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error
import optuna
import mlflow
import os

def objective_xgb(trial, X, y):
    params = {
        'n_estimators': trial.suggest_int('n_estimators', 100, 1000),
        'max_depth': trial.suggest_int('max_depth', 3, 10),
        'learning_rate': trial.suggest_float('learning_rate', 0.01, 0.3),
        'subsample': trial.suggest_float('subsample', 0.5, 1.0),
        'colsample_bytree': trial.suggest_float('colsample_bytree', 0.3, 1.0),
    }
    
    X_train, X_val, y_train, y_val = train_test_split(X, y, test_size=0.2)
    model = xgb.XGBRegressor(**params)
    model.fit(X_train, y_train)
    preds = model.predict(X_val)
    return mean_absolute_error(y_val, preds)

def train_ensemble_baselines(data_path, target_col):
    df = pd.read_csv(data_path)
    # Drop non-feature columns
    X = df.drop(columns=[target_col, 'composition', 'formula_pretty', 'material_id'], errors='ignore')
    y = df[target_col]
    
    # Optuna study for XGBoost
    study = optuna.create_study(direction='minimize')
    study.optimize(lambda trial: objective_xgb(trial, X, y), n_trials=20)
    
    print(f"Best params for XGBoost: {study.best_params}")
    
    # Log to MLflow
    mlflow.set_experiment("matrisk-ensemble")
    with mlflow.start_run(run_name="xgboost_baseline"):
        mlflow.log_params(study.best_params)
        model = xgb.XGBRegressor(**study.best_params)
        model.fit(X, y)
        mlflow.sklearn.log_model(model, "xgboost_model")
        
    return model

if __name__ == "__main__":
    processed_data = "data/processed/material_features_final.csv"
    if os.path.exists(processed_data):
        # Example: predict formation energy
        train_ensemble_baselines(processed_data, 'formation_energy_per_atom')
