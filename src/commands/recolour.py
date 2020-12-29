from discord.ext import commands


class recolour(commands.Cog, name='useful'):
    """
    Gregory is a dank memer :sunglasses:
    """
    def __init__(self, client):
        self.client = client

    @commands.command()
    async def test(self, ctx):
        await ctx.send('test')

def setup(client):
    client.add_cog(recolour(client))
