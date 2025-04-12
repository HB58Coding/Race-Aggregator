import json
import random
import time
import asyncio
import websockets

def generate_telemetry():
    return {
        "car_id": random.randint(1, 5),
        "speed": round(random.uniform(100, 320), 2),
        "rpm": random.randint(6000, 15000),
        "lap_time": round(random.uniform(60, 130), 2),
        "gear": random.randint(1, 8),
        "track_position": {
            "lat": round(random.uniform(12.9, 13.0), 6),
            "lon": round(random.uniform(77.5, 77.6), 6)
        },
        "timestamp": time.time()
    }

async def stream_telemetry():
    uri = "ws://localhost:8000/ws/telemetry"
    async with websockets.connect(uri) as websocket:
        while True:
            data = generate_telemetry()
            await websocket.send(json.dumps(data))
            print(f"📤 Sent: {data}")
            await asyncio.sleep(1)

if __name__ == "__main__":
    asyncio.run(stream_telemetry())