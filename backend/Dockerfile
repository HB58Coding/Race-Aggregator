FROM python:3.10-slim

WORKDIR /app

COPY . /app/

# Optional — if you have .env.example inside backend/  
# Or remove this line if you don't need it  
# COPY .env.example /app/.env  

COPY requirements.txt /app/requirements.txt

RUN pip install --no-cache-dir -r /app/requirements.txt

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
