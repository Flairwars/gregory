import asyncio
import json

import aiohttp

async def get_weather_data(query):
    async with aiohttp.ClientSession() as session:
        async with session.get(f'https://wttr.in/{query.lower().replace(" ","+")}?format=j1') as response:
            return await response.json()

async def get_current(query):
    data = await get_weather_data(query)
    if data['request'][0]['query'] == 'Not, Austria':
        return None
    else:
        data = data['current_condition'][0]
        return data

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(get_current('london'))