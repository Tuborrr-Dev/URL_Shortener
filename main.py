from fastapi import FastAPI
from URL_Shortener.api.routes import (
    router,
)  # this isnt done in the main.py file because we want to keep the main.py file clean and organized

app = FastAPI(title="URL Shortener API", version="1.0.0")

# Mount your endpoints to the main application
app.include_router(url_router)


@app.get("/health")
def health_check():
    return {"status": "ok"}
