# LinuxOps Monitor

A real full-stack Linux/server monitoring and automation application.

## What it does

- Shows live CPU, memory, disk, uptime and network information.
- Stores monitoring snapshots and automation-job history in PostgreSQL.
- Provides a React dashboard backed by FastAPI.
- Exposes Prometheus metrics.
- Includes a Docker Compose environment for the application, PostgreSQL, Prometheus and Grafana.
- Includes safe, allow-listed automation jobs:
  - health check
  - application dependency check
  - disk-usage check
- Does NOT expose arbitrary shell-command execution from the browser.

## Architecture

React + Vite
        |
        v
FastAPI REST API ---- PostgreSQL
        |
        +---- psutil (Linux/system metrics)
        |
        +---- Prometheus /metrics
                    |
                    v
                 Grafana

## Requirements

### Easiest method
- Docker Desktop / Docker Engine
- Docker Compose

### Local development
- Python 3.11+
- Node.js 20+
- PostgreSQL 16+

## Run with Docker

From this folder:

```bash
docker compose up --build
```

Then open:

- Frontend: http://localhost:5173
- API docs: http://localhost:8000/docs
- API health: http://localhost:8000/health
- Prometheus: http://localhost:9090
- Grafana: http://localhost:3000

Grafana login:
- Username: admin
- Password: admin

## Local Linux setup

```bash
chmod +x scripts/*.sh
./scripts/setup.sh
```

Backend:

```bash
cd backend
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

Frontend:

```bash
cd frontend
npm install
npm run dev
```

## API examples

```bash
curl http://localhost:8000/health
curl http://localhost:8000/api/system
curl http://localhost:8000/api/jobs
curl -X POST http://localhost:8000/api/jobs/health-check
```

## Database

The application creates these tables automatically:

- monitoring_snapshots
- automation_jobs

The database connection is controlled by `DATABASE_URL`.

## Important

This project is designed for learning and portfolio use. It is a monitoring/automation application, not a production security product. Before deploying publicly, add authentication, HTTPS, role-based access, secret management, rate limiting and stronger audit controls.
