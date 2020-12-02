import discord
from discord.ext import commands

class base(commands.Cog):
    '''
    docs
    '''
    def __init__(self, client):
        self.client = client


    @commands.Cog.listener()
    async def on_member_join(member):
        print(f'{member} has joined the server')

    @commands.Cog.listener()
    async def on_member_remove(member):
        print(f'{member} has left the server')

    @commands.command()
    async def ping(self, ctx):
        await ctx.send('pomg')

    @commands.command(aliases=['git'])
    async def github(ctx):
        """
        sends link to the github repo
        """
        await ctx.send('https://github.com/Blotz/gregory')
    

def setup(client):
    client.add_cog(base(client))