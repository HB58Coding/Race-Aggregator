# Example for frontend Dockerfile
FROM python:3.10-slim

WORKDIR /app

# Copy the frontend code
COPY frontend/dashboard.py /app/dashboard.py

# Install dependencies
COPY requirements.txt /app/requirements.txt
RUN pip3 install -r requirements.txt

# Run streamlit app
CMD ["streamlit", "run", "dashboard.py"]