import discord
from discord.ext import commands

from apis import urban

class search(commands.Cog, name='Search Commands'):
    '''
    Search Commands
    With this you can search for content on various websites :)
    '''
    def __init__(self, client):
        self.client = client

    @commands.command()
    async def urban(ctx, *, term):
        """
        : Looks up a term on Urban Dictionary
        """
        definition = urban.getDefinition("ritz")
        print(definition)
    

def setup(client):
    client.add_cog(base(client))