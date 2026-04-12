"""
Irrigation Need Predictor — Training Script
Module 1 of the Agro AI Decision Support System

Trains a Decision Tree classifier to predict irrigation need
(Low / Medium / High) based on soil and environmental conditions.

Usage:
    python src/irrigation/train_model.py
"""

import os
import pickle
import warnings
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import accuracy_score, classification_report

warnings.filterwarnings('ignore')


# ─────────────────────────────────────────
# CONFIGURATION
# ─────────────────────────────────────────

DATA_PATH   = 'data/irrigation.csv'
MODELS_DIR  = 'models'

NUMERIC_FEATURES = [
    'Soil_Moisture',
    'Temperature_C',
    'Humidity',
    'Rainfall_mm',
    'Soil_pH',
    'Sunlight_Hours',
    'Wind_Speed_kmh',
    'Organic_Carbon',
    'Electrical_Conductivity',
    'Previous_Irrigation_mm',
    'Field_Area_hectare'
]

CATEGORICAL_FEATURES = [
    'Soil_Type',
    'Crop_Type',
    'Crop_Growth_Stage',
    'Season',
    'Mulching_Used',
    'Region'
]

TARGET_COLUMN = 'Irrigation_Need'
TARGET_MAP    = {'Low': 0, 'Medium': 1, 'High': 2}


# ─────────────────────────────────────────
# STEP 1 — LOAD DATA
# ─────────────────────────────────────────

def load_data(path):
    print(f"[1/5] Loading data from {path}...")
    df = pd.read_csv(path)
    print(f"      Shape: {df.shape}")
    print(f"      Target distribution:\n{df[TARGET_COLUMN].value_counts().to_string()}")
    return df


# ─────────────────────────────────────────
# STEP 2 — PREPROCESS
# ─────────────────────────────────────────

def preprocess(df):
    print("\n[2/5] Preprocessing...")
    df_model = df.copy()
    le_dict = {}

    # Encode categorical input features
    for col in CATEGORICAL_FEATURES:
        le = LabelEncoder()
        df_model[col] = le.fit_transform(df_model[col])
        le_dict[col] = le

    # Encode target variable
    df_model[TARGET_COLUMN] = df_model[TARGET_COLUMN].map(TARGET_MAP)

    all_features = NUMERIC_FEATURES + CATEGORICAL_FEATURES
    X = df_model[all_features]
    y = df_model[TARGET_COLUMN]

    print(f"      Features used: {len(all_features)}")
    print(f"      X shape: {X.shape}, y shape: {y.shape}")
    return X, y, le_dict, all_features


# ─────────────────────────────────────────
# STEP 3 — SPLIT
# ─────────────────────────────────────────

def split_data(X, y):
    print("\n[3/5] Splitting data (80% train / 20% test)...")
    X_train, X_test, y_train, y_test = train_test_split(
        X, y,
        test_size=0.2,
        random_state=42,
        stratify=y
    )
    print(f"      Train: {X_train.shape[0]} samples")
    print(f"      Test:  {X_test.shape[0]} samples")
    return X_train, X_test, y_train, y_test


# ─────────────────────────────────────────
# STEP 4 — TRAIN
# ─────────────────────────────────────────

def train_model(X_train, y_train):
    print("\n[4/5] Training Decision Tree...")
    model = DecisionTreeClassifier(
        random_state=42,
        class_weight='balanced'
    )
    model.fit(X_train, y_train)
    print("      Training complete.")
    return model


# ─────────────────────────────────────────
# STEP 5 — EVALUATE
# ─────────────────────────────────────────

def evaluate_model(model, X_test, y_test):
    print("\n[5/5] Evaluating model...")
    preds = model.predict(X_test)
    acc = accuracy_score(y_test, preds)
    report = classification_report(y_test, preds, target_names=['Low', 'Medium', 'High'])
    print(f"\n      Accuracy: {acc * 100:.2f}%")
    print(f"\n      Classification Report:\n{report}")
    return acc


# ─────────────────────────────────────────
# SAVE ARTIFACTS
# ─────────────────────────────────────────

def save_artifacts(model, le_dict, all_features):
    os.makedirs(MODELS_DIR, exist_ok=True)

    artifacts = {
        'irrigation_model.pkl' : model,
        'label_encoders.pkl'   : le_dict,
        'feature_names.pkl'    : all_features,
        'target_map.pkl'       : TARGET_MAP,
    }

    for filename, obj in artifacts.items():
        path = os.path.join(MODELS_DIR, filename)
        with open(path, 'wb') as f:
            pickle.dump(obj, f)
        print(f"  ✅ Saved → {path}")


# ─────────────────────────────────────────
# MAIN
# ─────────────────────────────────────────

def main():
    print("=" * 50)
    print("  Agro AI — Irrigation Model Training")
    print("=" * 50)

    df                              = load_data(DATA_PATH)
    X, y, le_dict, all_features     = preprocess(df)
    X_train, X_test, y_train, y_test = split_data(X, y)
    model                           = train_model(X_train, y_train)
    evaluate_model(model, X_test, y_test)

    print("\nSaving artifacts...")
    save_artifacts(model, le_dict, all_features)

    print("\n" + "=" * 50)
    print("  Training complete! Model ready.")
    print("=" * 50)


if __name__ == '__main__':
    main()yes 