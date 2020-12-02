import discord
from discord.ext import commands, tasks
from sql_connection import sql_class

class persistant_role(commands.Cog, name='Persistant Roles'):
    """
    comands and functions for the persistant roles
    """
    def __init__(self, client):
        self.client = client
        self.server_id = 780836834635677708 # this is the server id of the current server that it is running on
        #self.update_database.start()

    @tasks.loop(minutes=30)
    async def update_database(self):
        '''
        automatically updates the sql server with members and new roles
        '''
        sql = sql_class()
        guild = self.client.get_guild(self.server_id)

        # update list of roles
        roleList = guild.roles

        for role in roleList:
            role_name = sql.get_role(str(role.id))

            if role_name == None:
                sql.add_role(str(role.id) , role.name)
            elif role_name != role.name:
                sql.update_role_name(str(role.id), role.name)

        # update list of users
        memberList = guild.members
        for member in memberList:

            user_name = sql.get_user(str(member.id))

            if user_name == None:
                sql.add_user(str(member.id) , member.name)
            elif user_name != member.name:
                sql.update_user_name(str(member.id), member.name)
        
            # update user_role table
            


    @commands.Cog.listener()
    async def on_member_join(self, member):
        '''
        adds all the stored roles to a member when they join
        '''
        print(f'{member} has joined the server')

    @commands.command()
    async def test(self, ctx):
        '''
        : testing command
        '''
        sql = sql_class()

        guild = self.client.get_guild(self.server_id)
        
        memberList = guild.members
        for member in memberList:
            member_roleList = member.roles

            member_roles = sql.get_user_role(str(member.id))
            for role in member_roleList:
                found_role = False

                for db_role in member_roles:
                    if str(role) == db_role:
                        found_role = True
                
                if found_role == False:
                    sql.add_user_role(str(member),str(role))



def setup(client):
    client.add_cog(persistant_role(client))