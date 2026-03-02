from flask import Flask, redirect, render_template, request, url_for

from config import SECRET_KEY
from database.db import get_connection, init_db
from services.health_service import calculate_health_score
from services.prediction_service import predict


app = Flask(__name__)
app.config["SECRET_KEY"] = SECRET_KEY


def _to_float(value, default=0.0):
    try:
        return float(value)
    except (TypeError, ValueError):
        return default


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/add_machine", methods=["GET", "POST"])
def add_machine():
    if request.method == "POST":
        name = request.form.get("name", "").strip()
        location = request.form.get("location", "").strip()
        install_date = request.form.get("install_date", "").strip()
        temperature = _to_float(request.form.get("temperature"))
        pressure = _to_float(request.form.get("pressure"))
        vibration = _to_float(request.form.get("vibration"))
        humidity = _to_float(request.form.get("humidity"), default=None)

        if (
            not name
            or not location
            or not install_date
            or temperature is None
            or pressure is None
            or vibration is None
            or humidity is None
        ):
            return "Missing required machine details.", 400

        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute(
            "INSERT INTO machines (name, location, install_date) VALUES (?, ?, ?)",
            (name, location, install_date),
        )
        machine_id = cursor.lastrowid

        cursor.execute(
            """
            INSERT INTO sensor_data
            (machine_id, temperature, vibration, pressure, humidity, label)
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            (machine_id, temperature, vibration, pressure, humidity, 0),
        )

        conn.commit()
        conn.close()

        return redirect(url_for("check_machine"))

    return render_template("add_machine.html")


@app.route("/check_machine", methods=["GET", "POST"])
def check_machine():
    conn = get_connection()
    machines = conn.execute("SELECT * FROM machines ORDER BY id DESC").fetchall()

    if request.method == "POST":
        machine_id = request.form.get("machine_id")
        temperature = _to_float(request.form.get("temperature"), default=None)
        pressure = _to_float(request.form.get("pressure"), default=None)
        vibration = _to_float(request.form.get("vibration"), default=None)
        humidity = _to_float(request.form.get("humidity"), default=None)

        if not machine_id:
            conn.close()
            return "No machine selected!", 400

        if (
            temperature is None
            or pressure is None
            or vibration is None
            or humidity is None
        ):
            conn.close()
            return "Current sensor values are required.", 400

        machine = conn.execute(
            "SELECT id FROM machines WHERE id = ?",
            (machine_id,),
        ).fetchone()
        if machine is None:
            conn.close()
            return "Machine not found.", 404

        conn.execute(
            """
            INSERT INTO sensor_data
            (machine_id, temperature, vibration, pressure, humidity, label)
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            (machine_id, temperature, vibration, pressure, humidity, 0),
        )
        conn.commit()
        conn.close()

        return redirect(url_for("machine_result", machine_id=machine_id))

    conn.close()
    return render_template("check_machine.html", machines=machines)


@app.route("/machine/<int:machine_id>")
def machine_result(machine_id):
    conn = get_connection()

    machine = conn.execute(
        "SELECT * FROM machines WHERE id = ?",
        (machine_id,),
    ).fetchone()
    if machine is None:
        conn.close()
        return "Machine not found.", 404

    latest = conn.execute(
        """
        SELECT temperature, vibration, pressure, humidity
        FROM sensor_data
        WHERE machine_id = ?
        ORDER BY created_at DESC, id DESC
        LIMIT 1
        """,
        (machine_id,),
    ).fetchone()

    conn.close()

    if latest is None:
        return "No sensor data available for this machine.", 404

    features = [
        latest["temperature"],
        latest["vibration"],
        latest["pressure"],
        latest["humidity"] if latest["humidity"] is not None else 0.0,
    ]
    probability = predict(features)

    if probability is None:
        return "Model not found. Train the model first.", 500

    health_score = calculate_health_score(probability)
    result = "Failure Risk" if probability >= 0.5 else "Healthy"

    return render_template(
        "dashboard.html",
        machine=machine,
        result=result,
        health_score=health_score,
        failure_probability=round(probability * 100, 2),
    )


if __name__ == "__main__":
    init_db()
    app.run(debug=True)
