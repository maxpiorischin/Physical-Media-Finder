from playwright.async_api import async_playwright, Page
from app.services.BrowserManager import newPage

URL = "https://www.kijiji.ca/"
DEFAULT_TIMEOUT = 50000.0


async def initialize(page: Page):
    return await page.goto(URL, wait_until="domcontentloaded")

async def inputLocation(page: Page, user_location: str):

    locationbutton = await page.query_selector("#SearchLocationPicker")
    await locationbutton.click()
    await page.wait_for_timeout(500)
    await page.get_by_label("Use my current location").click()
    await page.wait_for_timeout(DEFAULT_TIMEOUT)



async def getKijijiAds(user_input: str, user_location: str) -> str:
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        page = await newPage(browser)
        await initialize(page)
        await inputLocation(page, user_location)
        await page.wait_for_timeout(100000.0)
        await browser.close()
        return "done"
