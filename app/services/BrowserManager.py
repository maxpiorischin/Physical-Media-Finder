user_agent = "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Mobile Safari/537.36"

async def newPage(browser):
    context = await browser.new_context(
        user_agent=user_agent
    )
    page = await context.new_page()
    return page
