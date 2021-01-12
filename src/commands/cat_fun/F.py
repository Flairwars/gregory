import pathlib
from random import randint

from discord.ext import commands
respects_id = 587602797139329064
st_id = 708108259348709479
greg_id = 771011111242956820


class fInChat(commands.Cog, name='fInChat'):
    """
    F
    """
    def __init__(self, client):
        self.client = client
        self.category = pathlib.Path(__file__).parent.absolute().name[4:]

    @commands.Cog.listener()
    async def on_message(self, message):

        if message.content == "F" and (randint(1, 6) == 1) and not (message.author.id in [greg_id, st_id]):
            await message.channel.send("F")
            if randint(1, 17) == 1:
                await message.channel.send("wait") #F...wait

        if (message.author.id == st_id) and (message.channel.id == respects_id): #responds to ST's Fs
            await message.channel.send("F")

#I'm only commenting this cause it's good coding practice but honestly a 4 year-old could probably understand this code
