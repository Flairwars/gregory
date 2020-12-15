import asyncio
import json
from random import randint

import aiohttp

async def get_data(id):
    async with aiohttp.ClientSession() as session:
        if id == ' ' or id.isnumeric() == False:
            async with session.get(f'http://xkcd.com/info.0.json') as response:
                json = await response.json()
                id = randint(1, json['num'])

        async with session.get(f'http://xkcd.com/{id}/info.0.json') as response:
            return await response.json()

async def get_xkcd(id = ' '):
    data = await get_data(id)
    return data

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(get_xkcd())