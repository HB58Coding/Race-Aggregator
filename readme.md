# Race-Aggregator

A telemetry dashboard for live and simulated motorsport data, built with FastAPI, Streamlit, and FastF1.

## Features
- FastF1 data fetching with caching
- Real-time telemetry simulation
- WebSocket streaming
- SQLite storage
- Live dashboard visualization
- Dockerized microservices architecture

---

## Project Structure
```
race-aggregator/
├── backend/
│   ├── api.py
│   ├── db.py
│   ├── save_to_db.py
│   ├── Dockerfile
│   └── requirements.txt
├── frontend/
│   ├── dashboard.py
│   ├── Dockerfile
│   └── requirements.txt
├── simulator/
│   ├── telemetry_simulator.py
│   ├── Dockerfile
│   ├── requirements.txt
│   └── fastf1_cache/
├── telemetry.db
├── docker-compose.yml
├── .gitignore
└── requirements.txt
```

---

## Quick Start (Docker)

### 1. Clone the repository
```bash
git clone <repo-url>
cd race-aggregator
```

### 2. Create the SQLite database (optional, auto-created on start)
```bash
touch telemetry.db
```

### 3. Build and run all services
```bash
docker-compose up --build
```

### 4. Access the services
- **Backend (FastAPI)**: [http://localhost:8000](http://localhost:8000)
- **Frontend (Streamlit Dashboard)**: [http://localhost:8501](http://localhost:8501)

---

## For Development (Manual Run)

### Setup a virtual environment
```bash
python3 -m venv env310
source env310/bin/activate
```

### Install dependencies
```bash
pip install -r requirements.txt
```

### Run backend API
```bash
cd backend
uvicorn api:app --reload --host 0.0.0.0 --port 8000
```

### Run simulator
```bash
cd simulator
python telemetry_simulator.py
```

### Run dashboard
```bash
cd frontend
streamlit run dashboard.py
```

---

## Notes
- WebSocket simulator connects to: `ws://localhost:8000/ws/telemetry`
- FastF1 data is cached in `fastf1_cache/`
- All telemetry data is stored in `telemetry.db`

---

## Environment Variables (Optional)
Set in `.env` or Docker Compose:
```
DB_PATH=/app/telemetry.db
HOST_DB_PATH=./telemetry.db
```

---

## Future Improvements
- Add driver/car selection to simulator
- Historical data comparison
- Session type and year selection from dashboard
- CI/CD pipeline

---

## 🚀 Made with ❤️ by [You]
Built to showcase real-time racing telemetry and dashboarding skills using only Python and a laptop.
