import discord
from discord.ext import commands, tasks
from sql_connection import sql_class
import asyncio

class persistant_role(commands.Cog, name='Persistant Roles'):
    """
    comands and functions for the persistant roles
    """
    def __init__(self, client):
        self.client = client
        self.server_id = 780836834635677708 # this is the server id of the current server that it is running on
        self.update_database.start()

    @tasks.loop(minutes=30)
    async def update_database(self):
        '''
        automatically updates the sql server with members and new roles
        '''
        #sleep so bot can fully finish setting up and connecting to servers
        await asyncio.sleep(1)

        
        sql = sql_class()# initalise sql class 
        guild = self.client.get_guild(self.server_id)# getting guild class from discord servers

        for role in guild.roles:# loops for the number of roles on the discord server
            role_name = sql.get_role(str(role.id))# makes a request to the server seeing if it exists

            if role_name == None:# if it doesnt exist, it addes it
                sql.add_role(str(role.id) , role.name)
            elif role_name != role.name:# if the roles has changed name, it updates the name
                sql.update_role_name(str(role.id), role.name)

        # update list of users
        for member in guild.members:# loops for the number of users on the discord server

            user_name = sql.get_user(str(member.id))# makes a request to the server seeing if it exists

            if user_name == None:# if it doesnt exist, it adds it
                sql.add_user(str(member.id) , member.name)
            elif user_name != member.name:# if the user has changed name, it updates the name
                sql.update_user_name(str(member.id), member.name)
        
            # update user_role table
            
            member_roleList = member.roles # [role.id, role.id] # gets a list of all the members roles from discord
            member_roles = sql.get_user_role(str(member.id)) # [id, id] # gets a list of all the members roles from the sql server 

            for role in member_roleList: # loops though all the roles on the discord server
                role = str(role.id)
                found_role = False

                for db_role in member_roles: # loops though all the known roles on the sql server
                    db_role = db_role[0]

                    if role == db_role: # if it finds the role, it notes it
                        found_role = True

                if found_role == False:# updates the role if it hasnt found the role
                    sql.add_user_role(str(member.id),role)
        

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
        pass

            



def setup(client):
    client.add_cog(persistant_role(client))