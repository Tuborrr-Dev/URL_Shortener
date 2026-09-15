from database import (
    SessionLocal,
)  # <-- we have to use a seperate connection since this is a diff task
from URL_Shortener.models.models import Click
from URL_Shortener.services.celery_app import celery_app
from sqlalchemy.exc import OperationalError


@celery_app.task(
    autoretry_for=(OperationalError,),  # Retry on DB connection drop
    retry_kwargs={"max_retries": 5},  # Try up to 5 times
    retry_backoff=True,  # Exponential backoff (2s, 4s, 8s...)
    retry_backoff_max=600,  # Cap wait time at 10 minutes
)
def log_clicks(link_id: int, referrer: str | None, ip_hash: str, clicked_at: int):
    db = SessionLocal()  # Standalone session for worker thread
    try:
        new_click = Click(
            link_id=link_id, referrer=referrer, ip_hash=ip_hash, clicked_at=clicked_at
        )
        db.add(new_click)
        db.commit()
    finally:
        db.close()
