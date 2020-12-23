from discord.ext import commands
from PIL import ImageColor, Image
import discord
import io

class misc(commands.Cog, name='useful'):
    '''
    super fancy shmancy poll command
    '''
    def __init__(self, client):
        self.client = client
    
    @commands.command(aliases=['git'])
    async def github(self, ctx):
        """
        : sends link to the github repo
        """
        await ctx.send('https://github.com/Blotz/gregory')
        
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

    @commands.command(aliases = ['megainvite', 'megainv', 'megaInv'])
    async def megaInvite(self, ctx):
        """
        : provides a link to the megaserver
        """
        embed=discord.Embed(title="https://discord.com/invite/f647g7Z", url="https://discord.com/invite/f647g7Z", color=discord.Color.green())
        embed.set_author(name="Flairwars Megaserver")
        embed.set_thumbnail(url="https://cdn.discordapp.com/icons/463794005231271976/a_dad8b99b5351a2c8eaf18d9b77e2ad6e.jpg")

        await ctx.send(embed = embed)

    @commands.command(aliases = ['s', 'subreddit'])
    async def sub(self, ctx, color=''):
        """
        : links the subreddit for the specified color
        """
        color = color.lower();

        if color == 'red' or color == 'r':
            embed=discord.Embed(title="https://www.reddit.com/r/DSRRed/", url="https://www.reddit.com/r/DSRRed/", color=discord.Color.red())
            embed.set_author(name="DSRRed")
            embed.set_thumbnail(url="https://cdn.discordapp.com/emojis/600807579551137893.png?v=1")

        elif color == 'orange' or color == 'o':
            embed=discord.Embed(title="https://www.reddit.com/r/EternalOrange/", url="https://www.reddit.com/r/EternalOrange/", color=discord.Color.orange())
            embed.set_author(name="EternalOrange")
            embed.set_thumbnail(url="https://cdn.discordapp.com/emojis/615704227146235942.png?v=1")

        elif color == 'yellow' or color == 'y':
            embed=discord.Embed(title="https://www.reddit.com/r/YellowOnlineUnion/", url="https://www.reddit.com/r/YellowOnlineUnion/", color=discord.Color.gold())
            embed.set_author(name="Yellow Online Union")
            embed.set_thumbnail(url="https://cdn.discordapp.com/emojis/600807913740566619.png?v=1")

        elif color == 'blue' or color == 'b':
            embed=discord.Embed(title="https://www.reddit.com/r/AzureEmpire/", url="https://www.reddit.com/r/AzureEmpire/", color=discord.Color.blue())
            embed.set_author(name="Azure Empire")
            embed.set_thumbnail(url="https://cdn.discordapp.com/emojis/697546980519575573.png?v=1")

        elif color == 'purple' or color == 'p':
            embed=discord.Embed(title="https://www.reddit.com/r/PurpleImperium/", url="https://www.reddit.com/r/PurpleImperium/", color=discord.Color.purple())
            embed.set_author(name="Purple Imperium")
            embed.set_thumbnail(url="https://cdn.discordapp.com/emojis/600807913044443147.png?v=1")

        elif color == 'green' or color == 'g' or color == '':
            embed=discord.Embed(title="https://www.reddit.com/r/TheGreenArmy/", url="https://www.reddit.com/r/TheGreenArmy/", color=discord.Color.green())
            embed.set_author(name="The Green Army")
            embed.set_thumbnail(url="https://cdn.discordapp.com/emojis/600807577755844628.png?v=1")

        else:
            ctx.send('You did not give me a valid sub to look up :()')
            return

        await ctx.send(embed=embed)
    
    @commands.command()
    async def pfp(self, ctx, *, member:discord.Member = None):
        '''
        : Gets your/members pfp
        '''
        if member==None:
            url = ctx.author.avatar_url
            print(url)
        else:
            url = member.avatar_url
        
        embed = discord.Embed(color=discord.Color.green())
        embed.set_image(url=url)

        await ctx.send(embed=embed)

    @pfp.error
    async def pfp_error(self, ctx, error):
        if isinstance(error, commands.errors.MemberNotFound):
            await ctx.send('`ERROR: member not found`')
        else:
            print(error)

def setup(client):
    client.add_cog(misc(client))
