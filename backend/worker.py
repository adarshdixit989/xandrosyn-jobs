from sqlalchemy import select
from app.db import SessionLocal
from app.models import Job
from app.services.sources import load_sources, fetch_rss
from app.services.job_sources import fetch_adzuna, fetch_lever_public
from app.services.notifications import create_events, deliver_pending

def get_jobs(source):
    kind = source.get("type")
    if kind == "rss":
        return fetch_rss(source)
    if kind == "adzuna":
        return fetch_adzuna(source)
    if kind == "lever_public":
        return fetch_lever_public(source)
    return []

def run():
    db = SessionLocal()
    try:
        added = 0
        for source in load_sources("./sources.json"):
            if not source.get("enabled"):
                continue
            for item in get_jobs(source):
                exists = db.scalar(select(Job).where(
                    Job.source == item["source"],
                    Job.external_id == item["external_id"]
                ))
                if exists or not item.get("url"):
                    continue

                job = Job(**item)
                db.add(job)
                db.commit()
                db.refresh(job)
                create_events(db, job)
                added += 1

        sent = deliver_pending(db)
        print(f"new_jobs={added} notifications_sent={sent}")
    finally:
        db.close()

if __name__ == "__main__":
    run()
