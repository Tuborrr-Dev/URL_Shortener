from fastapi import FastAPI, Depends
from URL_Shortener.DB.models import User, Link, Click, click_links
from URL_Shortener.DB.db import SessionLocal
from URL_Shortener.PROCESSING.shortener import shorten_B62
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from sqlalchemy import text

app = FastAPI()


# first we try creating our DB through our models and handing it over to FAST
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()  # to avoid DB leaks


@app.post("/{username}/{url}")  # <-- this is the post method to our API to save the URL
def shorten_url(username: str, url: str, db: Session = Depends(get_db)):
    user = db.get(User, username)
    if user is None:
        return {"error": "User not found"}
    if url is None:
        return {"error": "url cannot be Empty"}
    # we are using a randomizer but this could still give rise to repition hence the readon to retry
    max_retries = 3
    for x in range(max_retries):
        try:
            short_cd = shorten_B62()
            new_link = Link(short_code=short_cd, long_url=url, user_id=user.id)
            db.add(new_link)
            db.commit()
            # return the short code, after storing in Postgres
            return {"short_url": {short_cd}}
        except IntegrityError:
            db.rollback()


@app.get("/")
def generate_url():
    return  # look up the code in the cache and then if not there from DB and return a 301 redirect
