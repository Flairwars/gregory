import discord
from discord.ext import commands

class base(commands.Cog, name='Basic Commands'):
    '''
    basic commands
    does simple things which all users have access to
    '''
    def __init__(self, client):
        self.client = client

    @commands.command()
    async def ping(self, ctx):
        """
        : works out latancy of bot
        """
        await ctx.send(f'Pong! {round(self.client.latency * 1000)}ms')

    @commands.command(aliases=['git'])
    async def github(ctx):
        """
        : sends link to the github repo
        """
        await ctx.send('https://github.com/Blotz/gregory')
    

def setup(client):
    client.add_cog(base(client))