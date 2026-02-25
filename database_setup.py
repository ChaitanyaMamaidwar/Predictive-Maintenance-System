import sqlite3

# Create database in current folder
conn = sqlite3.connect("database.db")

cursor = conn.cursor()

# Create machines table
cursor.execute("""
CREATE TABLE IF NOT EXISTS machines (
    machine_id TEXT PRIMARY KEY,
    machine_name TEXT,
    location TEXT,
    install_date TEXT
)
""")

# Create sensor data table
cursor.execute("""
CREATE TABLE IF NOT EXISTS sensor_data (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    machine_id TEXT,
    temperature REAL,
    vibration REAL,
    pressure REAL,
    prediction TEXT,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY(machine_id) REFERENCES machines(machine_id)
)
""")

conn.commit()
conn.close()

print("Database created successfully!")