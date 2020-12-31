from discord.ext import commands
from importlib import import_module
import pathlib
import pprint

class help(commands.Cog, name='cat_help'):
    '''
    Help Command
    '''

    def __init__(self, client):
        self.client = client
        self.category = pathlib.Path(__file__).parent.absolute().name[4:]

    @commands.command()
    async def help(self, ctx,*cog):
        for cog in self.client.cogs.values():
            print(cog.category)
        pass

def setup(client):
    client.add_cog(help(client))