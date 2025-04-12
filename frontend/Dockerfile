FROM python:3.10-slim

WORKDIR /app

COPY dashboard.py /app/dashboard.py
COPY requirements.txt /app/requirements.txt

RUN pip install --no-cache-dir -r /app/requirements.txt

EXPOSE 8501

CMD ["streamlit", "run", "/app/dashboard.py", "--server.port=8501", "--server.enableCORS=false"]
