import os
from fastapi import FastAPI, HTTPException
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.interval import IntervalTrigger
from app.services.Kijiji import get_kijiji_ads
from app.services.eBay import get_ebay_ads, regenerate_ebay_token
from app.services.Amazon import get_amazon_ads
from app.services.Helpers import retry_async, valid_postal_code, valid_search
from dotenv import load_dotenv

app = FastAPI()
scheduler = AsyncIOScheduler()
MAX_RETRIES = 3 #maximum number of retries before failing
MAX_ADS_LIMIT = 10 #Maximum number of ads that can be requested
MAX_CHARACTER_LIMIT = 30 #Maximum user input character limit


@app.on_event("startup")
async def startup():
    load_dotenv()
    await regenerate_ebay_token()
    # Schedule to regenerate ebay token every 100 minutes since it only lasts 2 hours
    scheduler.add_job(regenerate_ebay_token, IntervalTrigger(minutes=100))
    scheduler.start()


@app.get("/")
async def root():
    return {"message": "This is the root of the app."}


@app.get("/kijiji/")
async def kijiji(user_search: str, user_location: str, limit: int = 10):
    user_search = user_search.replace(" ", "-") #kijiji only takes dashes
    if not await valid_search(user_search, MAX_CHARACTER_LIMIT):
        raise HTTPException(status_code=400, detail="User search is improper, ensure it's less than 20 characters")
    if limit > MAX_ADS_LIMIT:
        raise HTTPException(status_code=400, detail="Limit too large, keep it less than or equal to 10")
    ads = await retry_async(get_kijiji_ads, MAX_RETRIES, 1, user_search, user_location, limit)
    return {"ads": ads}


@app.get("/amazon/")
async def amazon(user_search: str, user_postal_code: str, limit: int = 10):
    user_search = user_search.replace(" ", "+")
    if not await valid_postal_code(user_postal_code):
        raise HTTPException(status_code=400, detail="Invalid Postal Code")
    if not await valid_search(user_search, MAX_CHARACTER_LIMIT):
        raise HTTPException(status_code=400, detail="User search is improper, ensure it's less than 20 characters")
    if limit > MAX_ADS_LIMIT:
        raise HTTPException(status_code=400, detail="Limit too large, keep it less than or equal to 10")
    ads = await retry_async(get_amazon_ads, MAX_RETRIES, 1, user_search, user_postal_code, limit)
    return {"ads": ads}


@app.get("/ebay/")
async def ebay(user_search: str, limit: int = 10):
    user_search = user_search.replace(" ", "+")
    if not await valid_search(user_search, MAX_CHARACTER_LIMIT):
        raise HTTPException(status_code=400, detail="User search is improper, ensure it's less than 20 characters")
    if limit > MAX_ADS_LIMIT:
        raise HTTPException(status_code=400, detail="Limit too large, keep it less than or equal to 10")
    ads = await retry_async(get_ebay_ads, MAX_RETRIES, 1, user_search, limit)
    return {"ads": ads}
