import sqlite3
import os

DB_PATH = os.getenv('DB_PATH')
HOST_DB_PATH = os.getenv('HOST_DB_PATH')

print(f"DB Path: {DB_PATH}")
print(f"Host DB Path: {HOST_DB_PATH}")

def init_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS telemetry (
            car_id INTEGER,
            speed REAL,
            rpm INTEGER,
            lap_time REAL,
            gear INTEGER,
            latitude REAL,
            longitude REAL,
            timestamp REAL
        )
    ''')

    conn.commit()
    conn.close()
    print(f"✅ Database initialized at {DB_PATH}")

if __name__ == "__main__":
    init_db()