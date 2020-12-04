import discord
from discord.ext import commands

class poll(commands.Cog):
    '''
    docs
    '''
    def __init__(self, client):
        self.client = client
    
    @commands.command(aliases=['poll2', 'poll2electricboogaloo'])
    async def pollv2(self, ctx, arg, *args):
        await ctx.send(f'{arg}')
        for n in args:
            print(n)



def setup(client):
    client.add_cog(poll(client))