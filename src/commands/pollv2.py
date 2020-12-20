import re
import discord
import asyncio
import datetime
from discord.ext import commands
from converter.datetimeCalc import datetimeCal
from sql.pollv2 import sql_class
from apscheduler.schedulers.asyncio import AsyncIOScheduler

class poll(commands.Cog):
    '''
    super fancy shmancy poll command
    '''
    def __init__(self, client):
        self.client = client
        self.pollsigns = ["🇦","🇧","🇨","🇩","🇪","🇫","🇬","🇭","🇮","🇯","🇰","🇱","🇲","🇳","🇴","🇵","🇶","🇷","🇸","🇹","🇺","🇻","🇼","🇽","🇾","🇿"]
        self.sched = AsyncIOScheduler()
        self.sched.start()

        client.loop.create_task(self.async_init())
 
    async def async_init(self):
        await self.client.wait_until_ready()

        sql = sql_class()
        polls = sql.get_polls()
        now = datetime.datetime.now()
        for poll in polls:
            poll_id = str(poll[0])
            poll_datetime = poll[1] 
            if poll_datetime > now:
                self.sched.add_job(self._poll2_end, 'date', run_date=poll_datetime, args=[poll_id],id=poll_id)
            else:
                await self._poll2_end(poll_id)
        
    async def _poll2_end(self, poll_id):
        sql = sql_class()
        poll_info, votes = sql.get_poll_info(str(poll_id))
        #print(poll_info,votes)
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
            
            print(dict)
            for key,value in dict.items():
                description+=f'{value} votes for {key} \n\n'
        
        sql.remove_poll(poll_id)

        embed = discord.Embed(title=poll_info[1],color=discord.Color.green(),description=description)
        channel = self.client.get_channel(int(poll_info[0]))
        await channel.send(embed=embed)

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        """
        toggles the voting option for this poll
        """
        message_id = str(payload.message_id)
        channel_id = str(payload.channel_id)
        guild_id = str(payload.guild_id)   
        user_id = str(payload.user_id)
        
        # breaks if its the bot
        if user_id == '785578758450708492':
            return
        
        if payload.emoji.name not in self.pollsigns:
            return

        # if it has an id, its not one of the abcdef emotes
        if payload.emoji.name in self.pollsigns:
            emote_id = str(ord(payload.emoji.name))
            sql = sql_class()
            toggle = sql.toggle_vote(message_id, channel_id, guild_id, emote_id, user_id)

            if toggle == False or toggle == True:
                channel = self.client.get_channel(payload.channel_id)
                message = await channel.fetch_message(payload.message_id)
                await message.remove_reaction(payload.emoji, payload.member)        

    @commands.command(aliases=['poll2electricboogaloo','poll'])
    async def poll2(self, ctx, time: datetimeCal, *, args):
        """
        .poll2 7d2h {who do you want to vote lol?} [arg1] [arg2]
        """
        # checks message against regex to see if it matches
        reg = re.compile('({.+})\ *(\[[^\n\r\[\]]+\] *)+')
        if not reg.match(args):
            raise discord.errors.DiscordException

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
            description += self.pollsigns[count] + ' ' + args[count] + '\n\n'

        embed = discord.Embed(title=name,color=discord.Color.green(),description=description)
        message = await ctx.send(embed=embed)

        #add reactions
        for count in range(len(args)):
            await message.add_reaction(self.pollsigns[count])

        sql = sql_class()   
        poll_id = sql.add_poll(str(message.id), str(message.channel.id), str(message.author.guild.id), name, time, self.pollsigns, args)

        self.sched.add_job(self._poll2_end, 'date', run_date=time, args=[poll_id],id=poll_id)
        


    @poll2.error
    async def reload_error(self, ctx, error):
        print(error)
        if isinstance(error, commands.errors.MissingRequiredArgument) or isinstance(error, discord.errors.DiscordException):
            await ctx.send('`ERROR Missing Required Argument: make sure it is .poll2 <time ddhhmmss> {title} [args]`')
        else:
            print(error)

    @commands.command(aliases=['checkvotes'])
    async def check_votes(self, ctx):
        '''
        allows the user to check who they voted for
        '''
        sql = sql_class()
        polls = sql.check_polls(str(ctx.author.id))
        # removes duplicate polls from data
        polls = list(dict.fromkeys(polls))
        
        if len(polls) == 0:
            await ctx.send('You havent voted on any active polls')
        elif len(polls) == 1:
            votes = sql.check_votes(str(ctx.author.id), polls[0][0])
            await ctx.author.send(embed=self._sendvoted(votes))
        else:
            description = 'which poll do you want to see? \n\n' 
            for count in range(len(polls)):
                description += self.pollsigns[count] + ' ' + sql.get_poll_name(polls[count][0]) + '\n'
            
            embed = discord.Embed(title='Select a poll',color=discord.Color.green(),description=description)
            msg = await ctx.author.send(embed=embed)

            for count in range(len(polls)):
                await msg.add_reaction(self.pollsigns[count])
            
            def check(reaction, user):
                return user == ctx.message.author and str(reaction.emoji) in self.pollsigns
            
            try:
                reaction, user = await self.client.wait_for('reaction_add', timeout=100, check=check)
                if reaction.emoji in self.pollsigns:
                    await msg.delete()
                    votes = sql.check_votes(str(ctx.author.id), polls[self.pollsigns.index(reaction.emoji)][0])
                    await ctx.author.send(embed=self._sendvoted(votes))
                    return

            except asyncio.TimeoutError:
                await ctx.send("Timed out")


        # await ctx.author.send('👋')

    def _sendvoted(self, votes):
        description = 'You have voted: \n\n'
        for vote in votes:
            description += vote[0] + '\n'
        
        embed = discord.Embed(title='on poll "'+votes[0][1]+'"',color=discord.Color.green(),description=description)
        return embed

def setup(client):
    client.add_cog(poll(client))
