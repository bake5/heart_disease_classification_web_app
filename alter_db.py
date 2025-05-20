# -*- coding: utf-8 -*-
"""
Created on Tue May 20 09:27:53 2025

@author: novbuddy
"""

import sqlite3

conn = sqlite3.connect("database.db")
cursor = conn.cursor()

# Tambahkan kolom baru
cursor.execute("ALTER TABLE prediksi ADD COLUMN nama TEXT")

conn.commit()
conn.close()
print("Kolom 'nama' berhasil ditambahkan.")
