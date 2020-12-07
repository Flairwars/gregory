import discord
import random
from discord.ext import commands
from random import randint

class jokes(commands.Cog, name='memery bullshit'):
    """
    add a lil discription
    """
    def __init__(self, client):
        self.client = client

    @commands.command()
    async def fuck(self, ctx):
        """
        this is the fuck command. i think its self explanitory
        """
        await ctx.send("**Hello!**" + chr(13) + f"I noticed you dropped **1 f-bomb** in this comment. This might be necessary, but using nicer language makes the whole world a better place." + chr(13) + "Maybe you need to blow off some steam - in which case, go get a drink of water and come back later. This is just the internet and sometimes it can be helpful to cool down for a second." + chr(13) + ":hearts::hearts::hearts:")

    @commands.command()
    async def eatluna(self, ctx):
        """
        for when you want to eat luna i guess
        """
        if randint(1,2) == 1:
            await ctx.send("https://cdn.discordapp.com/attachments/691946326962864168/785612929717764106/eatLuna1.png")
        else:
            await ctx.send("https://cdn.discordapp.com/attachments/691946326962864168/785612927389401088/eatLuna2.png")


    @commands.Cog.listener()
    async def on_message(self, message):

        if message.author == self.client.user:
            return
        
        if "fuck" in message.content.lower():
            fBombs = message.content.lower().count("fuck")
            if fBombs == 1:
                plural = "f-bomb"
            else:
                plural = "f-bombs"
            await message.channel.send("**Hello!**" + chr(13) + f"I noticed you dropped **{fBombs} {plural}** in this comment. This might be necessary, but using nicer language makes the whole world a better place." + chr(13) + "Maybe you need to blow off some steam - in which case, go get a drink of water and come back later. This is just the internet and sometimes it can be helpful to cool down for a second." + chr(13) + ":hearts::hearts::hearts:")


def setup(client):
    client.add_cog(jokes(client))