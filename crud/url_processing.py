from URL_Shortener.models.models import User, Link, Click
from URL_Shortener.services.shortener import shorten_B62
from URL_Shortener.schemas.pydantic_models import UrlRequest
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from sqlalchemy import func

# for cachihne
import redis

"""unknown redis connection, fill later"""
r = redis.Redis(decode_responses=True)


# now we create an entire function to do all our CRUD processes for us
def shorten(username: str, long_url: str, db: Session) -> str:
    # 1. Check user
    user = (
        db.query(User).filter(User.username == username).first()
    )  # we query the DB to check for username first instance
    if not user:
        return None
    if long_url is None:
        return None

    """replace the below with a more efficient method of caching"""
    # in the case we have stored the exact same URL before, we dont want to store the same thing, save space
    link_b4 = db.query(Link).filter(Link.long_url == long_url).first()
    if link_b4:
        # then we already have this before
        return link_b4.short_code
    max_retries = 3
    for x in range(max_retries):
        try:
            short_cd = shorten_B62()
            new_link = Link(short_code=short_cd, long_url=long_url, user_id=user.id)
            db.add(new_link)
            db.commit()
            # return the short code, after storing in Postgres
            return short_cd
        # in the case where it has been stored the integrityError is raised and the entire process is roll-backed
        except IntegrityError:
            db.rollback()
    # and if after 3 tries it still shows DB has what we used we return none
    return None


def elongate(short_code: str, refer_url: str, iphash: str, db: Session) -> str:
    long_url = r.get({short_code})
    if long_url:
        return long_url
    # check in Link and get long url from DB
    link = db.query(Link).filter(Link.short_code == short_code).first()
    long_url = link.long_url
    # we now have the long link so lets cache
    r.set({short_code}, {long_url})
    if not link:  # not in that bih
        return None
    # above all else after confirming a link exists now a count should exist towards its clicks
    new_click = Click(link_id=link.id, referrer=refer_url, ip_hash=iphash)
    db.add(new_click)
    db.commit()
    return long_url


#    NEXT THING TO DO IS Cache the code → URL in Redis with a 1-hour TTL
# .  and then Record every click in the clicks table as a background RQ job
"""total_clicks = (
        db.query(func.count(Click.id)).filter(Click.link_id == link.id).scalar()
    )"""
