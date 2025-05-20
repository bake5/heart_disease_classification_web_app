# -*- coding: utf-8 -*-
"""
Created on Mon May 19 09:57:49 2025

@author: novbuddy
"""

import sqlite3

def init_db():
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS prediksi (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            age REAL,
            sex TEXT,
            cp TEXT,
            trestbps REAL,
            chol REAL,
            fbs TEXT,
            restecg TEXT,
            thalach REAL,
            exang TEXT,
            oldpeak REAL,
            slope TEXT,
            ca REAL,
            thal TEXT,
            hasil TEXT
        )
    """)
    conn.commit()
    conn.close()
    print("✅ Tabel 'prediksi' berhasil dibuat di database.db")

if __name__ == "__main__":
    init_db()
