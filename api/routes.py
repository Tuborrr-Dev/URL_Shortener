from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from URL_Shortener.schemas.pydantic_models import UrlRequest
from URL_Shortener.crud.url_processing import shorten, elongate

router = APIRouter()

# endpoint to register a user still not available
# endpoint to check if a user exists still not available
# ability to track clicks with timestamps


@router.post("/shorten_url")  # <-- this is the post method to our API to save the URL
def shorten_url(
    payload: UrlRequest, db: Session = Depends(get_db)
):  # <-- tells FastAPI: "Hey! Before running any CRUD, go execute get_db(), grab whatever it yields, and plug it into the db variable."
    short_cd = shorten(payload.username, payload.long_url, db)
    if short_cd:
        return {"short_url": short_cd}
    else:
        raise HTTPException(status_code=400, detail="User not found or Duplicate error")


# GET /{code} redirects to the original.
# Cache the code → URL in Redis with a 1-hour TTL
# Record every click in the clicks table as a background RQ jo
@router.get("/{short_code}")
def generate_url(
    short_code: str,
):  # <-- first off before cache lets try to get our code from our CRUD
    long_cd = elongate(short_code)
    # now long_cd contains the full url
    if not long_cd:
        raise HTTPException(status_code=400, detail="Link not found")
    return {"URL_elongated": long_cd}

    # look up the code in the cache and then if not there from DB and return a 301 redirect


# GET /links/{code}/stats —
# return click count and clicks per day (SQL aggregates)
