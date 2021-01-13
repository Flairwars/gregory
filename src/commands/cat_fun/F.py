import pathlib
from random import randint

from discord.ext import commands
respects_id = 587602797139329064
st_id = 708108259348709479


class fInChat(commands.Cog, name='fInChat'):
    """
    F
    """
    def __init__(self, client):
        self.client = client
        self.category = pathlib.Path(__file__).parent.absolute().name[4:]

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author == self.client.user:
            return

        if message.content == "F" and (randint(1, 6) == 1 or message.author.id != st_id):
            await message.channel.send("F")
            if randint(1, 17) == 1:
                await message.channel.send("wait") #F...wait

#I'm only commenting this cause it's good coding practice but honestly a 4 year-old could probably understand this code
