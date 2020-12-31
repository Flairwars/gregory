import pathlib
import re
import discord
import datetime
from asyncio import sleep
from discord.ext import commands
from converter.datetimeCalc import datetimeCal
from sql.poll import sql_class
from apscheduler.schedulers.asyncio import AsyncIOScheduler

class poll(commands.Cog, name='poll'):
    """
    Too Much Poll
    """
    def __init__(self, client):
        self.client = client
        self.category = pathlib.Path(__file__).parent.absolute().name[4:]
        self.pollsigns = ["🇦","🇧","🇨","🇩","🇪","🇫","🇬","🇭","🇮","🇯","🇰","🇱","🇲","🇳","🇴","🇵","🇶","🇷","🇸","🇹","🇺","🇻","🇼","🇽","🇾","🇿"]
        self.reg = re.compile('({.+})\ *(\[[^\n\r\[\]]+\] *)+')
        self.sched = AsyncIOScheduler()
        self.sched.start()

        client.loop.create_task(self.async_init())
 
    async def async_init(self):
        """
        this loads up all the command on a timer
        """
        await self.client.wait_until_ready()

        sql = sql_class()
        polls = sql.get_polls()
        now = datetime.datetime.now()
        for poll in polls:
            poll_id = str(poll[0])
            poll_datetime = poll[1]
            if not poll_datetime:
                # if the poll has no end time, it does nothing
                pass
            elif poll_datetime > now:
                # if the poll hasnt passed, it adds it to the schedule
                self.sched.add_job(self._poll2_end, 'date', run_date=poll_datetime, args=[poll_id],id=poll_id)
            else:
                # the poll has passed. it ends the poll
                await self._poll2_end(poll_id)
             
    async def _poll2_end(self, poll_id):
        """
        ends
        """
        sql = sql_class()
        poll_info, votes = sql.get_poll_info(str(poll_id))

        description = ''
        if len(votes) == 0:
            description = 'no one voted :/'
        else:
            dict = {}
            for elem in votes:
                if elem[1] in dict.keys():
                    dict[elem[1]] += 1
                else:
                    dict[elem[1]] = 1
            
            for key,value in dict.items():
                description+=f'{value}'
                if value == 1:
                    description +=f' vote for {key} \n\n'
                else:
                    description +=f' votes for {key} \n\n'
        
        sql.remove_poll(poll_id)

        embed = discord.Embed(title=poll_info[1],color=discord.Color.green(),description=description)
        channel = self.client.get_channel(int(poll_info[0]))
        await channel.send(embed=embed)

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        """
        toggles the voting option for this poll
        """
        if payload.member == self.client.user:
            return
        
        message_id = str(payload.message_id)
        channel_id = str(payload.channel_id)
        guild_id = str(payload.guild_id)
        user_id = str(payload.user_id)
        
        if payload.emoji.name not in self.pollsigns:
            return

        # if it has an id, its not one of the abcdef emotes
        if payload.emoji.name in self.pollsigns:
            emote_id = str(ord(payload.emoji.name))
            sql = sql_class()
            toggle = sql.toggle_vote(message_id, channel_id, guild_id, emote_id, user_id)


        channel = self.client.get_channel(payload.channel_id)
        message = await channel.fetch_message(payload.message_id)
        await message.remove_reaction(payload.emoji, payload.member)

    @commands.command(aliases=['poll2electricboogaloo','pollv2'])
    @commands.has_permissions(administrator=True) 
    async def poll2(self, ctx, *, args):
        """
        Fancy poll. Admin only
        """
        time = None
        # checks message against regex to see if it matches
        if not self.reg.match(args):
            # check if it has time at start of command
            # splits arguments and datetime
            index = args.find(' ')
            time = args[:index]
            args = args[index:].lstrip()

            # converts to datetime
            calc = datetimeCal()
            time = await calc.convert(ctx, time)

            # checks if the args are formatted correctly
            if not self.reg.match(args):
                raise discord.errors.DiscordException

        # have args and possible datetime
        # fomatting of arguments in message
        args = args.split('[')
        name = args.pop(0)[1:]
        name = name[:name.find('}')]
        
        args = [arg[:arg.find(']')] for arg in args] # thanks ritz for this line

        if len(args) > 20:
            await ctx.send(f"bad {ctx.author.name}! thats too much polling >:(")
            return
        elif len(args) == 0:
            await ctx.send(f"bad {ctx.author.name}! thats too little polling >:(")
            return
        elif name == '' or '' in args:
            await ctx.send(f"bad {ctx.author.name}! thats too simplistic polling >:(")
            return

        # creating embed for poll
        description = ''
        for count in range(len(args)):
            description += f'{self.pollsigns[count]} {args[count]}\n\n'

        if time:
            strtime = time.strftime("%m/%d/%Y, %H:%M:%S")
            description += f'ends on `{strtime}`\n'
        
        embed = discord.Embed(title=name,color=discord.Color.green(),description=description)
        message = await ctx.send(embed=embed)

        # adds a message id to the end of the poll
        description += f'id: *`{message.id}`*'
        embed = discord.Embed(title=name,color=discord.Color.green(),description=description)
        await message.edit(embed=embed)
        
        #add reactions
        for count in range(len(args)):
            await message.add_reaction(self.pollsigns[count])

        sql = sql_class()
        self._update_guilds()

        poll_id = sql.add_poll(str(message.id), str(message.channel.id), str(message.author.guild.id), name, time, self.pollsigns, args)
        if time:
            self.sched.add_job(self._poll2_end, 'date', run_date=time, args=[poll_id],id=poll_id)
        
    @commands.command(aliases=['checkvotes'])
    async def check_votes(self, ctx):
        """
        allows the user to check who they voted for
        """
        sql = sql_class()
        polls = sql.check_polls(str(ctx.author.id))
        # removes duplicate polls from data
        polls = list(dict.fromkeys(polls))
        await ctx.message.delete()
        
        if len(polls) == 0:
            msg = await ctx.send('You havent voted on any active polls')
            await sleep(10)
            await msg.delete()
        else:
            for poll in polls:
                votes = sql.check_votes(str(ctx.author.id), poll[0])

                description = 'You have voted: \n\n'
                for vote in votes:
                    description += vote[0] + '\n'
                embed = discord.Embed(title=f'on poll: {votes[0][1]}',color=discord.Color.green(),description=description)
                await ctx.author.send(embed=embed)
    
    
    @commands.command(aliases=['endpoll', 'stoppoll','stopoll','stop_poll'])
    @commands.has_permissions(administrator=True) 
    async def end_poll(self, ctx, message_id, dm=False):
        """
        manually ends a poll. optionally can make it output to channel or dms
        """
        channel_id = str(ctx.channel.id)
        guild_id = str(ctx.guild.id)
        sql = sql_class()
        poll_info = sql.location_get_poll(message_id, channel_id, guild_id)

        if not poll_info:
            await ctx.send('`no poll detected please check you are running it in the same channel as the poll`')
            return
        else:
            poll_info = poll_info[0]

        poll_id = str(poll_info[0])
        poll_date = poll_info[1]

        if poll_date:
            self.sched.remove_job(poll_id)
        
        poll_info, votes = sql.get_poll_info(poll_id)

        description = ''
        if len(votes) == 0:
            description = 'no one voted :/'
        else:
            dict = {}
            for elem in votes:
                if elem[1] in dict.keys():
                    dict[elem[1]] += 1
                else:
                    dict[elem[1]] = 1
            
            for key,value in dict.items():
                description+=f'{value}'
                if value == 1:
                    description +=f' votes for {key} \n\n'
                else:
                    description +=f' votes for {key} \n\n'
        
        sql.remove_poll(poll_id)
        embed = discord.Embed(title=poll_info[1],color=discord.Color.green(),description=description)
        
        if dm == True:
            await ctx.send(embed=embed)
        else:
            await ctx.author.send(embed=embed)

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
    
    @commands.command(aliases=['deletepoll','remove_poll', 'removepoll'])
    @commands.has_permissions(administrator=True) 
    async def delete_poll(self, ctx, message_id):
        """
        deletes poll
        """
        channel_id = str(ctx.channel.id)
        guild_id = str(ctx.guild.id)
        sql = sql_class()
        poll_info = sql.location_get_poll(message_id, channel_id, guild_id)

        if not poll_info:
            await ctx.send('`no poll detected please check you are running it in the same channel as the poll`')
            return
        else:
            poll_info = poll_info[0]

        poll_id = str(poll_info[0])
        poll_date = poll_info[1]

        if poll_date:
            self.sched.remove_job(poll_id)
        
        sql.remove_poll(poll_id)
        await ctx.send('deleted poll')

    @commands.command(aliases=['raidpoll','rp'])
    async def raid_poll(self, ctx, *,title='Raid Times'):
        """
        creates a poll for raiding
        """
        emotes = ["🇦","🇧","🇨","🇩","🇪","🇫","🇬","🇭","🇮","🇯","🇰"]
        description = """
        🇦 1:00\n
        🇧 2:00\n
        🇨 3:00\n
        🇩 4:00\n
        🇪 5:00\n
        🇫 6:00\n
        🇬 7:00\n
        🇭 8:00\n
        🇮 9:00\n
        🇯 10:00\n
        🇰 12:00\n
        """
        embed = discord.Embed(title=f'{title} AM',color=discord.Color.green(),description=description)
        msg = await ctx.send(embed=embed)
        embed = discord.Embed(title=f'{title} PM',color=discord.Color.green(),description=description)
        msg2 = await ctx.send(embed=embed)

        for emote in emotes:
            await msg.add_reaction(emote)
            await msg2.add_reaction(emote)

    @commands.command()
    async def poll(self, ctx, *, args):
        """
        normal poll
        """
        if not self.reg.match(args):
            await ctx.message.add_reaction('👍')
            await ctx.message.add_reaction('👎')
            await ctx.message.add_reaction('🤷‍♀️')
            return

        args = args.split('[')
        name = args.pop(0)[1:]
        name = name[:name.find('}')]
        
        args = [arg[:arg.find(']')] for arg in args] # thanks ritz for this line

        if len(args) > 20:
            await ctx.send(f"bad {ctx.author.name}! thats too much polling >:(")
            return
        elif len(args) == 0:
            await ctx.send(f"bad {ctx.author.name}! thats too little polling >:(")
            return
        elif name == '' or '' in args:
            await ctx.send(f"bad {ctx.author.name}! thats too simplistic polling >:(")
            return
        
        description = ''
        for count in range(len(args)):
            description += f'{self.pollsigns[count]} {args[count]}\n\n'

        embed = discord.Embed(title=name,color=discord.Color.green(),description=description)
        msg = await ctx.send(embed=embed)

        #add reactions
        for count in range(len(args)):
            await msg.add_reaction(self.pollsigns[count])
        
    @poll2.error
    async def poll2_error(self, ctx, error):
        if isinstance(error, commands.errors.MissingRequiredArgument) or isinstance(error, discord.errors.DiscordException):
            await ctx.send('`ERROR Missing Required Argument: make sure it is .poll2 <time ddhhmmss> {title} [args]`')
        else:
            print(error)
    
    @poll.error
    async def poll2_error(self, ctx, error):
        if isinstance(error, commands.errors.MissingRequiredArgument):
            await ctx.send('`ERROR Missing Required Argument: make sure it is .poll {title} [args]`')
        else:
            print(error)
    
    @check_votes.error
    async def check_votes_error(self, ctx, error):
        if isinstance(error, commands.errors.MissingRequiredArgument) or isinstance(error, discord.errors.DiscordException):
            await ctx.send('`ERROR Missing Required Argument: make sure it is .checkvotes`')
        else:
            print(error)
    
    @end_poll.error
    async def end_poll_error(self, ctx, error):
        if isinstance(error, commands.errors.MissingRequiredArgument) or isinstance(error, discord.errors.DiscordException):
            await ctx.send('`ERROR Missing Required Argument: make sure it is .deletepoll <message id> (True if it should output to channel)`')
        else:
            print(error)

    @delete_poll.error
    async def delete_poll_error(self, ctx, error):
        if isinstance(error, commands.errors.MissingRequiredArgument) or isinstance(error, discord.errors.DiscordException):
            await ctx.send('`ERROR Missing Required Argument: make sure it is .deletepoll <message id>`')
        else:
            print(error)

def setup(client):
    client.add_cog(poll(client))
