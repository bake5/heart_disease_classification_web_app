# -*- coding: utf-8 -*-
"""
Created on Sat May 17 05:51:59 2025

@author: novbuddy
"""

import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.metrics import classification_report
import joblib

df = pd.read_csv("heart_disease_uci.csv")  # pastikan file ini ada di direktori yang sama

# Salin dataframe
df_clean = df.copy()

# 1. Drop kolom tidak relevan
df_clean.drop(columns=["id", "dataset"], inplace=True)

# 2. Encode fitur kategorikal
categorical_cols = ["sex", "cp", "fbs", "restecg", "exang", "slope", "thal"]
for col in categorical_cols:
    df_clean[col] = LabelEncoder().fit_transform(df_clean[col].astype(str))

# 3. Tangani missing values (jika ada)
df_clean = df_clean.dropna()

# 4. Pisahkan fitur dan target
X = df_clean.drop("num", axis=1)
y = df_clean["num"]

# 5. Standardisasi fitur numerik
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# 6. Split data
X_train, X_test, y_train, y_test = train_test_split(X_scaled, y, stratify=y, test_size=0.2, random_state=42)

# 7. Latih model logistic regression multi-class
model = LogisticRegression(multi_class="multinomial", solver="lbfgs", max_iter=1000)
model.fit(X_train, y_train)

# 8. Evaluasi performa
y_pred = model.predict(X_test)
report = classification_report(y_test, y_pred, output_dict=True)

# 9. Simpan model dan scaler
joblib.dump(model, "model.pkl")
joblib.dump(scaler, "scaler.pkl")

report
