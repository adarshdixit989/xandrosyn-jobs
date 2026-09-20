from sqlalchemy import select
from ..models import Alert, DeviceToken, NotificationEvent, Job
from .fcm import send_job_notification

def create_events(db, job):
    alerts=db.scalars(select(Alert).where(Alert.enabled == True)).all()
    text=f"{job.title} {job.company} {job.location}".lower()
    for a in alerts:
        if a.keyword.lower() in text and (not a.location or a.location.lower() in text):
            db.add(NotificationEvent(user_id=a.user_id, job_id=job.id, status="pending"))
    db.commit()

def deliver_pending(db):
    events=db.scalars(select(NotificationEvent).where(NotificationEvent.status=="pending").limit(500)).all()
    sent=0
    for event in events:
        job=db.get(Job,event.job_id)
        tokens=db.scalars(select(DeviceToken).where(DeviceToken.user_id==event.user_id)).all()
        try:
            for device in tokens:
                send_job_notification(device.token, job.id, "New job matching your alert",
                                      f"{job.title} — {job.company}", job.url)
            event.status="sent"
            sent += 1
        except Exception:
            event.status="failed"
    db.commit()
    return sent
