import discord
from discord.ext import commands, tasks
from sql.roles import sql_class
import asyncio

class persistant_role(commands.Cog, name='Persistant Roles'):
    """
    comands and functions for the persistant roles
    """
    def __init__(self, client):
        self.client = client
        self.server_id = 780836834635677708 # this is the server id of the current server that it is running on

    @commands.Cog.listener()
    async def on_member_join(self, member):
        pass
        '''
        for db_memberroleid in db_memberroles:

        found = False
        for memberrole in memberroles:
            memberroleid = str(memberrole.id)

            if memberroleid == db_memberroleid:
                found = True
        
        if found == False:
            sql.delete_user_role(memberid,db_memberroleid)
        '''
        sql = sql_class()

        guild = self.client.get_guild(self.server_id)
        self._update_roles(guild)

        memberId = str(member.id)
        memberName = member.name


    @commands.Cog.listener()
    async def on_member_remove(self, member):
        sql = sql_class()

        guild = self.client.get_guild(self.server_id)
        self._update_roles(guild)

        memberId = str(member.id)
        memberName = member.name

        sql.add_user(memberId, memberName)

        memberRoles = member.roles
        for memberRole in memberRoles:
                memberRoleId = str(memberRole.id)
                sql.add_user_role(memberId,memberRoleId)


    def _update_roles(self, guild):
        sql = sql_class()
        db_roles = sql.get_roles()

        for role in guild.roles:
            roleId = str(role.id)
            roleName = role.name

            found = False
            for db_role in db_roles:
                db_roleId = db_role[0]
                db_roleName = db_role[1]

                if roleId == db_roleId:
                    found = True
                    if db_roleName != roleName:
                        sql.update_role_name(db_roleId, roleName)
                
            if found == False:
                sql.add_role(roleId, roleName)
        

        # searching for old roles that are deleted
        for db_role in db_roles:
            db_roleId = db_role[0]
            db_roleName = db_role[1]

            found = False
            for role in guild.roles:
                roleId = str(role.id)
                roleName = role.name
                
                if roleId == db_roleId:
                    found = True
                
            if found == False:
                sql.remove_role(db_roleId)


    @commands.command()
    async def test(self, ctx):


        #adds roles to member
        member = ctx.message.author #temp till i transfer to member join
        member_roleList = sql.get_user_role(str(member.id))

        await self.client.add_roles(member, member_roleList)


def setup(client):
    client.add_cog(persistant_role(client))