import pathlib

from discord.ext import commands
from discord.ext.commands.core import command

class automated_honchon(commands.Cog, name='automated_honcon'):
    """
    Automates basic honcon voting requests.
    """
    def __init__(self, client):
        self.client = client
        self.category = pathlib.Path(__file__).parent.absolute().name[4:]

    @commands.command()
    async def honcon(self, ctx, type):
