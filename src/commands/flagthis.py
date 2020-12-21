import discord
from discord.ext import commands

class flagthis(commands.Cog, name='Flagging so you don\'t have to'):
    '''
    Kind of like a poll command, but
    a flag instead
    '''
    def __init__(self, client):
        self.client = client


    async def flagthis(self, ctx):
        """
        : adds flag reaction to the message
        """
        emoji = '<:flag:584174141737926666>'
        await ctx.add_reaction(emoji)


def setup(client):
    client.add_cog(base(client))
