from discord.errors import DiscordException
from discord.ext import commands
from discord.utils import get
import discord
from sql.roles import sql_class

class persistant_role(commands.Cog, name='Persistant Roles'):
    """
    comands and functions for the persistant roles
    """
    def __init__(self, client):
        self.client = client
        self.server_id = 784750381694713908 # this is the server id of the current server that it is running on

    @commands.command(aliases=['addroles'])
    @commands.has_role("Verdancy")
    async def add_roles(self, ctx, member:discord.Member):
        sql = sql_class()

        self._update_guilds()
        self._update_roles(member)

        memberId = str(member.id)
        memberGuildId = str(member.guild.id)
        memberRoles = sql.get_user_role(memberId, memberGuildId)

        if len(memberRoles) < 1:
            await ctx.send(f'{member.name} has no roles in my datatable')
            return
        
        #gets a list of role classes
        roles = [] 
        for memberRole in memberRoles:
            role = get(member.guild.roles, id=int(memberRole))
            roles.append(role)
        
        # adds roles
        try:
            await member.add_roles(*roles, reason="Automatically added roles")
        except DiscordException as e:
            print(e)
        
        sql.remove_user_roles(memberId, memberGuildId)
        await ctx.send(f'updated {member.id}`s roles`')

    @add_roles.error
    async def add_roles_error(self, ctx, error):
        if isinstance(error, commands.errors.MissingRequiredArgument):
            await ctx.send('`MISSING ARGUMENTS: please specify a user`')
        else:
            print(error)


    @commands.Cog.listener()
    async def on_member_remove(self, member):
        sql = sql_class()

        self._update_guilds()
        self._update_roles(member)

        memberId = str(member.id)
        memberName = member.name
        memberGuildId = str(member.guild.id)

        sql.remove_user_roles(memberId, memberGuildId)

        exists = sql.get_user(memberId, memberGuildId)
        if exists == None:
            sql.add_user(memberId, memberName, memberGuildId)

        memberRoles = member.roles
        for memberRole in memberRoles:
                memberRoleId = str(memberRole.id)
                memberRoleName = memberRole.name
                if memberRoleName != "@everyone":
                    sql.add_user_role(memberId, memberRoleId, memberGuildId)


    def _update_roles(self, member):
        sql = sql_class()
        db_roles = sql.get_roles()

        guildRoles = member.guild.roles
        guildId = str(member.guild.id)

        for role in guildRoles:
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
                sql.add_role(roleId, roleName, guildId)
        

        # searching for old roles that are deleted
        for db_role in db_roles:
            db_roleId = db_role[0]
            db_roleName = db_role[1]

            found = False
            for role in guildRoles:
                roleId = str(role.id)
                roleName = role.name
                
                if roleId == db_roleId:
                    found = True
                
            if found == False:
                sql.remove_role(db_roleId, guildId)

    def _update_guilds(self):
        sql = sql_class()

        guilds = self.client.guilds
        db_guilds = sql.get_guilds()


        for guild in guilds:
            guildId = str(guild.id)
            guildName = guild.name

            found = False
            for db_guild in db_guilds:
                db_guildId = db_guild[0]
                db_guildName = db_guild[1]
                if guildId == db_guildId:
                    #print(db_roleId, roleName)
                    found = True
                    if db_guildName != guildName:
                        sql.update_guild_name(db_guildId, guildName)
                
            if found == False:
                sql.add_guild(guildId, guildName)
        

        # searching for old roles that are deleted
        for db_guild in db_guilds:
            db_guildId = db_guild[0]
            db_guildName = db_guild[1]

            found = False
            for guild in guilds:
                guildId = str(guild.id)
                guildName = guild.name
                
                if guildId == db_guildId:
                    found = True
                
            if found == False:
                sql.remove_role(db_guildId)



def setup(client):
    client.add_cog(persistant_role(client))
