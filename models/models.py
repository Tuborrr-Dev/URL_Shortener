from URL_Shortener.database import Base, engine
from sqlalchemy import Table, text, Column, Integer, String, ForeignKey, DateTime


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    username = Column(String(100), nullable=False)
    email = Column(String, unique=True, nullable=False)
    created_at = Column(DateTime, server_default=text("now()"))


class Link(Base):
    __tablename__ = "links"
    id = Column(Integer, primary_key=True)
    short_code = Column(
        String(10),
        unique=True,
        nullable=False,
    )
    long_url = Column(String(200), nullable=False)
    created_at = Column(DateTime, server_default=text("now()"))
    user_id = Column(Integer, ForeignKey("users.id"))


class Click(Base):
    __tablename__ = "clicks"
    id = Column(Integer, primary_key=True)
    link_id = Column(Integer, ForeignKey("links.id"))
    clicked_at = Column(DateTime, server_default=text("now()"))
    ip_hash = Column(String(100))
    referrer = Column(String(100))


# we have to delete clicks for a link if deleted
click_links = Table(
    "links_clicks",
    Base.metadata,
    Column("link_id", ForeignKey("links.id", ondelete="CASCADE"), primary_key=True),
    Column("click_id", ForeignKey("clicks.id", ondelete="CASCADE"), primary_key=True),
)

# create at all instances
Base.metadata.create_all(engine)
