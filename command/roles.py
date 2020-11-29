import discord
from discord.ext import commands

class persistant_role(commands.Cog, name='commands for persistant roles'):
    """
    comands and functions for the persistant roles
    """
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_member_join(self, member):
        """
        auto runs when members run
        """
        pass
        #await channel.send('Welcome {0.mention}.'.format(member))
        

    #returns a link to the github
    @commands.command()
    async def test2(self, ctx):
        """
        sends link to the github repo
        """
        pass



def setup(bot):
    bot.add_cog(persistant_role(bot))