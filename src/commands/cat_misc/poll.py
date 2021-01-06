import pathlib, re, discord, datetime
from asyncio import sleep
from discord.ext import commands
from converter.datetimeCalc import datetimeCal
from sql.poll import sql_class
from apscheduler.schedulers.asyncio import AsyncIOScheduler

class poll(commands.Cog, name='poll'):
    """
    Poll commands. all types
    """
    def __init__(self, client):
        #setup
        self.client = client
        self.category = pathlib.Path(__file__).parent.absolute().name[4:]
        self.sql = sql_class()

        # emotes
        self.pollsigns = ["🇦","🇧","🇨","🇩","🇪","🇫","🇬","🇭","🇮","🇯","🇰","🇱","🇲","🇳","🇴","🇵","🇶","🇷","🇸","🇹","🇺","🇻","🇼","🇽","🇾","🇿"]
        
        # regex for checking for complex poll
        self.reg = re.compile('({.+})\ *(\[[^\n\r\[\]]+\] *)+')

        # starts up the schedular and all the tasks for all commands on timer
        self.sched = AsyncIOScheduler()
        self.sched.start()

        client.loop.create_task(self._async_init())

        # caching of reacently accessed polls
        self.poll_locations = {} #contains {(message_id,channel_id,guild_id):poll_id}
 
    async def _async_init(self):
        """
        loads up all the tasks on a timer
        """
        await self.client.wait_until_ready()

        polls = self.sql.get_polls()
        now = datetime.datetime.now()
        for poll in polls:
            poll_id = str(poll[0])
            poll_datetime = poll[1]
            if not poll_datetime:
                # if the poll has no end time, it does nothing
                pass
            elif poll_datetime > now:
                # if the poll hasnt passed, it adds it to the schedule
                self.sched.add_job(self._end_poll, 'date', run_date=poll_datetime, args=[poll_id],id=poll_id)
            else:
                # the poll has passed. it ends the poll
                await self._end_poll(poll_id)
             
    async def _end_poll(self, poll_id):
        """
        code that executes when a timed poll finishes. sends poll results into channel where poll was made
        """
        poll_info, votes = self.sql.get_poll_info(str(poll_id))

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
        
        self.sql.remove_poll(poll_id)

        embed = discord.Embed(title=poll_info[1],color=discord.Color.green(),description=description)
        channel = self.client.get_channel(int(poll_info[0]))

        await channel.send(embed=embed)

    def _delete_poll(self, message_id, channel_id, guild_id):
        poll_id, poll_date = self.sql.location_get_poll(message_id, channel_id, guild_id)
        if poll_id:
            poll_id = str(poll_id)
            if poll_date:
                self.sched.remove_job(poll_id)
            self.sql.remove_poll(poll_id)
            return True
        else:
            return False
    
    def _update_guilds(self):
        guilds = self.client.guilds
        db_guilds = self.sql.get_guilds()

        for guild in guilds:
            guildId = str(guild.id)
            found = False
            for db_guild in db_guilds:
                db_guildId = db_guild[0]
                if guildId == db_guildId:
                    #print(db_roleId, roleName)
                    found = True
                
            if found == False:
                self.sql.add_guild(guildId)
        
        # searching for old guilds that are deleted
        for db_guild in db_guilds:
            db_guildId = db_guild[0]

            found = False
            for guild in guilds:
                guildId = str(guild.id)
                
                if guildId == db_guildId:
                    found = True
                
            if found == False:
                #self.sql.remove_guild(db_guildId)
                pass

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

        # checks whether is has reacent seen this poll
        if (message_id,channel_id,guild_id) in self.poll_locations.keys():
            poll_id = self.poll_locations[(message_id,channel_id,guild_id)]
        else:
            poll_id = self.sql.get_poll(message_id,channel_id,guild_id)
        
        if poll_id:
            self.poll_locations[(message_id,channel_id,guild_id)] = poll_id
            # if it has an id, its not one of the abcdef emotes
            if payload.emoji.name in self.pollsigns:# otherwise cant ord and crashes for custom emotes
                emote_id = str(ord(payload.emoji.name))
                self.sql.toggle_vote(poll_id,guild_id,emote_id,user_id)
            
            channel = self.client.get_channel(payload.channel_id)
            message = await channel.fetch_message(payload.message_id)

            await message.remove_reaction(payload.emoji, payload.member)

    @commands.Cog.listener()
    async def on_raw_message_delete(self, payload):
        if payload.cached_message.author == self.client.user:
            message_id = str(payload.message_id)
            channel_id = str(payload.channel_id)
            guild_id = str(payload.guild_id)

            self._delete_poll(message_id, channel_id, guild_id)

    @commands.command(aliases=['poll2electricboogaloo','pollv2'])
    @commands.has_permissions(administrator=True) 
    async def poll2(self, ctx, *, args):
        """
        creates anonymous poll with/without a timed ending
        .poll2 <optional time until end> {the title of the poll} [name of options]
        WARNING: wait until all reactions are added by the bot before reacting
        """
        time = None
        footer = ''
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
            footer += f'time: {strtime}\n'
        
        embed = discord.Embed(title=name,color=discord.Color.green(),description=description)
        embed.set_footer(text=footer)
        message = await ctx.send(embed=embed)
        message2 = await ctx.send('`please wait until all reactions are added before reacting`')
        # adds a message id to the end of the poll
        footer += f'id: {message.id}'
        embed.set_footer(text=footer)
        await message.edit(embed=embed)
        
        #add reactions
        for count in range(len(args)):
            await message.add_reaction(self.pollsigns[count])

        await message2.delete()
        self._update_guilds()

        poll_id = self.sql.add_poll(str(message.id), str(message.channel.id), str(message.author.guild.id), name, time, self.pollsigns, args)
        if time:
            self.sched.add_job(self._end_poll, 'date', run_date=time, args=[poll_id],id=poll_id)

    @poll2.error
    async def poll2_error(self, ctx, error):
        if isinstance(error, commands.errors.MissingRequiredArgument) or isinstance(error, discord.errors.DiscordException):
            await ctx.send('`ERROR Missing Required Argument: make sure it is .poll2 <time ddhhmmss> {title} [args]`')
        else:
            print(error)

        
    @commands.command(aliases=['checkvote'])
    async def checkvotes(self, ctx):
        """
        allows the user to check who they voted for
        it will dm users with every poll they are currently voting on
        """
        
        polls = self.sql.check_polls(str(ctx.author.id))
        # removes duplicate polls from data
        polls = list(dict.fromkeys(polls))
        await ctx.message.delete()
        
        if len(polls) == 0:
            msg = await ctx.send('You havent voted on any active polls')
            await sleep(10)
            await msg.delete()
        else:
            for poll in polls:
                votes = self.sql.check_votes(str(ctx.author.id), poll[0])

                description = 'You have voted: \n\n'
                for vote in votes:
                    description += vote[0] + '\n'
                embed = discord.Embed(title=f'on poll: {votes[0][1]}',color=discord.Color.green(),description=description)
                await ctx.author.send(embed=embed)
    
    @checkvotes.error
    async def check_votes_error(self, ctx, error):
        if isinstance(error, commands.errors.MissingRequiredArgument) or isinstance(error, discord.errors.DiscordException):
            await ctx.send('`ERROR Missing Required Argument: make sure it is .checkvotes`')
        else:
            print(error)


    @commands.command(aliases=['stoppoll','stopoll','stop_poll'])
    @commands.has_permissions(administrator=True) 
    async def endpoll(self, ctx, message_id:str, dm:bool):
        """
        Can be used to end anonymous polls (poll2)
        needs to be ran in the same channel as the poll
        True = send results to dms, False = sends results to the channel
        """
        channel_id = str(ctx.channel.id)
        guild_id = str(ctx.guild.id)
        
        poll_info = self.sql.location_get_poll(message_id, channel_id, guild_id)

        if not poll_info:
            await ctx.send('`no poll detected please check you are running it in the same channel as the poll`')
            return
        else:
            poll_info = poll_info[0]

        poll_id = str(poll_info[0])
        poll_date = poll_info[1]

        if poll_date:
            self.sched.remove_job(poll_id)
        
        poll_info, votes = self.sql.get_poll_info(poll_id)

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
        
        self.sql.remove_poll(poll_id)
        embed = discord.Embed(title=poll_info[1],color=discord.Color.green(),description=description)
        
        if dm == False:
            await ctx.send(embed=embed)
        else:
            await ctx.author.send(embed=embed)

    @endpoll.error
    async def endpoll_error(self, ctx, error):
        if isinstance(error, commands.errors.MissingRequiredArgument) or isinstance(error, discord.errors.DiscordException):
            await ctx.send('`ERROR Missing Required Argument: make sure it is .deletepoll <message id> <send to dms True/False>`')
        else:
            print(error)

    
    @commands.command(aliases=['removepoll'])
    @commands.has_permissions(administrator=True) 
    async def deletepoll(self, ctx, message_id):
        """
        Can be used to delete anonymous polls (poll2)
        needs to be ran in the same channel as the poll
        """
        channel_id = str(ctx.channel.id)
        guild_id = str(ctx.guild.id)
        
        deleted = self._delete_poll(message_id, channel_id, guild_id)
        if deleted == True:
            await ctx.send('`deleted poll`')
        else:
            await ctx.send('`no poll detected please check you are running it in the same channel as the poll`')

    @deletepoll.error
    async def delete_poll_error(self, ctx, error):
        if isinstance(error, commands.errors.MissingRequiredArgument) or isinstance(error, discord.errors.DiscordException):
            await ctx.send('`ERROR Missing Required Argument: make sure it is .deletepoll <message id>`')
        else:
            print(error)


    @commands.command(aliases=['rp'])
    async def raidpoll(self, ctx, *,title='Raid Times'):
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
    async def poll(self, ctx, *, args= ' '):
        """
        normal poll
        .poll some thing 
        or
        .poll {title} [option] [option]
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
    
    @poll.error
    async def poll_error(self, ctx, error):
        if isinstance(error, commands.errors.MissingRequiredArgument):
            await ctx.send('`ERROR Missing Required Argument: make sure it is .poll {title} [args]`')
        else:
            print(error)

def setup(client):
    client.add_cog(poll(client))
