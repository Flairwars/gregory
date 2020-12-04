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


# prints when bot has started up
@client.event
async def on_ready():
    print('bot done')

# Loading and unloading of cogs for testing
@client.command()
@commands.is_owner()
async def load(ctx, cog):
    '''
    : loads a catagory of commands
    '''
    print(f'loading {cog}...')
    client.load_extension(f'commands.{cog}')
    await ctx.send(f'successfully loaded {cog}')
    print('success!')


@client.command()
@commands.is_owner()
async def unload(ctx, cog):
    '''
    : unloads a catagory of commands
    '''
    print(f'unloading {cog}...')
    client.unload_extension(f'commands.{cog}')
    await ctx.send(f'successfully unloaded {cog}')
    print('success!')

@client.command()
@commands.is_owner()
async def reload(ctx, cog):
    '''
    : reloads a catagory of commands
    '''
    print(f'reloading {cog}...')
    client.unload_extension(f'commands.{cog}')
    client.load_extension(f'commands.{cog}')
    await ctx.send(f'successfully reloaded {cog}')
    print('success!')


# Loading and unloading of cogs Error handling
@load.error
async def load_error(ctx, error):
    # error if cog doesnt exist
    if isinstance(error, commands.CommandInvokeError):
        await ctx.send('`ERROR: cog has not been loaded`')
    
    # error if user is not bot owner/insufficant perms 
    if isinstance(error, commands.errors.NotOwner):
        await ctx.send('`ERROR: insufficant perms to run this command`')
    print('failure!')

@unload.error
async def unload_error(ctx, error):
    # error if cog doesnt exist
    if isinstance(error, commands.CommandInvokeError):
        await ctx.send('`ERROR: cog has not been unloaded`')
    
    # error if user is not bot owner/insufficant perms 
    if isinstance(error, commands.errors.NotOwner):
        await ctx.send('`ERROR: insufficant perms to run this command`')
    print('failure!')


@reload.error
async def reload_error(ctx, error):
    # error if cog doesnt exist
    if isinstance(error, commands.CommandInvokeError):
        await ctx.send('`ERROR: cog has not been reloaded`')
    
    # error if user is not bot owner/insufficant perms 
    if isinstance(error, commands.errors.NotOwner):
        await ctx.send('`ERROR: insufficant perms to run this command`')
    print('failure!')


client.run(config('TOKEN'))