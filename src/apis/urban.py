import aiohttp
import asyncio
from bs4 import BeautifulSoup
"""
This will be a webscraper for Urban Dictionary, as it does not possess a public API that can be used.
"""
async def getHTML(query):
    async with aiohttp.ClientSession() as session:
        async with session.get(f'https://www.urbandictionary.com/define.php?term={query.lower()}') as response:
            html = await response.text()
            return html

async def getContent(query):
    soup = BeautifulSoup(await getHTML(query), 'html.parser')
    defs = soup.find(id = 'content').find_all('div', {'class': 'def-panel'})

    for d in defs:
        print(d.prettify() + '\n--------------------------------------------------------\n')

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(getContent('ritz'))
