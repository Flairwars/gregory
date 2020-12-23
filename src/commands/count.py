from discord.ext import commands
from utils import count_utils

class count(commands.Cog, name='useful'):
    '''
    Count command shiz
    '''
    def __init__(self, client):
        self.client = client
    
    @commands.command(aliases=["c"])
    async def count(self, ctx, col = " "):
        '''
        : count the other color subs
        '''
        data = await count_utils.get_stats(col.strip())
        if data is None:
            await ctx.send("There was a problem. Did you have a huge typo in the colour?")
        else:
            response = f'**Situation over on {data["colour"][0].upper() + data["colour"][1:]}**'
            for page in range(0,5):
                response += f'\n**Page {page+1}**\n'
                for key in data[page].keys():
                    response += key + " : " + str(data[page][key]) + "\n"

            await ctx.send(response)




def setup(client):
    client.add_cog(count(client))