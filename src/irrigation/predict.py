
"""
Author: Harmanpreet Singh
Project: Agro AI Decision Support System — Final Year Project
Institution: TIET, Patiala
"""
import warnings
warnings.filterwarnings('ignore')
import pickle
import numpy as np
import os


# CONFIGURATION


MODELS_DIR = 'models'


# LOAD SAVED ARTIFACTS


def load_artifacts():
    artifacts = {}
    files = {
        'model'         : 'irrigation_model.pkl',
        'label_encoders': 'label_encoders.pkl',
        'feature_names' : 'feature_names.pkl',
        'target_map'    : 'target_map.pkl',
    }
    for key, filename in files.items():
        path = os.path.join(MODELS_DIR, filename)
        with open(path, 'rb') as f:
            artifacts[key] = pickle.load(f)

    # Reverse target map: 0→Low, 1→Medium, 2→High
    artifacts['reverse_target_map'] = {
        v: k for k, v in artifacts['target_map'].items()
    }
    print(" All artifacts loaded successfully.")
    return artifacts


# PREDICT FUNCTION


def predict_irrigation(input_data: dict, artifacts: dict) -> str:
    """
    Takes a dictionary of farm conditions and returns
    irrigation need: Low, Medium, or High.

    Args:
        input_data : dict with feature names as keys
        artifacts  : loaded model artifacts

    Returns:
        str — 'Low', 'Medium', or 'High'
    """
    model          = artifacts['model']
    label_encoders = artifacts['label_encoders']
    feature_names  = artifacts['feature_names']
    reverse_map    = artifacts['reverse_target_map']

    # Encode categorical fields using saved encoders
    processed = input_data.copy()
    for col, le in label_encoders.items():
        if col in processed:
            processed[col] = le.transform([processed[col]])[0]

    # Build feature vector in correct order
    feature_vector = np.array([[processed[f] for f in feature_names]])

    # Predict
    prediction_encoded = model.predict(feature_vector)[0]
    prediction_label   = reverse_map[prediction_encoded]

    return prediction_label


# TEST WITH SAMPLE INPUTS


def main():
    print("=" * 50)
    print("  Agro AI — Irrigation Predictor")
    print("=" * 50)

    artifacts = load_artifacts()

    # --- Test Case 1: Dry, hot conditions → expect High ---
    test_case_1 = {
        'Soil_Moisture'          : 10.0,
        'Temperature_C'          : 42.0,
        'Humidity'               : 20.0,
        'Rainfall_mm'            : 5.0,
        'Soil_pH'                : 6.5,
        'Sunlight_Hours'         : 12.0,
        'Wind_Speed_kmh'         : 25.0,
        'Organic_Carbon'         : 0.3,
        'Electrical_Conductivity': 1.5,
        'Previous_Irrigation_mm' : 2.0,
        'Field_Area_hectare'     : 3.0,
        'Soil_Type'              : 'Sandy',
        'Crop_Type'              : 'Wheat',
        'Crop_Growth_Stage'      : 'Flowering',
        'Season'                 : 'Rabi',
        'Mulching_Used'          : 'No',
        'Region'                 : 'North',
    }

    # --- Test Case 2: Wet, cool conditions → expect Low ---
    test_case_2 = {
        'Soil_Moisture'          : 55.0,
        'Temperature_C'          : 18.0,
        'Humidity'               : 85.0,
        'Rainfall_mm'            : 1800.0,
        'Soil_pH'                : 7.0,
        'Sunlight_Hours'         : 4.0,
        'Wind_Speed_kmh'         : 5.0,
        'Organic_Carbon'         : 1.2,
        'Electrical_Conductivity': 0.8,
        'Previous_Irrigation_mm' : 60.0,
        'Field_Area_hectare'     : 5.0,
        'Soil_Type'              : 'Clay',
        'Crop_Type'              : 'Rice',
        'Crop_Growth_Stage'      : 'Vegetative',
        'Season'                 : 'Kharif',
        'Mulching_Used'          : 'Yes',
        'Region'                 : 'South',
    }

    # --- Test Case 3: Moderate conditions → expect Medium ---
    test_case_3 = {
        'Soil_Moisture'          : 30.0,
        'Temperature_C'          : 28.0,
        'Humidity'               : 55.0,
        'Rainfall_mm'            : 400.0,
        'Soil_pH'                : 6.8,
        'Sunlight_Hours'         : 7.0,
        'Wind_Speed_kmh'         : 12.0,
        'Organic_Carbon'         : 0.8,
        'Electrical_Conductivity': 1.2,
        'Previous_Irrigation_mm' : 25.0,
        'Field_Area_hectare'     : 4.0,
        'Soil_Type'              : 'Clay',
        'Crop_Type'              : 'Maize',
        'Crop_Growth_Stage'      : 'Sowing',
        'Season'                 : 'Zaid',
        'Mulching_Used'          : 'Yes',
        'Region'                 : 'Central',
    }

    print("\n--- Running 3 test predictions ---\n")

    for i, test_case in enumerate([test_case_1, test_case_2, test_case_3], 1):
        result = predict_irrigation(test_case, artifacts)
        print(f"Test {i}: Irrigation Need → {result}")

    print("\n" + "=" * 50)
    print("  Prediction complete!")
    print("=" * 50)


if __name__ == '__main__':
    main()