from discord.ext import commands, tasks
from utils import count_utils


class Util(commands.Cog, name='Utils'):
    '''
    No commands. Just utilities
    '''
    def __init__(self, client):
        self.client = client

def setup(client):
    client.add_cog(Util(client))
