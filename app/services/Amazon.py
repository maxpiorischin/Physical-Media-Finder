import aiohttp

base_link = "https://www.amazon.ca/"
address_change_link = "https://www.amazon.ca/portal-migration/hz/glow/address-change?actionSource=glow"
post_data = {"locationType":"LOCATION_INPUT","zipCode": "123456","deviceType":"web","storeContext":"generic","pageType":"Search","actionSource":"glow"}

async def get_amazon_ads(user_input: str, user_postal_code: str):
    user_input = user_input.replace(" ", "+")
    filled_link = f"{base_link}s?field-keywords={user_input}"
    post_data["zipCode"] = user_postal_code
    async with aiohttp.ClientSession as session:
        await session.get(filled_link)
        await session.post(address_change_link, data=post_data) #change address using post request, then use bs4 to parse items
        return ["temp"]