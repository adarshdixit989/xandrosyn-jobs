import os
import firebase_admin
from firebase_admin import credentials, messaging

_initialized = False

def init_firebase():
    global _initialized
    if _initialized:
        return
    path = os.getenv("GOOGLE_APPLICATION_CREDENTIALS", "")
    if path:
        firebase_admin.initialize_app(credentials.Certificate(path))
    else:
        firebase_admin.initialize_app()
    _initialized = True

def send_job_notification(token, job_id, title, body, url):
    init_firebase()
    message = messaging.Message(
        notification=messaging.Notification(title=title, body=body),
        data={"job_id": str(job_id), "url": url},
        token=token,
    )
    return messaging.send(message)
