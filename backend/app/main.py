from fastapi import FastAPI, Depends
from pydantic import BaseModel
from sqlalchemy import select, text
from sqlalchemy.orm import Session
from .db import SessionLocal, engine
from .models import Base, Job, DeviceToken, Alert

Base.metadata.create_all(engine)
app = FastAPI(title="Xandrosyn Jobs API", version="11.0.0")

def db():
    s = SessionLocal()
    try:
        yield s
    finally:
        s.close()

class TokenIn(BaseModel):
    user_id: str
    token: str
    platform: str = "android"

class AlertIn(BaseModel):
    user_id: str
    keyword: str
    location: str = ""

@app.get("/")
def root():
    return {
        "name": "Xandrosyn Jobs API",
        "status": "online",
        "health": "/api/health",
        "docs": "/docs",
    }

@app.get("/api/health")
def health(db: Session = Depends(db)):
    db.execute(text("SELECT 1"))
    return {"ok": True, "version": "11.0.0", "database": "connected"}

@app.post("/api/devices")
def register_device(data: TokenIn, db: Session = Depends(db)):
    old = db.scalar(select(DeviceToken).where(DeviceToken.token == data.token))
    if old:
        old.user_id = data.user_id
        old.platform = data.platform
    else:
        db.add(DeviceToken(**data.model_dump()))
    db.commit()
    return {"registered": True}

@app.post("/api/alerts")
def alert(data: AlertIn, db: Session = Depends(db)):
    a = Alert(**data.model_dump())
    db.add(a)
    db.commit()
    db.refresh(a)
    return {"id": a.id}

@app.get("/api/jobs")
def jobs(q: str = "", location: str = "", db: Session = Depends(db)):
    rows = db.scalars(
        select(Job)
        .where(Job.is_active == True)
        .order_by(Job.created_at.desc())
        .limit(100)
    ).all()
    return [
        {
            "id": j.id,
            "title": j.title,
            "company": j.company,
            "location": j.location,
            "url": j.url,
        }
        for j in rows
        if (not q or q.lower() in (j.title + " " + j.company).lower())
        and (not location or location.lower() in j.location.lower())
    ]
