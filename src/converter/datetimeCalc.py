from discord.ext import commands
import datetime
class datetimeCal(commands.Converter):
    async def convert(self, ctx, argument):

        argument = argument.lower()# our weird as fauck string
        timeLetters = ['d','h','m','s']

        timeDict = {}
        for timeLetter in timeLetters:
            found = argument.find(timeLetter)
            if found != -1:
                splitarguments = argument.split(timeLetter)
                timeDict[timeLetter]=float(splitarguments[0])
                argument = splitarguments[1]
            else:
                timeDict[timeLetter] = 0
        
        now = datetime.datetime.now()
        due = now + datetime.timedelta(days=timeDict['d'], hours=timeDict['h'], minutes=timeDict['m'], seconds=timeDict['s'])
        
        return due