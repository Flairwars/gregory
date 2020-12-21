import discord
from discord.ext import commands

class links(commands.Cog, name='Making it easier to link since 2020'):
    '''
    Links for everything you might need
    '''
    def __init__(self, client):
        self.client = client

    @commands.command(aliases = ['s', 'subreddit'])
    async def sub(self, ctx, color):
        """
        : links the subreddit for the specified color
        """




def setup(client):
    client.add_cog(links(client))
