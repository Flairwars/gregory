import asyncio

import aiohttp
from bs4 import BeautifulSoup
"""
This is a webscraper for Urban Dictionary, as it does not possess a public API that can be used.
Run getContent(query) to get a Dictionary with all definitions of the query sorted in a list.
"""
async def getHTML(query):
    #Grabs the HTML of the needed website asynchronously with aiohttp
    async with aiohttp.ClientSession() as session:
        async with session.get(f'https://www.urbandictionary.com/define.php?term={query.lower()}') as response:
            html = await response.text()
            return html

async def getDefinitions(query):
    #Makes the HTML more easily accessible with BeautifulSoup
    soup = BeautifulSoup(await getHTML(query), 'html.parser')
    if soup.find(id = 'content') != None:
        defs = soup.find(id = 'content').find_all('div', {'class': 'def-panel'})

        definitions = []

        #Runs through the definitions and extracts the info from each one seperately
        for d in defs:
            content = {}
            content['title'] = d.find('div', {'class' : 'def-header'}).get_text()
            if content['title'].lower() != query.lower():
                continue

            content['meaning'] = d.find('div', {'class' : 'meaning'}).get_text()
            content['example'] = d.find('div', {'class' : 'example'}).get_text()

            content['contributor'] = {}
            content['contributor']['author'] = d.find('div', {'class' : 'contributor'}).get_text().split(' ')[1]
            content['contributor']['link'] = f'https://www.urbandictionary.com/author.php?author=' + content['contributor']['author']
            
            content['id'] = d.attrs['data-defid']
            definitions.append(content)

        return definitions
    else: 
        return -1

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(getDefinitions('ritz'))
