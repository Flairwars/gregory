from time import time
from discord.ext import commands
import pathlib
import os

class system(commands.Cog, name='system'):
    """
    system commands
    """
    def __init__(self, client):
        self.client = client
        self.category = pathlib.Path(__file__).parent.absolute().name[4:]

    @commands.command()
    async def ping(self, ctx):
        """
        works out latancy of bot
        """
        t1 = time()
        msg = await ctx.send('`pong`')
        t2 = time()
        delay = t2-t1
        await msg.edit(content=f'`Pong! Latency is {round(delay*1000)}ms. API Latency is {round(self.client.latency  * 1000)}ms`')

    # Loading and unloading of cogs for testing
    @commands.command()
    @commands.is_owner()
    async def load(self, ctx, name):
        """
        loads a cog of commands
        """
        name = name.lower()

        print(f'loading {name}...')
        if name in os.listdir(f'./commands'):
            for cog in os.listdir(f'./commands/{name}'):
                if cog.endswith('.py'):
                    try:
                        self.client.load_extension(f'commands.{name}.{cog[:-3]}')
                    except:
                        pass
            print('success!')
            return await ctx.send(f'`successfully loaded category {name}`')
        else:
            for category in os.listdir(f'./commands'):
                for cog in os.listdir(f'./commands/{category}'):
                    if name == cog[:-3]:
                        self.client.load_extension(f'commands.{category}.{name}')
                        print('success!')
                        return await ctx.send(f'`successfully loaded {name}`')

    # print(f'loading {input}...')
    # self.client.load_extension(f'commands.{input}')
    # await ctx.send(f'`successfully unloaded {input}`')
    # print('success!')


    @commands.command()
    @commands.is_owner()
    async def unload(self, ctx, name):
        """
        unloads a cog of commands
        """
        name = name.lower()

        print(f'loading {name}...')
        if name in os.listdir(f'./commands'):
            for cog in os.listdir(f'./commands/{name}'):
                if cog.endswith('.py'):
                    try:
                        self.client.unload_extension(f'commands.{name}.{cog[:-3]}')
                    except:
                        pass
            print('success!')
            return await ctx.send(f'`successfully loaded category {name}`')
        else:
            for category in os.listdir(f'./commands'):
                for cog in os.listdir(f'./commands/{category}'):
                    if name == cog[:-3]:
                        self.client.unload_extension(f'commands.{category}.{name}')
                        print('success!')
                        return await ctx.send(f'`successfully loaded {name}`')

        #print(f'unloading {input}...')
        #self.client.unload_extension(f'commands.{input}')
        #await ctx.send(f'`successfully unloaded {input}`')
        #print('success!')

    @commands.command()
    @commands.is_owner()
    async def reload(self, ctx, name):
        """
        reloads a cog of commands
        """
        name = name.lower()

        print(f'loading {name}...')
        if name in os.listdir(f'./commands'):
            for cog in os.listdir(f'./commands/{name}'):
                if cog.endswith('.py'):
                    try:
                        self.client.reload_extension(f'commands.{name}.{cog[:-3]}')
                    except:
                        pass
            print('success!')
            return await ctx.send(f'`successfully loaded category {name}`')
        else:
            for category in os.listdir(f'./commands'):
                for cog in os.listdir(f'./commands/{category}'):
                    if name == cog[:-3]:
                        self.client.reload_extension(f'commands.{category}.{name}')
                        print('success!')
                        return await ctx.send(f'`successfully loaded {name}`')

        #print(f'reloading {input}...')
        #self.client.reload_extension(f'commands.{input}')
        #await ctx.send(f'`successfully reloaded {input}`')
        #print('success!')


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