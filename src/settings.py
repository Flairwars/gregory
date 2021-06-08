"""
Contains all configuration for bot.
All settings should be loaded from enviroment variables.
For development, create a .env file in the package and make sure python-dotenv is installed.
"""

import logging
import os

log = logging.getLogger(__name__)

# Check for python-dotenv
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    logging.error("python-dotenv not loaded. Hope you set your environment variables.")

DEBUG: bool = bool(os.getenv("DEBUG", False))
TOKEN: str = os.getenv("TOKEN")
REDDIT_ID: str = os.getenv("REDDIT_ID")
REDDIT_SECRET: str = os.getenv("REDDIT_SECRET")

# Debug Mode Setup
__handlers = [logging.FileHandler('data/logs/discord_bot.log'), logging.StreamHandler()]
__format = '%(asctime)s:%(name)s:%(levelname)s %(message)s'
# if 'logs' not in os.listdir('data'):
#     os.mkdir('data/logs')
# data/logs/

if DEBUG is True:
    # noinspection PyArgumentList
    logging.basicConfig(
        level=logging.DEBUG,
        format=__format,
        handlers=__handlers
    )
    # Set Logger Level
    logging.root.setLevel(logging.DEBUG)
    logging.getLogger("discord").setLevel(logging.WARN)
    logging.getLogger("apscheduler.scheduler:Scheduler").setLevel(logging.WARN)
    logging.getLogger("cppimport.import_hook").setLevel(logging.ERROR)
    log.info("Debug Mode Enabled")
else:
    # noinspection PyArgumentList
    logging.basicConfig(
        level=logging.INFO,
        format=__format,
        handlers=__handlers
    )
    logging.root.setLevel(logging.INFO)
    logging.getLogger("discord").setLevel(logging.ERROR)
    logging.getLogger("apscheduler.scheduler:Scheduler").setLevel(logging.ERROR)
    logging.getLogger("cppimport.import_hook").setLevel(logging.ERROR)

# Check for token and exit if not exists
if TOKEN is None:
    log.error("Discord API token not set")
    exit()
elif REDDIT_ID  is None or REDDIT_SECRET is None:
    log.error("REDDIT ID or SECRET not set")
    log.error(f"REDDIT_ID: {REDDIT_ID}")
    log.error(f"REDDIT_SECRET: {REDDIT_SECRET}")

