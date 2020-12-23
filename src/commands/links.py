import discord
from discord.ext import commands

class links(commands.Cog, name='Making it easier to link since 2020'):
    '''
    Links for everything you might need
    '''
    def __init__(self, client):
        self.client = client


    @commands.command(aliases = ['megainvite', 'megainv', 'megaInv'])
    async def megaInvite(self, ctx):
        """
        : provides a link to the megaserver
        """
        embed=discord.Embed(title="https://discord.com/invite/f647g7Z", url="https://discord.com/invite/f647g7Z", color=discord.Color.green())
        embed.set_author(name="Flairwars Megaserver")
        embed.set_thumbnail(url="https://cdn.discordapp.com/icons/463794005231271976/a_dad8b99b5351a2c8eaf18d9b77e2ad6e.jpg")



    @commands.command(aliases = ['s', 'subreddit'])
    async def sub(self, ctx, color):
        """
        : links the subreddit for the specified color
        """
        color = color.lower();

        if color = 'red' or color = 'r':
            embed=discord.Embed(title="https://www.reddit.com/r/DSRRed/", url="https://www.reddit.com/r/DSRRed/", color=discord.Color.red())
            embed.set_author(name="DSRRed")
            embed.set_thumbnail(url="https://cdn.discordapp.com/emojis/600807579551137893.png?v=1")
        elif color = 'orange' or color = 'o':
            embed=discord.Embed(title="https://www.reddit.com/r/EternalOrange/", url="https://www.reddit.com/r/EternalOrange/", color=discord.Color.orange())
            embed.set_author(name="EternalOrange")
            embed.set_thumbnail(url="https://cdn.discordapp.com/emojis/615704227146235942.png?v=1")
        elif color = 'yellow' or color = 'y':
            embed=discord.Embed(title="https://www.reddit.com/r/YellowOnlineUnion/", url="https://www.reddit.com/r/YellowOnlineUnion/", color=discord.Color.yellow())
            embed.set_author(name="Yellow Online Union")
            embed.set_thumbnail(url="https://cdn.discordapp.com/emojis/600807913740566619.png?v=1")
        elif color = 'green' or color = 'g':
            embed=discord.Embed(title="https://www.reddit.com/r/TheGreenArmy/", url="https://www.reddit.com/r/TheGreenArmy/", color=discord.Color.green())
            embed.set_author(name="The Green Army")
            embed.set_thumbnail(url="https://cdn.discordapp.com/emojis/600807577755844628.png?v=1")
        elif color = 'blue' or color = 'b':
            embed=discord.Embed(title="https://www.reddit.com/r/AzureEmpire/", url="https://www.reddit.com/r/AzureEmpire/", color=discord.Color.blue())
            embed.set_author(name="Azure Empire")
            embed.set_thumbnail(url="https://cdn.discordapp.com/emojis/697546980519575573.png?v=1")
        elif color = 'purple' or color = 'p':
            embed=discord.Embed(title="https://www.reddit.com/r/PurpleImperium/", url="https://www.reddit.com/r/PurpleImperium/", color=discord.Color.purple())
            embed.set_author(name="Purple Imperium")
            embed.set_thumbnail(url="https://cdn.discordapp.com/emojis/600807913044443147.png?v=1")
        else:
            ctx.send('You did not give me a valid sub to look up :()')
            return

        await ctx.send(embed=embed)


def setup(client):
    client.add_cog(links(client))
