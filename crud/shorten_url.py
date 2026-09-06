from URL_Shortener.models.models import User, Link, Click, click_links
from URL_Shortener.services.shortener import shorten_B62
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError


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
    max_retries = 3
    for x in range(max_retries):
        try:
            short_cd = shorten_B62()
            new_link = Link(short_code=short_cd, long_url=long_url, user_id=user.id)
            db.add(new_link)
            db.commit()
            # return the short code, after storing in Postgres
            return short_cd
        except IntegrityError:
            db.rollback()
    # and if after 3 tries it still shows DB has what we used we return none
    return None
