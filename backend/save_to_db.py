import sqlite3
import os

DB_PATH = os.getenv('DB_PATH')
HOST_DB_PATH = os.getenv('HOST_DB_PATH')

print(f"DB Path: {DB_PATH}")
print(f"Host DB Path: {HOST_DB_PATH}")

def save_telemetry_data(data):
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()

        cursor.execute('''
            INSERT INTO telemetry (
                car_id, speed, rpm, lap_time, gear,
                latitude, longitude, timestamp
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            data.get("car_id"),
            data.get("speed"),
            data.get("rpm"),
            data.get("lap_time"),
            data.get("gear"),
            data["track_position"].get("lat"),
            data["track_position"].get("lon"),
            data.get("timestamp")
        ))

        conn.commit()
        conn.close()
        print("✅ Data saved to DB")

    except Exception as e:
        print(f"❌ DB Error: {e}")