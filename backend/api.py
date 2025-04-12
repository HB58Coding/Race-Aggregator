from fastapi import FastAPI, WebSocket
import json
import traceback
from backend.save_to_db import save_telemetry_data 
from backend.db import init_db

app = FastAPI()

@app.on_event("startup")
def startup_event():
    print("🔧 Initializing database...")
    init_db()

@app.websocket("/ws/telemetry")
async def telemetry_stream(websocket: WebSocket):
    await websocket.accept()
    print("📡 WebSocket connection accepted.")

    try:
        while True:
            raw_data = await websocket.receive_text()
            telemetry = json.loads(raw_data)
            print(f"📥 Received telemetry: {telemetry}")
            save_telemetry_data(telemetry)

    except Exception as e:
        print(f"❌ WebSocket Error: {e}")
        traceback.print_exc()
        await websocket.close()