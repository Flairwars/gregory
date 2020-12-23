import asyncio
import json

import praw
from decouple import config


async def get_posts(colour):
    reddit = praw.Reddit(
        client_id=config('REDDITID'),
        client_secret=config('REDDITSECRET'),
        user_agent='TheGreenArmy Gregory Discord bot'
    )

    sub = (await convert_to_sub(colour.lower()))

    if sub is None:
        return None

    sub = sub[0]

    # Grabs 125 posts without stickied posts.
    posts = []
    stickies = 0
    for submission in reddit.subreddit(sub).hot(limit=127):
        if submission.stickied:
            stickies += 1
        posts.append(submission)

    # Remove the stickied posts.
    posts = posts[stickies:]

    # Include only the author names.
    posts = list(map(lambda a: a.author.name, posts))

    # Split posts up into the pages.
    # This will also remove redundant posts, if the sub has less than two stickies.
    page_posts = []
    for i in range(0, 5):
        page_posts.append(posts[i * 25:(i + 1) * 25])

    return page_posts


async def convert_to_sub(colour):
    red_sub = ("DSRRed", "red")
    orange_sub = ("EternalOrange", "orange")
    yellow_sub = ("YellowOnlineUnion", "yellow")
    green_sub = ("TheGreenArmy", "green")
    blue_sub = ("AzureEmpire", "blue")
    purple_sub = ("PurpleImperium", "purple")

    col_sub = {
        "red": red_sub,
        "re": red_sub,
        "rd": red_sub,
        "r": red_sub,
        "orange": orange_sub,
        "ornge": orange_sub,
        "orage": orange_sub,
        "orang": orange_sub,
        "oran": orange_sub,
        "ora": orange_sub,
        "orng": orange_sub,
        "or": orange_sub,
        "o": orange_sub,
        "yellow": yellow_sub,
        "yello": yellow_sub,
        "yelow": yellow_sub,
        "yelo": yellow_sub,
        "yellw": yellow_sub,
        "yel": yellow_sub,
        "yell": yellow_sub,
        "ye": yellow_sub,
        "y": yellow_sub,
        "green": green_sub,
        "gren": green_sub,
        "geen": green_sub,
        "grn": green_sub,
        "gn": green_sub,
        "g": green_sub,
        "": green_sub,
        "blue": blue_sub,
        "blu": blue_sub,
        "ble": blue_sub,
        "glue": blue_sub,
        "bl": blue_sub,
        "bu": blue_sub,
        "b": blue_sub,
        "purple": purple_sub,
        "purpl": purple_sub,
        "purp": purple_sub,
        "purpe": purple_sub,
        "puple": purple_sub,
        "pupl": purple_sub,
        "pup": purple_sub,
        "pur": purple_sub,
        "pu": purple_sub,
        "p": purple_sub,
        "pink": green_sub
    }

    if colour not in col_sub.keys():
        return None
    return col_sub[colour]


async def get_stats(colour):

    colours = await get_colour_database()

    posts = await get_posts(colour)
    if posts is None:
        return None

    stats = {"colour": (await convert_to_sub(colour))[1]}
    for page in range(0, 5):
        page_cols = {}
        for author in posts[page]:
            if author not in colours.keys():
                if author not in page_cols.keys():
                    page_cols[author] = 1
                else:
                    page_cols[author] += 1
            else:
                if colours[author] not in page_cols.keys():
                    page_cols[colours[author]] = 1
                else:
                    page_cols[colours[author]] += 1
        stats[page] = page_cols

    return stats


async def get_colour_database():
    with open("colours.json", "r") as file:
        return json.load(file)


async def write_database(data):
    with open("colours.json", "w") as file:
        json.dump(data, file)


async def update_database():
    data = await get_colour_database()

    reddit = praw.Reddit(
        client_id=config('REDDITID'),
        client_secret=config('REDDITSECRET'),
        user_agent='TheGreenArmy Gregory Discord bot'
    )

    # Main sub
    for submission in reddit.subreddit('Flairwars').hot(limit=1000):
        if submission.author_flair_text:
            author_col = submission.author_flair_text.split(" ")[0].lower()
            data[submission.author.name] = author_col

    # Green sub
    green_flairs = {
        "Boily Oily": "mod",
        "Evergreen": "green",
        "Verdant Conclave": "green",
        "Commander": "green",
        "Greenie": "green",
        "Purple": "purple",
        "Red": "red",
        "Yellow": "yellow",
        "Blue": "blue",
        "Orange": "orange"
    }

    for submission in reddit.subreddit('TheGreenArmy').hot(limit=1000):
        if submission.author_flair_text:
            if "Verdancy" in submission.author_flair_text:
                data[submission.author.name] = "green"
            else:
                author_col = green_flairs[submission.author_flair_text]
                data[submission.author.name] = author_col

    await write_database(data)

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(update_database())
