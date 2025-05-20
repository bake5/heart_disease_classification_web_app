# -*- coding: utf-8 -*-
"""
Created on Mon May 19 10:51:50 2025

@author: novbuddy
"""

import sqlite3
import pandas as pd

conn = sqlite3.connect("database.db")
df = pd.read_sql_query("SELECT * FROM prediksi", conn)
conn.close()

print(df)