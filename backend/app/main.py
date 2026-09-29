from fastapi import Depends, FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import Response
from prometheus_client import generate_latest, CONTENT_TYPE_LATEST
from sqlalchemy.orm import Session

from .automation import run_job
from .database import Base, engine, get_db
from .metrics import update_metrics
from .models import AutomationJob, MonitoringSnapshot
from .monitoring import system_metrics

Base.metadata.create_all(bind=engine)

app = FastAPI(title="LinuxOps Monitor", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/health")
def health():
    return {"status": "ok", "service": "linuxops-monitor"}

@app.get("/api/system")
def system(db: Session = Depends(get_db)):
    data = system_metrics()
    update_metrics(data)
    snapshot = MonitoringSnapshot(
        cpu_percent=data["cpu_percent"],
        memory_percent=data["memory_percent"],
        disk_percent=data["disk_percent"],
        network_sent_mb=data["network_sent_mb"],
        network_recv_mb=data["network_recv_mb"],
    )
    db.add(snapshot)
    db.commit()
    return data

@app.get("/api/history")
def history(db: Session = Depends(get_db)):
    rows = db.query(MonitoringSnapshot).order_by(MonitoringSnapshot.id.desc()).limit(20).all()
    return [
        {
            "created_at": r.created_at.isoformat(),
            "cpu_percent": r.cpu_percent,
            "memory_percent": r.memory_percent,
            "disk_percent": r.disk_percent,
        }
        for r in reversed(rows)
    ]

@app.get("/api/jobs")
def jobs(db: Session = Depends(get_db)):
    rows = db.query(AutomationJob).order_by(AutomationJob.id.desc()).limit(20).all()
    return [
        {"id": r.id, "name": r.name, "status": r.status, "output": r.output, "created_at": r.created_at.isoformat()}
        for r in rows
    ]

@app.post("/api/jobs/{name}")
def create_job(name: str, db: Session = Depends(get_db)):
    allowed = {"health-check", "dependency-check", "disk-check"}
    if name not in allowed:
        raise HTTPException(status_code=400, detail="Unsupported automation job")
    try:
        output = run_job(name)
        status = "success"
    except Exception as exc:
        output = str(exc)
        status = "failed"

    job = AutomationJob(name=name, status=status, output=output)
    db.add(job)
    db.commit()
    db.refresh(job)
    return {"id": job.id, "name": job.name, "status": job.status, "output": job.output}

@app.get("/metrics")
def metrics():
    return Response(generate_latest(), media_type=CONTENT_TYPE_LATEST)
