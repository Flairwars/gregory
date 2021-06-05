import asyncio

import aiohttp
from bs4 import BeautifulSoup


async def getHTML():
    # Grabs the HTML of the needed website asynchronously with aiohttp
    async with aiohttp.ClientSession() as session:
        async with session.get('https://www.either.io') as response:
            html = await response.text()
            return html


async def get_wyr():
    html = await getHTML()
    html = html[:html.find('<div id=\"sub-banner-wrapper\">')]
    soup = BeautifulSoup(html, 'html.parser')

    options = soup.find(id='question').find_all('span', {'class': 'option-text'})
    content = {'blue': options[0].get_text(), 'red': options[1].get_text()}
    return content


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(get_wyr())
