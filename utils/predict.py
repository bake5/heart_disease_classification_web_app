import joblib
import numpy as np
import pandas as pd

# Load model and encoder once
model = joblib.load("model.pkl")
scaler = joblib.load("scaler.pkl")

'''
print("Koefisien tiap fitur:\n", model.coef_)
print("Intercept:\n", model.intercept_)
print("Kelas target:\n", model.classes_)
print("Mean fitur:\n", scaler.mean_)
print("Skala (std):\n", scaler.scale_)
'''

# Mapping kategori ke angka sesuai training
def encode_input(data):
    mapping = {
        "sex": {"Male": 1, "Female": 0},
        "cp": {"typical angina": 0, "atypical angina": 1, "non-anginal pain": 2, "asymptomatic": 3},
        "fbs": {"True": 1, "False": 0},
        "restecg": {"normal": 0, "abnormal": 1},
        "exang": {"True": 1, "False": 0},
        "slope": {"upsloping": 0, "flat": 1, "downsloping": 2},
        "thal": {"normal": 1, "fixed defect": 2, "reversable defect": 3}
    }
    for key, val in mapping.items():
        data[key] = val[data[key]]
    return data

def predict_condition(input_data):
    encoded = encode_input(input_data)
    df = pd.DataFrame([encoded])
    scaled = scaler.transform(df)
    prediction = model.predict(scaled)[0]
    return f"Tingkat Penyakit Jantung: {prediction}"