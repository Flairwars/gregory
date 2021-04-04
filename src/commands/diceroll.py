from discord.ext import commands
from random import randint


class DiceRoll(commands.Cog, name='misc'):
    def __init__(self, client):
        self.client = client

    @commands.command(aliases=['roll'])
    async def diceroll(self, ctx, *args):
        """
        rolls the dice of fate
        """

        description = ''

        # args = ['d4','4d4','4']
        for arg in args:
            # 3d4
            arg = arg.lower()
            index = arg.find('d')

            if index == -1:
                dice = int(arg)
                roll = randint(1, dice)
                description += f'dice: {dice}, count: 1\n{roll}\nTotal: {roll}\n\n'

            else:
                dice = int(arg[index + 1:])
                count = arg[:index]

                if count == '':
                    count = 1
                else:
                    count = int(count)

                total = 0
                description += f'dice: {dice}, count: {count}\n'
                for n in range(count):
                    roll = randint(1, dice)
                    total += roll
                    description += f'{roll}, '
                description = description[:-2]  # remove trailing ', '
                description += f'\nTotal: {total}\n\n'

        await ctx.send(description)


def setup(client):
    client.add_cog(DiceRoll(client))
