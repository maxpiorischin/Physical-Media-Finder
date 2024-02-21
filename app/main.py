from fastapi import FastAPI
from app.services.Kijiji import getKijijiAds
from app.services.BrowserManager import retry_async

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "This is the root of the app."}


@app.get("/kijiji/")
async def kijiji(user_search: str, user_location: str):
    ads = await retry_async(getKijijiAds, 3, user_search, user_location)
    return {"ads": ads}
