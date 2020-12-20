Gregory
-------
hello and welcome to the gregory github repository. Feel free to build and add on the existing code or steal any code you like

### Resources 
This discord bot is running on my Raspberry pi 3b+ 24/7. This Pi is also running a mariaDB SQL server

### How to contribute code
#### General setup
First, you need to message me on discord with your github account name so i can add you as a contributer on the github

Secondly, you need to create a branch of master. you need to call the branch after what you are programming on it. You will also need to install / setup some files.
You will need to run some commands. These commands are as follows:

**windows**
```
cd {the directory that the github repo is in}
pip install virtualenv
python -m venv env
env/Scripts/activate.bat (to enter the vitual enviroment)
pip install -r requirements
```
**linux**
```
cd {the directory that the github repo is in}
pip3 install virtualenv
python3 -m venv env
source env/bin/activate (to enter the vitual enviroment)
pip install -r requirements.txt
```

Every time you wish to program in gregory, unless your IDE does it for you, you will need to enter the virtual enviroment. VSCode is one such IDE that enters it for you.

afterwards, you need to make a file inside the folder.
the file is called `.env`.
In this file you must enter the following:
```
TOKEN={enter your bot token}
```

#### Programming
The file structure looks like this:
```
requirments.txt
src/commands
   /apis
   /sql
   /converters
```
(these only contain the relavent files for simplisity)
All programming files are stored within src
there are 4 main files

**commands**

commands is where you store your cogs that you program for the bot (Cogs are modules for the discord bot). you can use .load, .unload and .reload commands on discord to load induvidual modules.

**apis**

This is where you store classes for scraping websites and using apis. these can then be imported in your cog. 
Name the file after the api or website you are accessing

**sql**

This is where you store classes for accessing the sql server. these can then be imported in your cog.
Name the file the same as the file in the commands folder so that people know which file uses which

**converters**

This is where cog converters are stored. These let you filter arguments in a command when commands are run in cogs. For example, datetimeCalc converts ddhhmmss to datetime.

#### Commiting changes
Once you are finished programming, you will need to make a pull request. You can make a pull request here https://github.com/Blotz/gregory/pulls. The base will be `master` and the compare will be `{the name of your branch}`. Once you are finished, I'll reveiw the code and merge it to the bot.
