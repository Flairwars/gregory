import discord
from discord.ext import commands

class base(commands.Cog):
    '''
    docs
    '''
    def __init__(self, client):
        self.client = client
    
    @commands.command()
    async def poll(self, ctx):
        pass


def setup(client):
    client.add_cog(base(client))