import aiohttp, os


def get_api_key():
    """
    in a function since in want it so be called rather than immediately setting this value to
    null before doing load_dotenv
    """
    return os.environ.get("EBAY_API_KEY")


async def get_ebay_ads(user_input, user_location):
    api_key = get_api_key()
    #use api key once availble
    return [api_key]
