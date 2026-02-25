from flask import Flask, render_template, request
import sqlite3
import datetime
import os

app = Flask(__name__)

DATABASE = "database/database.db"


# ================================
# DATABASE CONNECTION
# ================================
def get_db():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn


# ================================
# HOME PAGE
# ================================
@app.route("/")
def home():

    conn = get_db()

    machines = conn.execute(
        "SELECT * FROM machines ORDER BY created_at DESC"
    ).fetchall()

    conn.close()

    return render_template("index.html", machines=machines)


# ================================
# ADD MACHINE
# ================================
@app.route("/add_machine", methods=["POST"])
def add_machine():

    machine_id = request.form["machine_id"]
    machine_name = request.form["machine_name"]
    location = request.form["location"]

    conn = get_db()

    conn.execute(
        """
        INSERT INTO machines (machine_id, machine_name, location)
        VALUES (?, ?, ?)
        """,
        (machine_id, machine_name, location),
    )

    conn.commit()
    conn.close()

    return render_template(
        "index.html",
        message="Machine added successfully!"
    )


# ================================
# PREDICT MACHINE FAILURE
# ================================
@app.route("/predict", methods=["POST"])
def predict():

    machine_id = request.form["machine_id"]
    temperature = float(request.form["temperature"])
    vibration = float(request.form["vibration"])
    pressure = float(request.form["pressure"])

    # ============================
    # SIMPLE INDUSTRY LOGIC
    # ============================

    risk_score = (temperature * 0.4) + (vibration * 0.4) + (pressure * 0.2)

    if risk_score > 70:
        prediction = "HIGH RISK - Failure likely"
        status = "FAIL"
    elif risk_score > 50:
        prediction = "MEDIUM RISK - Maintenance needed"
        status = "WARNING"
    else:
        prediction = "LOW RISK - Machine healthy"
        status = "SAFE"

    timestamp = datetime.datetime.now()

    # ============================
    # SAVE TO DATABASE
    # ============================

    conn = get_db()

    conn.execute(
        """
        INSERT INTO sensor_data
        (machine_id, temperature, vibration, pressure, prediction, status, timestamp)
        VALUES (?, ?, ?, ?, ?, ?, ?)
        """,
        (
            machine_id,
            temperature,
            vibration,
            pressure,
            prediction,
            status,
            timestamp,
        ),
    )

    conn.commit()
    conn.close()

    return render_template(
        "index.html",
        result=prediction,
        machine_id=machine_id,
        temperature=temperature,
        vibration=vibration,
        pressure=pressure,
        status=status
    )


# ================================
# MACHINE DASHBOARD
# ================================
@app.route("/dashboard/<machine_id>")
def dashboard(machine_id):

    conn = get_db()

    data = conn.execute(
        """
        SELECT *
        FROM sensor_data
        WHERE machine_id = ?
        ORDER BY timestamp DESC
        LIMIT 20
        """,
        (machine_id,),
    ).fetchall()

    conn.close()

    return render_template(
        "dashboard.html",
        data=data,
        machine_id=machine_id
    )


# ================================
# RUN APP
# ================================
if __name__ == "__main__":
    app.run(debug=True)