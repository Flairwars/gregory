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
        #self.update_database.start()

    @tasks.loop(minutes=30)
    async def update_database(self):
        '''
        automatically updates the sql server with members and new roles
        '''
        #sleep so bot can fully finish setting up and connecting to servers
        await asyncio.sleep(1)

        
        sql = sql_class()
        guild = self.client.get_guild(self.server_id)

        # checks for new roles and updates their names in the db
        for role in guild.roles:
            roleid = str(role.id)
            rolename = role.name

            db_rolename = sql.get_role(roleid)

            if db_rolename == None:
                sql.add_role(roleid , rolename)
            elif db_rolename != role.name:
                sql.update_role_name(str(role.id), role.name)

        # checks for new members and updates their names in the db
        for member in guild.members:
            memberid = str(member.id)
            membername = member.name

            db_membername = sql.get_user(memberid)

            if db_membername == None:
                sql.add_user(memberid , membername)
            elif db_membername != membername:# if the user has changed name, it updates the name
                sql.update_user_name(memberid, membername)
        
            # checks for different roles in user_role table
            
            memberroles = member.roles 
            db_memberroles = sql.get_user_role(memberid) 

            # checks for new roles to be added
            for memberrole in memberroles:
                memberroleid = str(memberrole.id)

                found = False
                for db_memberroleid in db_memberroles: 

                    if memberroleid == db_memberroleid:
                        found = True

                if found == False:
                    sql.add_user_role(memberid,memberroleid)

            #checks for old roles to be deleted
            for db_memberroleid in db_memberroles:

                found = False
                for memberrole in memberroles:
                    memberroleid = str(memberrole.id)

                    if memberroleid == db_memberroleid:
                        found = True
                
                if found == False:
                    sql.delete_user_role(memberid,db_memberroleid)


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

        db_roles = sql.get_roles()

        
        # searching for new roles that have been added
        for role in guild.roles:
            roleid = str(role.id)
            rolename = role.name

            found = False
            for db_role in db_roles:
                db_roleid = db_role[0]
                db_rolename = db_role[1]

                if roleid == db_roleid:
                    found = True
                    if db_rolename != rolename:
                        sql.update_role_name(db_roleid, rolename)
                
            if found == False:
                sql.add_role(roleid, rolename)
        

        # searching for old roles that are deleted
        for db_role in db_roles:
            db_roleid = db_role[0]
            db_rolename = db_role[1]

            found = False
            for role in guild.roles:
                roleid = str(role.id)
                rolename = role.name
                
                if roleid == db_roleid:
                    found = True
                
            if found == False:
                sql.remove_role(db_roleid)


        #adds roles to member
        member = ctx.message.author #temp till i transfer to member join
        member_roleList = sql.get_user_role(str(member.id))

        await self.client.add_roles(member, member_roleList)



def setup(client):
    client.add_cog(persistant_role(client))