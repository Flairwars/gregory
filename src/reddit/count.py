import praw
from decouple import config
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
        output: <list post>
        """
        #posts = filter(lambda x: x.stickied == False, list(iter(self.reddit.subreddit(sub).hot(limit=130))))
        
        #posts = list(iter(self.reddit.subreddit(sub).hot(limit=130)))
        #posts = filter(lambda x: x.stickied == False, posts)
        
        posts = []
        stickies = 0
        for submission in self.reddit.subreddit(sub).hot(limit=130):
            if submission.stickied:
                stickies += 1
            posts.append(submission)
        
        posts = posts[stickies:]
        return posts
    
    def get_hotposts(self,sub:str ,num:int = 100):
        '''
        gets <int> num posts from green
        input: <int> num
        output: <list class> posts
        '''
        posts = []
        for submission in self.reddit.subreddit(sub).hot(limit=num):
            posts.append(submission)
        
        return posts