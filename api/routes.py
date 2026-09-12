from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session
from database import get_db
from URL_Shortener.schemas.pydantic_models import UrlRequest
from URL_Shortener.crud.url_processing import shorten, elongate
import hashlib

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


# Cache the code → URL in Redis with a 1-hour TTL
# Record every click in the clicks table as a background RQ jo
@router.get("/{short_code}")
def generate_url(short_code: str, request: Request, db: Session = Depends(get_db)):
    # gets where the user came from (e.g., "https://twitter.com/")
    referrer_url = request.headers.get("referer")

    # the raw IP (or fallback if behind a proxy
    raw_ip_header = request.headers.get("x-forwarded-for")
    if raw_ip_header:
        raw_ip = raw_ip_header.split(",")[
            0
        ].strip()  # Get the true client IP because a list of IP's is returned
    else:
        raw_ip = request.client.host if request.client else "unknown"
    # we then hash with SHA-256
    ip_hash = hashlib.sha256(raw_ip.encode("utf-8")).hexdigest()
    # <-- first off before cache lets try to get our code from our CRUD
    long_cd = elongate(short_code, referrer_url, ip_hash, db)
    # now long_cd contains the full url
    if not long_cd:
        raise HTTPException(status_code=404, detail="Link not found")
    return RedirectResponse(
        url=long_cd, status_code=307
    )  # ensures our click function is active and still redirects the browser insteda of json

    #    NEXT THING TO DO IS Cache the code → URL in Redis with a 1-hour TTL
    # .  and then Record every click in the clicks table as a background RQ job


# GET /links/{code}/stats —
# return click count and clicks per day (SQL aggregates)
