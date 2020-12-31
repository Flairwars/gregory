from discord.ext import commands
from importlib import import_module
import pprint

class help(commands.Cog, name='help'):
    '''
    Help Command
    '''

    def __init__(self, client):
        self.client = client

    @commands.command()
    async def help(self, ctx,*cog):
        pp = pprint.PrettyPrinter(indent=4)
        pp.pprint(self.client.cogs)
        from src.commands import misc
        test = import_module('src.commands.misc')
        test = test.__getattribute__('misc')
        await test.github()
def setup(client):
    client.add_cog(help(client))