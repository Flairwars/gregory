from discord.ext import commands
import aiohttp
import io, discord, re
from PIL import Image, ImageChops


class recolour(commands.Cog, name='useful'):
    """
    Gregory is a dank memer :sunglasses:
    """
    def __init__(self, client):
        self.client = client


    def isImage(self, data):
        try:
            Image.open(io.BytesIO(data))
        except IOError:
            return False
        return True



    @commands.command(aliases=['recolor', 'rc'])
    async def recolour(self, ctx, colour='green', strength:float=100):
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
        if not ctx.message.attachments:
            foundImage = False
            msgLimit = 200
            regex = re.compile(r'https?:/.*\.(png|jpg|jpeg|gif|jfif|bmp)')
            
            searchingMessage = await ctx.send(f'Searching for image in last {msgLimit} messages…')
            async with aiohttp.ClientSession() as session:
                async for msg in ctx.channel.history(limit=msgLimit): # regex to check for images in links
                    if msg.attachments:
                        data = await msg.attachments[0].read()
                        if not self.isImage(data): continue
                        foundImage = True
                        break

                    m = regex.search(msg.content)
                    if m:
                        async with session.get(m.group()) as resp:
                            data = await resp.read()
                            if not self.isImage(data): continue
                            foundImage = True
                            break
            await searchingMessage.edit(content=f'Searching for Image in last {msgLimit} messages…{"No "* False * foundImage}Image {"successfully " * foundImage}found in last {msgLimit} messages.')

        else: # If there is an attachment, just read the data from it.
            data = await ctx.message.attachments[0].read()

        img = Image.open(io.BytesIO(data))
        img = img.convert('RGBA') # In case image (e.g. JPG) is in 'RGB' or else mode.

        for i in range(0, img.size[0]): # process all pixels
            for j in range(0, img.size[1]):
                pixelData = img.getpixel((i, j))
                newColour = tuple(abs(pixelData[n] + round(additionColours[colour][n] * strength)) for n in range(4))
                img.putpixel((i, j), newColour)

        # Send image to discord without saving to file
        imgBytesArr = io.BytesIO()
        img.save(imgBytesArr, format='PNG')
        imgBytesArr.seek(0)
        f = discord.File(imgBytesArr, 'recolour.png')
        await ctx.send(f'{colour}@{int(strength * 100)}%', file=f)


    @recolour.error
    async def recolour_error(self, ctx, error):
        if isinstance(error, commands.errors.BadArgument):
            await ctx.send('`ERROR: Invalid Syntax`')
        elif isinstance(error, discord.errors.DiscordException):
            await ctx.send('`ERROR: Invalid Colour`')


def setup(client):
    client.add_cog(recolour(client))
