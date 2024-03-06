import aiohttp, os
from aiohttp import ClientError

EBAY_API_URL = "https://api.ebay.com/buy/browse/v1/item_summary/search" #url to search for an item
EBAY_TOKEN_GEN_URL = "https://api.ebay.com/identity/v1/oauth2/token" #url for generating a new access token
DEFAULT_LIMIT = 10 #limit of how many items to request for

request_headers = {
    'Authorization': 'temp',
    'X-EBAY-C-MARKETPLACE-ID': 'EBAY_ENCA',
    'X-EBAY-C-ENDUSERCTX': 'affiliateCampaignId=<ePNCampaignId>,affiliateReferenceId=<referenceId>'
} #header for making browse item requests, authorization is set by regenerate_ebay_token() on startup


async def regenerate_ebay_token():
    """
    Regenerate Ebay token (only lasts 2 hrs)
    """
    client_id, client_secret = os.environ.get('EBAY_CLIENT_ID'), os.environ.get('EBAY_CLIENT_SECRET')
    headers = {
        "Content-Type": "application/x-www-form-urlencoded",
        "Accept": "application/json"
    }
    data = {
        "grant_type": "client_credentials",
        "scope": "https://api.ebay.com/oauth/api_scope"
    }

    auth = aiohttp.BasicAuth(login=client_id, password=client_secret)

    async with aiohttp.ClientSession() as session:
        try:
            response = await session.post(EBAY_TOKEN_GEN_URL, headers=headers, data=data, auth=auth)
            response.raise_for_status()  # raise an exception if for 400 or 500 error
            tokens = await response.json()
            access_token = tokens.get('access_token')
            request_headers['Authorization'] = f"Bearer {access_token}" #set request headers authorization to the access token
            return True
        except Exception as e:
            raise ClientError(f"Failed to generate api token with error msg: {e}")


async def parse_ebay_listings(json_data):
    # This list will hold the parsed listings
    parsed_listings = []

    #if there isnt itemsummaries then there is no results
    if 'itemSummaries' in json_data:
        for item in json_data['itemSummaries']:
            # Relavent details
            listing = {
                'title': item.get('title', ''),
                'link': item.get('itemWebUrl', ''),
                'price': item.get('price', {}).get('value', '') + ' ' + item.get('price', {}).get('currency', ''),
                'image_links': [image['imageUrl'] for image in item.get('thumbnailImages', [])],
                'itemLocation': item.get('itemLocation', {}).get('country', '') + ', ' + item.get('itemLocation',
                                                                                                  {}).get('postalCode',
                                                                                                          ''),
                'condition': item.get('condition', ''),
                'availableCoupons': item.get('availableCoupons', False),
                'itemCreationDate': item.get('itemCreationDate', ''),
            }
            # Append the listing to the parsed listings list
            parsed_listings.append(listing)

    return parsed_listings


async def get_ebay_ads(user_input, limit=DEFAULT_LIMIT):
    """
    Using request headers containing a generated ebay api key, search canadian ebay API for the user specified item
    :param limit: limit of how many ads
    :param user_input: the item which the user is searching for
    :return: json of ads
    """
    async with aiohttp.ClientSession() as session:
        link = f"{EBAY_API_URL}?q={user_input}&limit={limit}" #link with user input and limit of items
        try:
            response = await session.get(link, headers=request_headers)
            response.raise_for_status()  # Raises HTTPStatusError bad reqs
            response_content = await response.json()
            ads = await parse_ebay_listings(response_content) #parse the api response into a list of ads
        except Exception as e:
            raise ClientError(f"Failed to connect to eBay API: {e}")
    return ads
