from discord.ext import commands
from PIL import ImageColor, Image
import discord
import io
class poll(commands.Cog):
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

def setup(client):
    client.add_cog(poll(client))