from fastapi import FastAPI, Depends
from app.services.Kijiji import getKijijiAds

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "This is the root of the app."}


@app.get("/kijiji/")
async def kijiji(user_search: str, user_location: str):
    print(longitude, latitude)
    ads = await getKijijiAds("test", user_location)
    print(ads)
    return {"message": "This is the kijiji route"}
