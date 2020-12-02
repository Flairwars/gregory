import discord
from discord.ext import commands, tasks
from sql_connection import sql_class

class persistant_role(commands.Cog):
    """
    comands and functions for the persistant roles
    """
    def __init__(self, client):
        self.client = client
        self.server_id = 780836834635677708 # this is the server id of the current server that it is running on
        #self.update_database.start()

    @tasks.loop(minutes=30)
    async def update_database(self):
        # update list of roles
        

        # update list of users
        guild = self.client.get_guild(self.server_id)
        memberList = guild.members
        for member in memberList:
            print(member.id, member.name)
            #member.id member.name
        
        # update user_role table
        

    @commands.Cog.listener()
    async def on_member_join(self, member):
        print(f'{member} has joined the server')

    @commands.command()
    async def test(self, ctx):
        sql = sql_class()
        #lst = discord.Guild.members
        #print(lst, type(lst))
        guild = self.client.get_guild(780836834635677708)
        memberList = guild.members
        for member in memberList:
            sql.add_user(int(member.id) , member.name)
            

def setup(client):
    client.add_cog(persistant_role(client))