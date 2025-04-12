import streamlit as st
import pandas as pd
import sqlite3
from streamlit_autorefresh import st_autorefresh

st.set_page_config(
    page_title="🏁 Live Race Dashboard",
    layout="wide"
)

# 💫 Auto-refresh every 5 seconds
st_autorefresh(interval=5000, key="auto_refresh")
st.caption("🔁 Auto-refresh every 5 seconds")

st.title("🏎️ Live Race Telemetry Dashboard")

def load_data(limit=100):
    conn = sqlite3.connect("telemetry.db")
    df = pd.read_sql_query(f'''
        SELECT * FROM telemetry ORDER BY timestamp DESC LIMIT {limit}
    ''', conn)
    conn.close()
    return df

df = load_data()

if df.empty:
    st.warning("No telemetry data found yet.")
else:
    # Convert timestamp
    df['timestamp'] = pd.to_datetime(df['timestamp'], unit='s')

    # Latest data
    latest = df.iloc[0]

    st.subheader("📊 Live Car Stats")
    st.metric("Speed", f"{latest['speed']} km/h")
    st.metric("RPM", f"{latest['rpm']}")
    st.metric("Lap Time", f"{latest['lap_time']} sec")
    st.metric("Gear", f"{latest['gear']}")

    st.subheader("📈 Speed Over Time")
    st.line_chart(df[['timestamp', 'speed']].set_index('timestamp'))

    st.subheader("📉 RPM Over Time")
    st.line_chart(df[['timestamp', 'rpm']].set_index('timestamp'))

    st.subheader("📊 Gear Distribution")
    st.bar_chart(df['gear'].value_counts().sort_index())

    st.subheader("🌍 GPS Position (Last 20)")
    st.map(df[['latitude', 'longitude']].head(20))