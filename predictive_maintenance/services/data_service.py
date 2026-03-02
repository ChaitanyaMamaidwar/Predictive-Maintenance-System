from database.db import get_connection

def add_machine(name, location, install_date):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO machines (name, location, install_date) VALUES (?, ?, ?)",
        (name, location, install_date)
    )
    conn.commit()
    conn.close()

def get_all_machines():
    conn = get_connection()
    machines = conn.execute("SELECT * FROM machines").fetchall()
    conn.close()
    return machines

def add_sensor_data(machine_id, temp, vib, pres, hum, label):
    conn = get_connection()
    conn.execute("""
        INSERT INTO sensor_data (machine_id, temperature, vibration, pressure, humidity, label)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (machine_id, temp, vib, pres, hum, label))
    conn.commit()
    conn.close()

def get_training_data():
    conn = get_connection()
    data = conn.execute("""
        SELECT temperature, vibration, pressure, humidity, label
        FROM sensor_data
    """).fetchall()
    conn.close()
    return data