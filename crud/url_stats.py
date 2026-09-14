# this is our main processor for the stats
from sqlalchemy import func
from sqlalchemy.orm import Session

# this is calculating the date
import time
from datetime import datetime, timezone

# for accessing DB
from URL_Shortener.models.models import Link, Click

# for getting cache data
from URL_Shortener.services.cache import r
import json


def count_em_up(short_code: str, db: Session) -> int:
    cached_data = r.get(short_code)
    if cached_data:  # <-- then we have it in the cache
        data = json.loads(cached_data)
        link_id = data["id"]
        long_url = link.long_url
    else:  # not in cache so we have to go find the link ID first
        link = db.query(Link).filter(Link.short_code == short_code).first()
        if not link:  # not in our DB
            return None
        link_id = link.id
        # we now have the link access so lets cache either way in json form
        r.set(
            short_code,
            json.dumps({"id": link_id, "long_url": long_url}),
            ex=3600,
        )
    # now we have link ID so we count em up
    total_clicks = (
        db.query(func.count(Click.id)).filter(Click.link_id == link_id).scalar()
    )  # <-- the func count is the sqlalchemy equivalent of count in TEXT
    return total_clicks


def count_em_24hr(short_code: str, db: Session) -> int:
    # for the past 24 hours we do a filter based off timestamp
    # we first checked if it exists which it does so it's definitely in cache
    cached_data = r.get(short_code)
    if not cached_data:
        return None
    data = json.loads(cached_data)
    link_id = data["id"]
    # now we have link ID so we calculate using epoch to know exact 24 hour ago
    limit_epoch = int(time.time()) - 86400  # 86400 is 24hrs ago in secs
    total_clicks_24hr = (
        db.query(func.count(Click.id))
        .filter(Click.link_id == link_id)
        .filter(Click.clicked_at >= limit_epoch)
        .scalar()
    )
    return total_clicks_24hr
