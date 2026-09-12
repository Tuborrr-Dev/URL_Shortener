from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker
from URL_Shortener.core.config import (
    settings,
)  # we import all our .env through the core config files

DB_URL = settings.DATABASE_URL

engine = create_engine(DB_URL)  # engine created
SessionLocal = sessionmaker(
    bind=engine
)  # engine binded to the machine that ensures back and forth flow in sqlalchemy


class Base(DeclarativeBase):
    pass  # to maintain registry of all tables and all models import this


# first we try creating our DB through our models and handing it over to FAST
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()  # to avoid DB leaks
