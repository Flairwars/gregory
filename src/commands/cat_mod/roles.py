import pathlib

from discord.errors import DiscordException
from discord.ext import commands
from discord.utils import get
import discord
from sql.roles import sql_class

class roles(commands.Cog, name='roles'):
    """
    comands and functions for the persistant roles
    """
    def __init__(self, client):
        self.client = client
        self.category = pathlib.Path(__file__).parent.absolute().name[4:]

    @commands.command(aliases=['removeroles','clearroles','purgeroles'])
    async def remove_roles(self, ctx):
        '''
        : remove roles from datatable
        '''
        sql = sql_class()
        message = await ctx.send(f"`purging {ctx.author.name}'s roles from datatables...`")
        sql.remove_user_roles(str(ctx.author.id), str(ctx.guild.id))
        await message.edit(content=f"`purged {ctx.author.name}'s roles from datatables!`")

    @commands.command(aliases=['addroles'])
    @commands.has_permissions(administrator=True)
    async def add_roles(self, ctx, member:discord.Member):
        """
        : command which adds roles from when someone last joined the server
        """
        sql = sql_class()

        self._update_guilds()
        self._update_roles(member)

        memberId = str(member.id)
        memberGuildId = str(member.guild.id)
        memberRoles = sql.get_user_role(memberId, memberGuildId)

        if len(memberRoles) < 1:
            await ctx.send(f'`{member.name} has no roles in my datatable`')
            return
        

        message = await ctx.send(f"`adding {member.name}'s roles...`")
        
        #gets a list of role classes
        roles = [] 
        for memberRole in memberRoles:
            role = get(member.guild.roles, id=int(memberRole[0]))
            roles.append(role)
        
        # adds roles
        try:
            await member.add_roles(*roles, reason="Automatically added roles")
        except DiscordException as e:
            print(e)
        
        sql.remove_user_roles(memberId, memberGuildId)
        await message.edit(content=f"`updated {member.name}'s roles!`")


    @add_roles.error
    async def add_roles_error(self, ctx, error):
        if isinstance(error, commands.errors.MissingRequiredArgument):
            await ctx.send('`MISSING ARGUMENTS: please specify a user`')
        elif isinstance(error, commands.errors.MissingPermissions):
            await ctx.send('`MISSING PERMS: you need to be an administrator to run this command`')
        else:
            print(error)


    @commands.Cog.listener()
    async def on_member_remove(self, member):
        """
        adds member's roles to database when they leave
        """
        sql = sql_class()

        # updates guilds and members
        self._update_guilds()
        self._update_roles(member)

        memberId = str(member.id)
        memberGuildId = str(member.guild.id)

        sql.remove_user_roles(memberId, memberGuildId)
        exists = sql.get_user(memberId, memberGuildId)

        if exists == None:
            sql.add_user(memberId, memberGuildId)

        memberRoles = member.roles
        for memberRole in memberRoles:
                memberRoleId = str(memberRole.id)
                memberRoleName = memberRole.name
                if memberRoleName != "@everyone":
                    sql.add_user_role(memberId, memberRoleId, memberGuildId)


    def _update_roles(self, member):
        sql = sql_class()

        guildRoles = member.guild.roles
        guildId = str(member.guild.id)

        db_roles = sql.get_roles(guildId)

        for role in guildRoles:
            roleId = str(role.id)
            roleName = role.name

            found = False
            for db_role in db_roles:
                if roleId == db_role[0]:
                    #print(db_roleId, roleName)
                    found = True
                
            if found == False and roleName !="@everyone":
                sql.add_role(roleId, guildId)
        

        # searching for old roles that are deleted
        for db_role in db_roles:
            db_roleId = db_role[0]

            found = False
            for role in guildRoles:
                roleId = str(role.id)

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
            found = False
            for db_guild in db_guilds:
                db_guildId = db_guild[0]
                if guildId == db_guildId:
                    #print(db_roleId, roleName)
                    found = True
                
            if found == False:
                sql.add_guild(guildId)
        
        # searching for old guilds that are deleted
        for db_guild in db_guilds:
            db_guildId = db_guild[0]

            found = False
            for guild in guilds:
                guildId = str(guild.id)
                
                if guildId == db_guildId:
                    found = True
                
            if found == False:
                sql.remove_guild(db_guildId)

def setup(client):
    client.add_cog(roles(client))
