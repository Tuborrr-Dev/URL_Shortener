from URL_Shortener.DB.db import Base
from datetime import datetime, UTC
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Index
from sqlalchemy.orm import relationship


class Link(Base):
    __tablename__ = "links"
