import aiohttp, os
from aiohttp import ClientError

EBAY_API_LINK = "https://api.ebay.com/buy/browse/v1/item_summary/search"
DEFAULT_LIMIT = 10

request_headers = {
    'Authorization': 'temp',
    'X-EBAY-C-MARKETPLACE-ID': 'EBAY_ENCA',
    'X-EBAY-C-ENDUSERCTX': 'affiliateCampaignId=<ePNCampaignId>,affiliateReferenceId=<referenceId>'
}

def set_ebay_api_key():
    """
    in a function since in want it so be called rather than immediately setting this value to
    null before doing load_dotenv
    """
    request_headers['Authorization'] = f"Bearer {os.environ.get('EBAY_API_KEY')}"


async def get_ebay_ads(user_input):
    ads = []
    async with aiohttp.ClientSession() as session:
        link = f"{EBAY_API_LINK}?q={user_input}&limit={DEFAULT_LIMIT}"
        try:
            response = await session.get(link, headers=request_headers)
            response.raise_for_status()  # Raises HTTPStatusError bad reqs
            ads = await response.json()
        except Exception as e:
            raise ClientError(f"Failed to connect to eBay API: {e}")
    return ads
