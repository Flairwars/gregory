import logging

import aiohttp
from discord import errors
from discord.ext import commands

log = logging.getLogger(__name__)

class inspire(commands.Cog, name='fun'):
    """
    Pings inspirobot API and sends the image
    """
    def __init__(self, client):
        self.client = client

    @commands.command(aliases=['inspireme', 'insp'])
    async def inspire(self, ctx, n:int=1):
        """
        Sends an image from inspirobot. Number of images to be sent can be passed (max 5).
        n = number of images sent (limit = 5)
        """
        if n > 5 or n < 0:
            raise errors.DiscordException

        async with aiohttp.ClientSession() as session:
            for i in range(n):
                async with session.get('https://inspirobot.me/api?generate=true') as resp:
                    await ctx.send((await resp.read()).decode('utf-8')) # .decode because it gives a bytestring for some reason.

    @inspire.error
    async def inspire_error(self, ctx, error):
        if isinstance(error, errors.DiscordException):
            await ctx.send('`ERROR: Between 1 and 5 images`')
        else:
            await ctx.send(f'`{error}`')


def setup(client):
    log.debug(f'loading {__name__}')
    client.add_cog(inspire(client))


def teardown(client):
    log.debug(f'{__name__} unloaded')
