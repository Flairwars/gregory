from decouple import config
import os

import discord
from discord.ext import commands

# add discord bot perms
intents = discord.Intents.default()
intents.presences - True
intents.members = True
client = commands.Bot(command_prefix = '.', intents=intents)

# loads all cogs 
for filename in os.listdir('./commands'):
    if filename.endswith('.py'):
        client.load_extension(f'commands.{filename[:-3]}')

# checks
def is_owner(ctx):
    return ctx.author.id == 510539578827079680

# prints when bot has started up
@client.event
async def on_ready():
    print('bot done')

# error handleing 
@client.event
async def on_command_error(ctx,error):
    pass

# loads a cog
@client.command()
@commands.check(is_owner)
async def load(ctx, cog):
    '''
    loads a catagory of commands
    '''
    client.load_extension(f'commands.{cog}')
    await ctx.send(f'successfully loaded {cog}')


@client.command()
@commands.check(is_owner)
async def unload(ctx, cog):
    '''
    unloads a catagory of commands
    '''
    client.unload_extension(f'commands.{cog}')
    await ctx.send(f'successfully unloaded {cog}')

@client.command()
@commands.check(is_owner)
async def reload(ctx, cog):
    '''
    reloads a catagory of commands
    '''
    client.unload_extension(f'commands.{cog}')
    client.load_extension(f'commands.{cog}')
    await ctx.send(f'successfully reloaded {cog}')

client.run(config('TOKEN'))