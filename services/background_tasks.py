from database import (
    SessionLocal,
)  # <-- we have to use a seperate connection since this is a diff task
from URL_Shortener.models.models import Click
from URL_Shortener.services.celery_app import celery_app


@celery_app.task
def log_clicks(link_id: int, referrer: str | None, ip_hash: str):
    db = SessionLocal()  # Standalone session for worker thread
    try:
        new_click = Click(link_id=link_id, referrer=referrer, ip_hash=ip_hash)
        db.add(new_click)
        db.commit()
    finally:
        db.close()
