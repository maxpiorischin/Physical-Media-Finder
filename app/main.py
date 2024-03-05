import os
from fastapi import FastAPI, HTTPException
from app.services.Kijiji import get_kijiji_ads
from app.services.eBay import get_ebay_ads, set_ebay_api_key
from app.services.Amazon import get_amazon_ads
from app.services.Helpers import retry_async, valid_postal_code
from dotenv import load_dotenv

app = FastAPI()
MAX_RETRIES = 3
load_dotenv()
set_ebay_api_key()


@app.get("/")
async def root():
    return {"message": "This is the root of the app."}


@app.get("/kijiji/")
async def kijiji(user_search: str, user_location: str):
    ads = await retry_async(get_kijiji_ads, MAX_RETRIES, 1, user_search, user_location)
    return {"ads": ads}


@app.get("/amazon/")
async def amazon(user_search: str, user_postal_code: str):
    if not await valid_postal_code(user_postal_code):
        raise HTTPException(status_code=400, detail="Invalid Postal Code")
    ads = await retry_async(get_amazon_ads, MAX_RETRIES, 1, user_search, user_postal_code)
    return {"ads": ads}


@app.get("/ebay/")
async def ebay(user_search: str):
    ads = await retry_async(get_ebay_ads, MAX_RETRIES, 1, user_search)
    return {"ads": ads}
