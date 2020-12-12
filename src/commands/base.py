import discord
from discord.ext import commands

class base(commands.Cog, name='Basic Commands'):
    '''
    basic commands
    does simple things which all users have access to
    '''
    def __init__(self, client):
        self.client = client

    @commands.command(aliases=['git'])
    async def github(self, ctx):
        """
        : sends link to the github repo
        """
        await ctx.send('https://github.com/Blotz/gregory')
    

def setup(client):
    client.add_cog(base(client))