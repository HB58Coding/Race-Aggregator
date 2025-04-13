import os
import streamlit as st
import pandas as pd
import sqlite3
import fastf1
from fastf1.core import Laps
from streamlit_autorefresh import st_autorefresh
import time

# Setup FastF1 cache
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
CACHE_DIR = os.path.join(CURRENT_DIR, "fastf1Cache")
os.makedirs(CACHE_DIR, exist_ok=True)
fastf1.Cache.enable_cache(CACHE_DIR)


# Database path (in root folder)
PROJECT_ROOT = os.path.abspath(os.path.join(CURRENT_DIR, os.pardir))
DB_PATH = os.path.join(PROJECT_ROOT, "telemetry.db")

# Streamlit page setup
st.set_page_config(
    page_title="Live Race Dashboard",
    layout="wide"
)

# Auto-refresh every 5 seconds
st_autorefresh(interval=5000, key="auto_refresh")
st.caption("Auto-refresh every 5 seconds")

# Manual Refresh Button
if st.button("Manual Refresh"):
    st.rerun()

st.title("Live Race Telemetry Dashboard")

# User Inputs
available_years = list(range(2018, 2025))
selected_year = st.sidebar.selectbox("Select Year", available_years[::-1])

# Fetch and Handle FastF1 Data
def fetch_race_data():
    try:
        schedule = fastf1.get_event_schedule(selected_year)
        if schedule.empty:
            st.error("No race schedule found.")
            st.stop()
    except Exception as e:
        st.error(f"Failed to fetch event schedule: {e}")
        st.stop()

    # Map for dropdown
    race_name_map = {
        f"Round {row.RoundNumber}: {row.EventName}": row.RoundNumber
        for _, row in schedule.iterrows()
    }

    race_label = st.sidebar.selectbox("Select Race", list(race_name_map.keys()))
    round_number = race_name_map[race_label]

    try:
        event = fastf1.get_event(selected_year, round_number)
        if event is None:
            st.error("Failed to fetch event.")
            st.stop()

        session = event.get_race()
        session.load(laps=True, telemetry=True)
    except Exception as e:
        st.error(f"Could not load session data: {e}")
        st.stop()

    all_drivers = session.drivers
    if not all_drivers:
        st.warning("No drivers found for this race yet.")

    driver_map = {session.get_driver(d)["FullName"]: d for d in all_drivers}
    selected_driver_name = st.sidebar.selectbox("Select Driver", list(driver_map.keys()))
    selected_driver = driver_map[selected_driver_name]

    st.subheader(f"Live Stats for {selected_driver_name} in {event['EventName']} {selected_year}")

    driver_laps: Laps = session.laps.pick_driver(selected_driver).pick_quicklaps()

    if driver_laps.empty:
        st.warning("No telemetry data available yet for this driver.")
    else:
        fastest_lap = driver_laps.pick_fastest()
        telemetry = fastest_lap.get_car_data()

        st.metric("Speed (top)", f"{telemetry['Speed'].max()} km/h")
        st.metric("RPM (top)", f"{telemetry['RPM'].max()}")
        st.metric("Lap Time", f"{fastest_lap['LapTime']}")
        st.metric("Gear", f"{telemetry['nGear'].max()}")

        st.subheader("Speed Over Distance")
        st.line_chart(telemetry.set_index('Distance')['Speed'])

        st.subheader("RPM Over Distance")
        st.line_chart(telemetry.set_index('Distance')['RPM'])

        st.subheader("Gear Shifts Over Distance")
        st.line_chart(telemetry.set_index('Distance')['nGear'])
        schedule = fastf1.get_event_schedule(2024)
        print(schedule)



# SQLite Live Telemetry (Sim Data)
def ensure_telemetry_table():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS telemetry (
            timestamp INTEGER,
            speed REAL,
            rpm INTEGER,
            gear INTEGER,
            lap_time REAL,
            latitude REAL,
            longitude REAL
        )
    """)
    conn.commit()
    conn.close()

def load_local_data(limit=100):
    if not os.path.exists(DB_PATH):
        return pd.DataFrame()
    conn = sqlite3.connect(DB_PATH)
    try:
        df = pd.read_sql_query(f'''
            SELECT * FROM telemetry ORDER BY timestamp DESC LIMIT {limit}
        ''', conn)
        conn.close()
        return df
    except Exception as e:
        st.warning("Local telemetry table not available or unreadable.")
        return pd.DataFrame()

ensure_telemetry_table()
df = load_local_data()

if not df.empty:
    st.subheader("Simulator Telemetry Data")
    df['timestamp'] = pd.to_datetime(df['timestamp'], unit='s')

    latest = df.iloc[0]

    st.metric("Speed (Sim)", f"{latest['speed']} km/h")
    st.metric("RPM (Sim)", f"{latest['rpm']}")
    st.metric("Lap Time (Sim)", f"{latest['lap_time']} sec")
    st.metric("Gear (Sim)", f"{latest['gear']}")

    st.subheader("Speed Over Time (Sim)")
    st.line_chart(df[['timestamp', 'speed']].set_index('timestamp'))

    st.subheader("RPM Over Time (Sim)")
    st.line_chart(df[['timestamp', 'rpm']].set_index('timestamp'))

    st.subheader("Gear Distribution (Sim)")
    st.bar_chart(df['gear'].value_counts().sort_index())

    st.subheader("GPS Position (Sim, Last 20)")
    st.map(df[['latitude', 'longitude']].head(20))

# Fetch the race data
fetch_race_data()
