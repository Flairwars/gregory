import discord
from discord.ext import commands, tasks
from utils import count_utils


class Util(commands.Cog, name='Utilities'):
    '''
    No commands. Just utilities
    '''

    def __init__(self, client):
        self.client = client

    @tasks.loop(minutes=60.0)
    async def update_colour_database(self):
        count_utils.update_database()


def setup(client):
    client.add_cog(Util(client))
