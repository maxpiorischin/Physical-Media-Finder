import re, asyncio
from fastapi import HTTPException
user_agent = "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Mobile Safari/537.36"

async def newPage(browser):
    context = await browser.new_context(
        user_agent=user_agent,
        permissions=["geolocation"]
    )
    page = await context.new_page()
    return page

async def retry_async(func, max_attempts=3, delay=1, *args, **kwargs):
    """Retry an async function up to max_attempts times with a delay between attempts.

    Args:
        func: The async function to be retried.
        max_attempts (int): Maximum number of attempts.
        delay (int or float): Delay between attempts in seconds.

    Returns:
        The return value of the function or None if it fails.
    """
    msg = ""
    for attempt in range(max_attempts):
        try:
            return await func(*args, **kwargs)
        except Exception as e:
            msg = e
            print(f"Attempt {attempt + 1} failed with error: {e}")
            if attempt < max_attempts - 1:
                await asyncio.sleep(delay)  # Delay before next retry
    raise HTTPException(status_code=500, detail=str(msg))

async def valid_postal_code(postal_code):
    postal_code_pattern = r'^[A-Za-z]\d[A-Za-z]\d[A-Za-z]\d$'
    return re.match(postal_code_pattern, postal_code)

async def valid_search(user_search, character_limit = 20): #simple for validating the user search
    return len(user_search) < character_limit
