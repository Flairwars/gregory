import pathlib

from discord.ext import commands, tasks
from sql.count import sql_class
from reddit.count import reddit_class

class count(commands.Cog, name='count'):
    """
    Count command shiz
    """
    def __init__(self, client):
        self.client = client
        self.category = pathlib.Path(__file__).parent.absolute().name[4:]
        self.update_colour_database.start()
        red_sub = ("DSRRed", "red")
        orange_sub = ("EternalOrange", "orange")
        yellow_sub = ("YellowOnlineUnion", "yellow")
        green_sub = ("TheGreenArmy", "green")
        blue_sub = ("AzureEmpire", "blue")
        purple_sub = ("PurpleImperium", "purple")

        self.sub = {
        "red": red_sub,
        "rd": red_sub,
        "r": red_sub,

        "orange": orange_sub,
        "ornge": orange_sub,
        "orang": orange_sub,
        "o": orange_sub,

        "yellow": yellow_sub,
        "yelow": yellow_sub,
        "y": yellow_sub,

        "green": green_sub,
        "grn": green_sub,
        "g": green_sub,

        "blue": blue_sub,
        "blu": blue_sub,
        "b": blue_sub,

        "purple": purple_sub,
        "purp": purple_sub,
        "p": purple_sub,

        "pink": green_sub
        }
        
        green_flairs = [
        "evergreen",
        "verdant conclave",
        "commander",
        "greenie"
        ]
        mod_flairs = [
            'cat_mod',
            'boily oil'
        ]
        blue_flairs = [
            "emperor",
            "synedrion"
        ]

        self.flairs = [
            # main chunk of flairs on mega or green
            (lambda flair:"red" in flair, "red"),
            (lambda flair:"orange" in flair, "orange"),
            (lambda flair:"yellow" in flair, "yellow"),
            (lambda flair:"green" in flair, "green"),
            (lambda flair:"blue" in flair, "blue"),
            (lambda flair:"purple" in flair, "purple"),
            # special flairs on green
            (lambda flair: flair in green_flairs, 'green'),
            (lambda flair:"verdancy" in flair, "green"),
            # special flairs for oils
            (lambda flair: flair in mod_flairs, 'cat_mod'),
            # special flairs for reds
            (lambda flair:"premier" in flair, "red"),
            (lambda flair:"crimson" in flair, "red"),
            # special flairs for blue
            (lambda flair: flair in blue_flairs, 'blue'),
            # special flairs for purple
            (lambda flair:"knight" in flair, "purple")
        ]

    def cog_unload(self):
        self.update_colour_database.cancel()
    
    #async def on_cog_unload():
    @tasks.loop(hours=6)
    async def update_colour_database(self):
        """
        automatically updating the reddit user database in the background
        """
        reddit = reddit_class()
        sql = sql_class()
        
        posts = reddit.get_hotposts('Flairwars', 100)
        posts += reddit.get_hotposts('DSRRed',100)
        #posts += reddit.get_hotposts('EternalOrange',100) honestly fuck orange flairs. they can suck my hairy balls
        #posts += reddit.get_hotposts('YellowOnlineUnion',100) fuck yellow too. the flairs are shit
        posts += reddit.get_hotposts('TheGreenArmy',100)
        posts += reddit.get_hotposts('AzureEmpire',100)
        posts += reddit.get_hotposts('PurpleImperium',100)

        users = []
        for submission in posts:
            # submission = <class> reddit post
            if submission.author_flair_text:
                author = submission.author.name
                if author not in users:
                    color = submission.author_flair_text
                    # checks if we have already checked this user reacently
                    flair_name = submission.author_flair_text.lower()
                    for flair in self.flairs:
                        if flair[0](flair_name):
                            color = flair[1]
                            break
                    
                    users.append(author)
                    if not sql.user_exists(author):
                        sql.add_user(author, color)

    
    @commands.command(aliases=["c"])
    async def count(self, ctx, col = "green"):
        """
        count the other color subs
        """
        col = col.lower()
        # gets the sub name
        if col not in self.sub.keys():
            await ctx.send('`Sub not found`')
            return
        sub = self.sub[col]
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
                    response += f'{key} : {str(count[page][key])}\n'.replace("_","\_").replace("*","\*").replace("~","\~")
        
        await msg.edit(content=response)


def setup(client):
    client.add_cog(count(client))