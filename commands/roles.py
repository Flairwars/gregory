import discord
from discord.errors import DiscordException
from discord.ext import commands
from discord.utils import get
from sql.roles import sql_class

class persistant_role(commands.Cog, name='Persistant Roles'):
    """
    comands and functions for the persistant roles
    """
    def __init__(self, client):
        self.client = client
        self.server_id = 780836834635677708 # this is the server id of the current server that it is running on

    @commands.Cog.listener()
    async def on_member_join(self, member):
        sql = sql_class()

        guild = self.client.get_guild(self.server_id)
        self._update_roles(guild)

        memberId = str(member.id)
        memberRoles = sql.get_user_role(memberId)

        #gets a list of role classes
        roles = [] 
        for memberRole in memberRoles:
            role = get(guild.roles, id=int(memberRole))
            roles.append(role)
        
        # adds roles
        try:
            await member.add_roles(*roles, reason="Automatically added roles")
        except DiscordException:
            pass
        
        sql.remove_user_roles(memberId)

    @commands.Cog.listener()
    async def on_member_remove(self, member):
        sql = sql_class()

        guild = self.client.get_guild(self.server_id)
        self._update_roles(guild)

        memberId = str(member.id)
        memberName = member.name

        exists = sql.get_user(memberId)
        if exists == None:
            sql.add_user(memberId, memberName)

        memberRoles = member.roles
        for memberRole in memberRoles:
                memberRoleId = str(memberRole.id)
                memberRoleName = memberRole.name
                if memberRoleName != "@everyone":
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
                    #print(db_roleId, roleName)
                    found = True
                    if db_roleName != roleName:
                        sql.update_role_name(db_roleId, roleName)
                
            if found == False and roleName !="@everyone":
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


def setup(client):
    client.add_cog(persistant_role(client))