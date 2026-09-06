from pydantic import BaseModel, HttpUrl


# so we create the entire request in pydantic to avoid see finish
class UrlRequest(BaseModel):
    username: str
    long_url: HttpUrl  # <-- this is to avoid any url giving any issues
