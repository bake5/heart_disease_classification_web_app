from flask import Flask, render_template, request, redirect, send_file
from utils.predict import predict_condition
import pandas as pd
import sqlite3
import io

app = Flask(__name__)

def get_db_connection():
    conn = sqlite3.connect("database.db")
    conn.row_factory = sqlite3.Row
    return conn

@app.route("/", methods=["GET"])
def index():
    conn = get_db_connection()
    history = conn.execute("SELECT * FROM prediksi ORDER BY id DESC").fetchall()
    conn.close()

    cp_map = {
        "0": "Typical Angina",
        "1": "Atypical Angina",
        "2": "Non-Anginal Pain",
        "3": "Asymptomatic"
    }
    slope_map = {
        "0": "Upsloping",
        "1": "Flat",
        "2": "Downsloping"
    }
    thal_map = {
        "0": "Normal",
        "1": "Fixed Defect",
        "2": "Reversable Defect"
    }

    history_clean = []
    for row in history:
        row = dict(row)
        row["cp"] = cp_map.get(str(row["cp"]), row["cp"])
        row["fbs"] = "Ya" if row["fbs"] == "True" else "Tidak"
        row["exang"] = "Ya" if row["exang"] == "True" else "Tidak"
        row["restecg"] = "Normal" if row["restecg"] == "0" else "Abnormal"
        row["slope"] = slope_map.get(str(row["slope"]), row["slope"])
        row["thal"] = thal_map.get(str(row["thal"]), row["thal"])
        history_clean.append(row)

    return render_template("form.html", history=history_clean)

@app.route("/predict", methods=["POST"])
def predict():
    try:
        input_data = {
            "nama": request.form["nama"],
            "age": float(request.form["age"]),
            "sex": request.form["sex"],
            "cp": request.form["cp"],
            "trestbps": float(request.form["trestbps"]),
            "chol": float(request.form["chol"]),
            "fbs": request.form["fbs"],
            "restecg": request.form["restecg"],
            "thalch": float(request.form["thalch"]),
            "exang": request.form["exang"],
            "oldpeak": float(request.form["oldpeak"]),
            "slope": request.form["slope"],
            "ca": float(request.form["ca"]),
            "thal": request.form["thal"]
        }

        # Pisahkan data untuk prediksi (tanpa nama)
        input_predict = input_data.copy()
        del input_predict["nama"]

        hasil = predict_condition(input_predict)

        # Simpan ke database
        conn = get_db_connection()
        conn.execute("""
            INSERT INTO prediksi (nama, age, sex, cp, trestbps, chol, fbs, restecg,
                                  thalach, exang, oldpeak, slope, ca, thal, hasil)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            input_data["nama"], input_data["age"], input_data["sex"], input_data["cp"],
            input_data["trestbps"], input_data["chol"], input_data["fbs"], input_data["restecg"],
            input_data["thalch"], input_data["exang"], input_data["oldpeak"], input_data["slope"],
            input_data["ca"], input_data["thal"], hasil
        ))
        conn.commit()
        conn.close()

        #return render_template("form.html", result=f"Tingkat Penyakit Jantung: {hasil}")
        return redirect("/")

    except Exception as e:
        return render_template("form.html", result=f"Error: {str(e)}")

@app.route("/delete/<int:id>", methods=["POST"])
def delete(id):
    conn = get_db_connection()
    conn.execute("DELETE FROM prediksi WHERE id = ?", (id,))
    conn.commit()
    conn.close()
    return redirect("/")

@app.route("/reset", methods=["POST"])
def reset():
    conn = get_db_connection()
    conn.execute("DELETE FROM prediksi")
    conn.commit()
    conn.close()
    return redirect("/")

@app.route("/download", methods=["GET"])
def download():
    conn = get_db_connection()
    df = pd.read_sql_query("SELECT * FROM prediksi", conn)
    conn.close()
    if df.empty:
        return redirect("/")
    buffer = io.StringIO()
    df.to_csv(buffer, index=False)
    buffer.seek(0)
    return send_file(
        io.BytesIO(buffer.getvalue().encode()),
        mimetype="text/csv",
        as_attachment=True,
        download_name="riwayat_prediksi.csv"
    )

@app.route("/edit/<int:id>", methods=["GET", "POST"])
def edit(id):
    conn = get_db_connection()
    if request.method == "POST":
        input_data = {
            "nama": request.form["nama"],
            "age": float(request.form["age"]),
            "sex": request.form["sex"],
            "cp": request.form["cp"],
            "trestbps": float(request.form["trestbps"]),
            "chol": float(request.form["chol"]),
            "fbs": request.form["fbs"],
            "restecg": request.form["restecg"],
            "thalch": float(request.form["thalch"]),
            "exang": request.form["exang"],
            "oldpeak": float(request.form["oldpeak"]),
            "slope": request.form["slope"],
            "ca": float(request.form["ca"]),
            "thal": request.form["thal"]
        }

        # Buat salinan tanpa 'nama' untuk prediksi
        input_predict = input_data.copy()
        del input_predict["nama"]

        from utils.predict import predict_condition
        hasil = predict_condition(input_predict)

        conn.execute("""
            UPDATE prediksi
            SET nama=?, age=?, sex=?, cp=?, trestbps=?, chol=?, fbs=?, restecg=?,
                thalach=?, exang=?, oldpeak=?, slope=?, ca=?, thal=?, hasil=?
            WHERE id=?
        """, (
            input_data["nama"], input_data["age"], input_data["sex"], input_data["cp"],
            input_data["trestbps"], input_data["chol"], input_data["fbs"], input_data["restecg"],
            input_data["thalch"], input_data["exang"], input_data["oldpeak"], input_data["slope"],
            input_data["ca"], input_data["thal"], hasil, id
        ))
        conn.commit()
        conn.close()
        return redirect("/")
    else:
        row = conn.execute("SELECT * FROM prediksi WHERE id = ?", (id,)).fetchone()
        conn.close()
        if row is None:
            return "Data tidak ditemukan", 404
        return render_template("edit.html", row=row)

if __name__ == "__main__":
    app.run(debug=True, port=1000, use_reloader=False)