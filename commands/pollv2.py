import datetime
import discord
from discord.ext import commands
from converter.datetimeCalc import datetimeCal



class poll(commands.Cog):
    '''
    super fancy shmancy poll command
    '''
    def __init__(self, client):
        self.client = client
    
    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        print(payload)


    @commands.command(aliases=['poll2electricboogaloo'])
    async def poll2(self, ctx, time: datetimeCal, *, args):
        """
        .poll2 7d2h {who do you want to vote lol?} [arg1] [arg2]
        """
        name = args.split('}')
        args = name[1]
        name = name[0][1:]
        
        argList = []
        while args.find(']') != -1:
            arg = args.split('}')
            try:
                args = arg[1]
                arg.append(arg[0][1:])
            except Exception as e:
                arg.append(args[0])
                break
        
        print(argList)

        message = await ctx.send(name)

        pass

    @commands.command()
    async def test(self, ctx, time: datetimeCal, name, *args):
        message = await ctx.send(name)
        print(message)
        pass


def setup(client):
    client.add_cog(poll(client))