from discord.ext import commands, tasks
from sql.count import sql_class
from reddit.count import reddit_class
from time import time

class count(commands.Cog, name='useful'):
    '''
    Count command shiz
    '''
    def __init__(self, client):
        self.client = client

        red_sub = ("DSRRed", "red")
        orange_sub = ("EternalOrange", "orange")
        yellow_sub = ("YellowOnlineUnion", "yellow")
        green_sub = ("TheGreenArmy", "green")
        blue_sub = ("AzureEmpire", "blue")
        purple_sub = ("PurpleImperium", "purple")

        self.color = {
        "red": red_sub,
        "rd": red_sub,
        "r": red_sub,

        "orange": orange_sub,
        "ornge": orange_sub,
        "orage": orange_sub,
        "orang": orange_sub,
        "orng": orange_sub,
        "o": orange_sub,

        "yellow": yellow_sub,
        "yelow": yellow_sub,
        "yell": yellow_sub,
        "y": yellow_sub,

        "green": green_sub,
        "gren": green_sub,
        "grn": green_sub,
        "g": green_sub,

        "blue": blue_sub,
        "blu": blue_sub,
        "b": blue_sub,

        "purple": purple_sub,
        "purp": purple_sub,
        "pur": purple_sub,
        "p": purple_sub,

        "pink": green_sub
        }
    
    @tasks.loop(hours=6)
    async def update_colour_database(self):
        '''
        automatically updating the reddit user database in the background
        '''
        #count_utils.update_database()
    
    @commands.command(aliases=["c"])
    async def count(self, ctx, col = "green"):
        '''
        : count the other color subs
        '''
        
        col = col.lower()
        # gets the sub name
        if col not in self.color.keys():
            await ctx.send('`Sub not found`')
            return
        sub = self.color[col]
        # sub = ('subname', 'color')

        msg = await ctx.send('Counting...')

        # get reddit posts from sub
        reddit = reddit_class()
        posts = reddit.get_125_hotposts(sub[0])

        # Include only the author names.
        posts = list(map(lambda a: a.author.name, posts))

        pages = []
        for i in range(0, 5):
            pages.append(posts[i * 25:(i + 1) * 25])
        # [[25 posts], [25 posts], [25 posts], [25 posts], [25 posts]]
        # post = [author_name,author_name,author_name, etc...]

        sql = sql_class()
        users = {}
        count = []
        page_count = {
                'red':0,
                'orange':0,
                'yellow':0,
                'green':0,
                'blue':0,
                'purple':0
                }
        for page in pages:
            # page = [author_name, author_name, author_name, etc...]
            # resets values in dict
            page_count = page_count.fromkeys(page_count, 0)
            
            for author in page:
                # author = 'reddit account name'
                if author in users.keys():
                    # if user has already been seen by the code
                    user_color = users[author]
                    page_count[user_color] += 1
                else:
                    # new user, color unknown
                    user_color = sql.get_user(author)# if user color unknoqn, funct returns None
                    
                    if user_color == None:
                        user_color = author
                        page_count[user_color] = 0
                    
                    page_count[user_color] += 1
                    users[author] = user_color
            count.append(page_count)
        # count = [{color posts per page},{},{}]

        response = f'**Situation over on {sub[1]}**'
        
        for page in range(0,5):
            response += f'\n**Page {page+1}**\n'
            for key in count[page].keys():
                if count[page][key] != 0:
                    response += f'{key} : {str(count[page][key])}\n'

        await msg.edit(content=response)




def setup(client):
    client.add_cog(count(client))