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
        self.uwu_conversions = {}
        self.populate_uwu()

    def populate_uwu(self):
        self.uwu_conversions['the'] = 'da'
        self.uwu_conversions['The'] = 'Da'

        self.uwu_conversions['you'] = 'u'
        self.uwu_conversions['You'] = 'U'

        self.uwu_conversions['are'] = 'ish'
        self.uwu_conversions['Are'] = 'Ash'

        self.uwu_conversions['is'] = 'ish'
        self.uwu_conversions['Is'] = 'Ish'

        self.uwu_conversions['r'] = 'w'
        self.uwu_conversions['R'] = 'W'

        self.uwu_conversions['l'] = 'w'
        self.uwu_conversions['L'] = 'W'

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
            await message.channel.send("**Hello!**" + chr(
                13) + f"I noticed you dropped **{fBombs} {plural}** in this comment. This might be necessary, but using nicer language makes the whole world a better place." + chr(
                13) + "Maybe you need to blow off some steam - in which case, go get a drink of water and come back later. This is just the internet and sometimes it can be helpful to cool down for a second." + chr(
                13) + ":hearts::hearts::hearts:")

    @commands.command(aliases=['uwu', 'uwuify', 'owo', 'owoify', 'owoifier'])
    async def uwuifier(self, ctx, *, message):
        for key, value in self.uwu_conversions.items():
            message = message.replace(key, value)
        await ctx.send(message)


def setup(client):
    client.add_cog(jokes(client))
