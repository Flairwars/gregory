import logging
from random import randint

from discord.ext import commands

log = logging.getLogger(__name__)
respects_id = 587602797139329064
st_id = 708108259348709479


class F(commands.Cog, name='misc'):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author == self.client.user:
            return

        if (message.content == "F" and randint(1, 6) == 1) or (message.author.id == st_id and message.channel.id == respects_id):
            await message.channel.send("F")
            if randint(1, 600) == 1:
                await message.channel.send("wait") #F...wait


def setup(client):
    log.debug(f'loading {__name__}')
    client.add_cog(F(client))


def teardown(client):
    log.debug(f'{__name__} unloaded')
