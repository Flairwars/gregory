from discord.ext import commands
import aiohttp
import io, discord, re
from PIL import Image
import pathlib

from functools import partial

class recolour(commands.Cog, name='recolour'):
    """
    Recolor cog
    """
    def __init__(self, client):
        self.client = client
        self.category = pathlib.Path(__file__).parent.absolute().name[4:]

        self.msgLimit = 20
        self.reg = re.compile(r'https?:/.*\.(png|jpg|jpeg|gif|jfif|bmp)')

    @staticmethod
    def image_processing(img ,color, strength):
        '''
        recolors
        '''
        for i in range(0, img.size[0]): # process all pixels
            for j in range(0, img.size[1]):
                pixelData = img.getpixel((i, j))
                newColour = tuple(abs(pixelData[n] + round(color[n] * strength)) for n in range(4))
                img.putpixel((i, j), newColour)
        
        return img
        

    @commands.command(aliases=['recolour', 'rc'])
    async def recolor(self, ctx, colour='green', strength:float=100):
        '''
        Call with image attached. colour can be one of [red, orange, yellow, green, blue, purple], or just the first letter of any.
        If no image is attached, bot will search recent messages for the most recent image or image link.
        '''
        
        colour = colour.lower()
        # Strength and colour definitions
        strength /= 100
        additionColours = {
                'red'    : ( 255, -255, -255, 0),
                'orange' : ( 255,  127,    0, 0),
                'yellow' : ( 255,  255, -255, 0),
                'green'  : (-255,  255, -255, 0),
                'blue'   : (-255, -255,  255, 0),
                'purple' : ( 127, -255,  127, 0),
                'r' : 'red',
                'o' : 'orange',
                'y' : 'yellow',
                'g' : 'green',
                'b' : 'blue',
                'p' : 'purple'
        }
        if len(colour) == 1:
            colour = additionColours[colour]

        if colour not in additionColours:
            raise discord.errors.DiscordException


        # What to do when no attachment is sent with the file: Search prev. messages for a file, also for links.
        bot_msg = await ctx.send('`Editing images`')

        if ctx.message.attachments:
            data = await ctx.message.attachments[0].read()
        else:
            async for msg in ctx.channel.history(limit=self.msgLimit):
                # loop through x mssages
                if msg.attachments:
                    file_url = msg.attachments[0].url
                else:
                    file_url = ''

                message_url = self.reg.search(msg.content)
                if message_url:
                    message_url = message_url.group(0)

                #print(file_url, message_url)
                if self.reg.match(file_url) or message_url:# self.reg to check for images in links
                    url = file_url if file_url else message_url
                    # found attachment with image file format
                    async with aiohttp.ClientSession() as session:
                        async with session.get(url) as response:
                            data = await response.read()
                    break
            else:
                await bot_msg.edit(content = '`No image found`')
                return

        await bot_msg.edit(content = '`Image found!`')
        img = Image.open(io.BytesIO(data))
        img = img.convert('RGBA') # In case image (e.g. JPG) is in 'RGB' or else mode.


        fn = partial(self.image_processing, img, additionColours[colour], strength)
        img = await self.client.loop.run_in_executor(None, fn)

        # Send image to discord without saving to file
        imgBytesArr = io.BytesIO()
        img.save(imgBytesArr, format='PNG')
        imgBytesArr.seek(0)
        f = discord.File(imgBytesArr, 'recolour.png')

        await ctx.send(f'`{colour}@{int(strength * 100)}%`', file=f)
        await bot_msg.delete()


def setup(client):
    client.add_cog(recolour(client))
