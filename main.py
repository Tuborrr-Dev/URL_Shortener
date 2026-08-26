from fastapi import FastAPI

app = FastAPI()


@app.post("/")  # <-- this is the post method to our API to save the URL
def shorten_url():
    return  # generate a short code, after storing in Postgres


@app.get("/")
def generate_url():
    return  # look up the code in the cache and then if not there from DB and return a 301 redirect
