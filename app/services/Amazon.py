import aiohttp, re
from bs4 import BeautifulSoup

base_link = "https://www.amazon.ca/"
address_change_link = "https://www.amazon.ca/portal-migration/hz/glow/address-change?actionSource=glow"
headers = {
    "User-Agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Mobile Safari/537.36",
    "Accept": "text/html,*/*"}
post_data = {"locationType": "LOCATION_INPUT", "zipCode": "123456", "deviceType": "web", "storeContext": "generic",
             "pageType": "Search", "actionSource": "glow"}


async def get_webpage(session, filled_link):
    await session.get(filled_link)
    await session.post(address_change_link, headers=headers,
                       data=post_data)  # change address using post request, then use bs4 to parse items
    webpage = await session.get(filled_link)
    return await webpage.text()  # html content as a string


async def parse_webpage_into_ads(html: str, limit: int):
    soup = BeautifulSoup(html, 'html.parser')
    # get the amount of search results found on amazon
    search_results_amount = len(soup.find_all(class_="template=SEARCH_RESULTS"))
    limit = min(limit, search_results_amount)  # if there are less ads than
    return [f"{search_results_amount}{soup}"]


async def get_amazon_ads(user_input: str, user_postal_code: str, limit: int):
    user_input = user_input.replace(" ", "+")  # the reason these lines are not abstracted into another function is
    # because Windows has a known issue with aiohttp and async event loops when it comes to ClientSession,
    # so the main called function is the one which initiates the session for simplicity
    filled_link = f"{base_link}s?field-keywords={user_input}"
    post_data["zipCode"] = user_postal_code
    async with aiohttp.ClientSession() as session:
        html = await get_webpage(session, filled_link)
        ads = await parse_webpage_into_ads(html, limit) #this must stay in here if it wants to reference html, otherwise a windows socket error occurs (known aiohttp bug)
        return [ads]
