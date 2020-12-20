import discord
from discord.ext import commands

class system(commands.Cog, name='System commands'):
    '''
    system commands
    '''
    def __init__(self, client):
        self.client = client

    @commands.command()
    async def ping(self, ctx):
        """
        : works out latancy of bot
        """
        await ctx.send(f'Pong! Latency is {round(self.client.latency * 1000)}ms. API Latency is {round(self.client.latency  * 1000)}ms')

    # Loading and unloading of cogs for testing
    @commands.command()
    @commands.is_owner()
    async def load(self, ctx, cog):
        '''
        : loads a catagory of commands
        '''
        print(f'loading {cog}...')
        self.client.load_extension(f'commands.{cog}')
        await ctx.send(f'successfully loaded {cog}')
        print('success!')

    @commands.command()
    @commands.is_owner()
    async def unload(self, ctx, cog):
        '''
        : unloads a catagory of commands
        '''
        print(f'unloading {cog}...')
        self.client.unload_extension(f'commands.{cog}')
        await ctx.send(f'successfully unloaded {cog}')
        print('success!')

    @commands.command()
    @commands.is_owner()
    async def reload(self, ctx, cog):
        '''
        : reloads a catagory of commands
        '''
        print(f'reloading {cog}...')
        self.client.unload_extension(f'commands.{cog}')
        self.client.load_extension(f'commands.{cog}')
        await ctx.send(f'successfully reloaded {cog}')
        print('success!')



    # Loading and unloading of cogs Error handling
    @load.error
    async def load_error(self, ctx, error):
        # error if cog doesnt exist
        if isinstance(error, commands.CommandInvokeError):
            await ctx.send('`ERROR: cog has not been loaded`')
        
        # error if user is not bot owner/insufficant perms 
        if isinstance(error, commands.errors.NotOwner):
            await ctx.send('`ERROR: insufficant perms to run this command`')
        print('failure!')

    @unload.error
    async def unload_error(self, ctx, error):
        # error if cog doesnt exist
        if isinstance(error, commands.CommandInvokeError):
            await ctx.send('`ERROR: cog has not been unloaded`')
        
        # error if user is not bot owner/insufficant perms 
        if isinstance(error, commands.errors.NotOwner):
            await ctx.send('`ERROR: insufficant perms to run this command`')
        print('failure!')

    @reload.error
    async def reload_error(self, ctx, error):
        # error if cog doesnt exist
        if isinstance(error, commands.CommandInvokeError):
            await ctx.send('`ERROR: cog has not been reloaded`')
        
        # error if user is not bot owner/insufficant perms 
        if isinstance(error, commands.errors.NotOwner):
            await ctx.send('`ERROR: insufficant perms to run this command`')
        print('failure!')

def setup(client):
    client.add_cog(system(client))