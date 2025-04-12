# Example for simulator Dockerfile
FROM python:3.10-slim

WORKDIR /app

# Copy the simulation script and any other necessary files
COPY simulator/telemetry_simulator.py /app/telemetry_simulator.py

# Install dependencies
COPY requirements.txt /app/requirements.txt
RUN pip3 install -r requirements.txt

# Command to run the simulation script
CMD ["python3", "telemetry_simulator.py"]