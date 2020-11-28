import discord
from discord.ext import commands

from decouple import config


bot = commands.Bot(command_prefix = '%')


###############################################################################

#prints when bot has started up
@bot.event
async def on_ready():
    print('Bot is ready')

class base_commands(commands.Cog):
    """Cog description"""
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

bot.add_cog(base_commands())
bot.run(config('TOKEN'))