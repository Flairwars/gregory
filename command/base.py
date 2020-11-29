import discord
from discord.ext import commands

class base_commands(commands.Cog):
    """
    Generic commands. not much function
    """
    def __init__(self, bot):
        self.bot = bot

    
    #returns a link to the github
    @commands.command(aliases=['git'])
    async def github(ctx):
        """
        sends link to the github repo
        """
        await ctx.send('https://github.com/Blotz/gregory')

    #testing with different arguements
    @commands.command()
    async def test(ctx, *args):
        """
        dumb test command
        """
        await ctx.send('{} arguments: {}'.format(len(args), ', '.join(args)))


def setup(bot):
    bot.add_cog(base_commands(bot))