import praw
from decouple import config
from time import time
class reddit_class():
    def __init__(self):
        self.reddit = praw.Reddit(
            client_id=config('REDDITID'),
            client_secret=config('REDDITSECRET'),
            user_agent='TheGreenArmy Gregory Discord bot'
        )
    
    def get_125_hotposts(self, sub):
        """
        gets the top 125 posts from hot on a reddit sub
        input: <str> sub name
        output: ???
        """
        t1= time()
        #posts = filter(lambda x: x.stickied == False, list(iter(self.reddit.subreddit(sub).hot(limit=130))))
        
        posts = list(iter(self.reddit.subreddit(sub).hot(limit=130)))
        
        t2 = time()
        posts = filter(lambda x: x.stickied == False, posts)
        
        t3 = time()
        posts = []
        stickies = 0
        for submission in self.reddit.subreddit(sub).hot(limit=130):
            if submission.stickied:
                stickies += 1
            posts.append(submission)
        
        posts = posts[stickies:]

        t4 = time()
        print(f'{round((t2-t1)*1000)}')
        print(f'{round((t3-t2)*1000)}')
        return posts