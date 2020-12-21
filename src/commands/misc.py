from discord.ext import commands
from PIL import ImageColor, Image
import discord
import io
class misc(commands.Cog):
    '''
    super fancy shmancy poll command
    '''
    def __init__(self, client):
        self.client = client
    
    @commands.command(aliases=['colour'])
    async def color(self, ctx, hex : str):
        '''
        : creates color image and sends it
        '''
        if not hex.startswith('#'):
            hex ='#'+hex
        
        color = ImageColor.getrgb(hex)
        img = Image.new('RGB', (600, 200), color = color)

        arr = io.BytesIO()
        img.save(arr, format='PNG')
        arr.seek(0)
        file = discord.File(arr, 'color.png')

        embed = discord.Embed(title=hex, color=discord.Color.green())
        embed.set_image(url='attachment://color.png')
        await ctx.send(file=file, embed=embed)

    @color.error
    async def color_error(self, ctx, error):
        if isinstance(error, commands.CommandInvokeError):
            await ctx.send('`ERROR: invalid hex code`')

    @commands.command()
    async def flagthis(self, ctx):
        """
        : adds flag reaction to the message
        """
        emoji = '<:flag:584174141737926666>'
        await ctx.message.add_reaction(emoji)

def setup(client):
    client.add_cog(misc(client))