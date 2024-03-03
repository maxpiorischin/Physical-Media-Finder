from playwright.async_api import async_playwright, Page
from app.services.Helpers import newPage
from urllib.parse import urlparse, parse_qs, urlunparse, urlencode

URL = "https://www.kijiji.ca/"
DEFAULT_CATEGORY = "b-video-games-consoles"
DEFAULT_CODE = "k0c141l1700212"
DEFAULT_TIMEOUT = 1000
DEFAULT_TIMEOUT_LONG = 5000


async def initialize(page: Page):
    return await page.goto(URL, wait_until="domcontentloaded")


async def input_location(page: Page, user_location: str):
    locationbutton = await page.wait_for_selector("#SearchLocationPicker")
    await locationbutton.click()
    input_form = await page.wait_for_selector("#SearchLocationSelector-input")
    await input_form.fill(user_location)
    await page.wait_for_timeout(DEFAULT_TIMEOUT)
    await input_form.press("Enter")
    apply_button = page.locator("button:has-text('Apply')")
    await apply_button.click()
    return page


async def search_ads(page: Page, user_input: str):
    parsed_url = urlparse(page.url)
    query_components = parse_qs(parsed_url.query)
    location = parsed_url.path.split('/')[-2][2:]  # remove the b- from the location

    # Construct the new path
    new_path = f'/{DEFAULT_CATEGORY}/{location}/{user_input}/{DEFAULT_CODE}'
    # Maintain other parameters from the original URL
    new_query_string = urlencode(query_components, doseq=True)

    # Reconstruct the new URL
    new_url = urlunparse((parsed_url.scheme, parsed_url.netloc, new_path, '', new_query_string, ''))

    await page.goto(new_url, wait_until="domcontentloaded")

    return page


async def get_ads_list(page: Page) -> list[dict[str, str]]:
    ads = []  # list of ads
    titles = page.locator('[data-testid="listing-title"]')
    links = page.locator('[data-testid="listing-link"]')
    descriptions = page.locator('[data-testid="listing-description"]')
    locations = page.locator('[data-testid="listing-location"]')
    prices = page.locator('[data-testid="listing-price"]')
    ads_count = await titles.count()
    for i in range(ads_count):
        title = await titles.nth(i).text_content()
        link = await links.nth(i).get_attribute("href")
        description = await descriptions.nth(i).text_content()
        location = await locations.nth(i).text_content()
        price = await prices.nth(i).text_content()
        ads.append({"title": title, "link": link, "description": description, "location": location, "price": price})
    return ads


async def get_kijiji_ads(user_input: str, user_location: str) -> list[dict[str, str]]:
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        page = await newPage(browser)
        await initialize(page)
        await input_location(page, user_location)
        await page.wait_for_timeout(DEFAULT_TIMEOUT_LONG)
        await search_ads(page, user_input)
        ads = await get_ads_list(page)
        await browser.close()
        return ads
