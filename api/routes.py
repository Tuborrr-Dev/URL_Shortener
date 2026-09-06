from fastapi import APIRouter, Depends
from URL_Shortener.models.models import User, Link, Click, click_links
from URL_Shortener.database import SessionLocal
from URL_Shortener.services.shortener import shorten_B62
from URL_Shortener.schemas.pydantic_models import UrlRequest
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from sqlalchemy import text

router = APIRouter()


# first we try creating our DB through our models and handing it over to FAST
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()  # to avoid DB leaks


# endpoint to register a user still not available
# endpoint to check if a user exists still not available
# ability to track clicks with timestamps


@router.post("/shorten_url")  # <-- this is the post method to our API to save the URL
def shorten_url(payload: UrlRequest, db: Session = Depends(get_db)):
    user = db.get(User, payload.username)
    if user is None:
        return {"error": "User not found"}
    if payload.long_url is None:
        return {"error": "url cannot be Empty"}
    # we are using a randomizer but this could still give rise to repition hence the readon to retry
    max_retries = 3
    for x in range(max_retries):
        try:
            short_cd = shorten_B62()
            new_link = Link(
                short_code=short_cd, long_url=payload.long_url, user_id=user.id
            )
            db.add(new_link)
            db.commit()
            # return the short code, after storing in Postgres
            return {"short_url": {short_cd}}
        except IntegrityError:
            db.rollback()


# GET /{code} redirects to the original.
# Cache the code → URL in Redis with a 1-hour TTL
# Record every click in the clicks table as a background RQ jo
@router.get("/{code}")
def generate_url():

    return  # look up the code in the cache and then if not there from DB and return a 301 redirect


# GET /links/{code}/stats —
# return click count and clicks per day (SQL aggregates)
