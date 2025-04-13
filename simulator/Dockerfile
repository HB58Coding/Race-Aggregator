FROM python:3.10-slim

WORKDIR /app

COPY telemetry_simulator.py /app/telemetry_simulator.py
COPY requirements.txt /app/requirements.txt

RUN pip install --no-cache-dir -r /app/requirements.txt

EXPOSE 5000

RUN mkdir -p /app/.fastf1_cache

CMD ["python", "/app/telemetry_simulator.py"]
