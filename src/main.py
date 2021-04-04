import os
import discord
from discord.ext import commands
from decouple import config

# add discord bot perms
intents = discord.Intents.default()
intents.presences = True
intents.members = True

client = commands.Bot(command_prefix = '.', intents=intents)

# Remove standard cat_help command
client.remove_command('help')

# loads all cogs
for filename in os.listdir('./commands'):
    if filename.endswith('.py'):
        client.load_extension(f'commands.{filename[:-3]}')

# prints when bot has started up
@client.event
async def on_ready():
    print('bot done')

client.run(config('TOKEN'))
