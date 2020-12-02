from decouple import config

from discord.ext import commands
from command import *

bot = commands.Bot(command_prefix = '%')

base.setup(bot)
roles.setup(bot)


#prints when bot has started up
@bot.event
async def on_ready():
    print('Bot is ready')


bot.run(config('TOKEN'))