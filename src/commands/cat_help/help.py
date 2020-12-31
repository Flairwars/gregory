from discord.ext import commands
from pathlib import Path
import pprint


class help(commands.Cog, name='help'):
    """
    Help Command
    """

    def __init__(self, client):
        self.client = client
        self.category = Path(__file__).parent.absolute().name[4:]

    @commands.command()
    async def help(self, ctx, query=''):
        """
        Opens this menu.
        """
        query = query.lower()

        categories = {}

        for cog in self.client.cogs.values():
            for command in cog.walk_commands():
                if cog.category not in categories.keys():
                    categories[cog.category] = [(command.name,command.help,command.signature,command.aliases)]
                else:
                    categories[cog.category].append((command.name,command.help,command.signature,command.aliases))

        response = ''
        if query == '':
            response += "**I'll gladly assist you :)**\n"
            response += 'To get more information on the commands in the category, simply do `help <category>`!\n'
            response += 'Categories:\n'
            for name, content in categories.items():
                response += f'\n{name} --- `'
                for i in range(len(content)):
                    if i == 5:
                        break
                    response += f'{content[i][0]}, '
                if len(content) > 5:
                    response += '...`'
                else:
                    response = response[0:-2] + '`'
        else:
            if query in categories.keys():
                response += f'**{query.capitalize()} Category**\n'
                response += 'To get more info on each command itself, simply do `help <command>`!\n'
                response += 'Commands:\n'

                for command in categories[query]:
                    response += f'\n{command[0]} --- '
                    response += f'{command[1]} | {command[2]}'
            else:
                for cat in categories.values():
                    for com in cat:
                        if query == com[0]:
                            response += f'**{com[0]}**\n'
                            if len(com[3]) > 0:
                                response += f'Aliases: {com[3]}\n\n'
                            response += f'{com[1]}\n\n'
                            if len(com[2]) > 0:
                                response += f'Usage: {com[2]}'

        if response == '':
            return await ctx.send(f'I could not find anything for `{query}`')

        return await ctx.send(response)


def setup(client):
    client.add_cog(help(client))
