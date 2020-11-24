import discord
from discord.ext import commands

from decouple import config
import datetime

client = commands.Bot(command_prefix = '%')


###############################################################################
def get_datetime(str):
    """
    converts YYMMWWDD HHMMSS to datetime
    """
    '3H6D1Y2S50M'
    str = str.lower()
    
    lst = []
    for time in ('d','h','m','s'):
        
        index = str.find(time)
        if index != -1:
            lst.append({index:time})

    
        

    



@client.event
async def on_ready():
    print('Bot is ready')

@client.command()
async def test(ctx, *args):

    await ctx.send('{} arguments: {}'.format(len(args), ', '.join(args)))










client.run(config('TOKEN'))