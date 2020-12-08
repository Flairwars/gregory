import discord
import random
from discord.ext import commands
from random import randint

allowedChannels = [588354715625193473, 579538738988711958]


class jokes(commands.Cog, name='memery bullshit'):
    """
    Gregory is a dank memer :sunglasses:
    """
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_message(self, message):

        if message.author == self.client.user:
            return
        
        if "fuck" in message.content.lower() and message.channel.id in allowedChannels:
            fBombs = message.content.lower().count("fuck")
            if fBombs == 1:
                plural = "f-bomb"
            else:
                plural = "f-bombs"
            await message.channel.send("**Hello!**" + chr(13) + f"I noticed you dropped **{fBombs} {plural}** in this comment. This might be necessary, but using nicer language makes the whole world a better place." + chr(13) + "Maybe you need to blow off some steam - in which case, go get a drink of water and come back later. This is just the internet and sometimes it can be helpful to cool down for a second." + chr(13) + ":hearts::hearts::hearts:")
            
def setup(client):
    client.add_cog(jokes(client))