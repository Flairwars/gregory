'''
Lets new greenies through the tutorial and pings welcome wagon when they join the server.
'''

from discord.ext import commands
import discord


# These are ID's from my test server but I'm still setting up all the libraries
# and stuff on my laptop and haven't had a chance to test this code yet -Excel
NEW_GREEN_ID = 872601525460017152
GREENIE_ID = 872617475810943056

GREEN_SERVER_ID = 259293507955589121

class newGreenie(commands.Cog, name='new greenie'):
    '''
    
    '''

    def __init__(self, client):
        self.client = client

    @commands.command(alias = ['tut'])
    async def tutorial(self, ctx, greenie: discord.Member = None):
        '''
        Give new greens access to the tutorial by giving them the "New Green".'''

        # If no user is supplied as a parameter, defaults to the user who used the command.
        if greenie == None:
            greenie == ctx.author

        # Ensures that the code only runs on the green server.
        guild = greenie.guild
        if guild.id != GREEN_SERVER_ID:
            return

        new_green_role = guild.get_role(NEW_GREEN_ID)
        # Checks if the user already has the new green role. If not, adds the role.
        if new_green_role in greenie.roles:
            await ctx.send('User already has the new green role!')
        else:
            greenie.add_roles(new_green_role)

        
        @commands.command()
        async def greenie(self, ctx, greenie: discord.Member = None):
            '''
            Remove the "New Green" role and give new greens the "Greenie" role.'''

            # If no user is supplied as a parameter, defaults to the user who used the command.
            if greenie == None:
                greenie == ctx.author

            # Ensures that the code only runs on the green server.
            guild = greenie.guild
            if guild.id != GREEN_SERVER_ID:
                return

            new_green_role = guild.get_role(NEW_GREEN_ID)
            greenie_role = guild.get_role(GREENIE_ID)
            # Checks if the user already has the new green role. If not, adds the role.
            if new_green_role in greenie.roles:
                greenie.remove_roles(new_green_role)
                await ctx.send('"New Green" role removed!')
            if not greenie_role in greenie.roles:
                greenie.add_roles(new_green_role)