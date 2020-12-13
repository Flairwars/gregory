import asyncio

import discord
from discord.ext import commands

from apis import urban, weather, wyr, constants


async def generate_urban_embed(definition, n, query):
    if n < 0:
        n = 0
    if n >= len(definition):
        n = len(definition) - 1
    meaning = definition[n]['meaning']
    example = definition[n]['example']
    title = definition[n]['title']
    if len(meaning) + len(example) > 1800:
        if len(meaning) > 500:
            meaning = meaning[:500]
            meaning = meaning[:meaning.rfind(" ")]
            meaning += "[[...]](https://www.urbandictionary.com/define.php?term=" + query.lower() + ")"
        if len(example) > 500:
            example = example[:500]
            example = example[:example.rfind(" ")]
            example += "[[...]](https://www.urbandictionary.com/define.php?term=" + query.lower() + ")"
    authorName = definition[n]['contributor']['author']
    authorLink = definition[n]['contributor']['link']
    author = f'[{authorName}]({authorLink})'

    description = f'[{n + 1}/{len(definition)}]\n__**Definition**__\n{meaning}\n\n__**Example**__\n{example}\n\n' \
                  f'__**Author**__\n{author} '

    embed = discord.Embed(title=f'Urban Dictionary\'s results for {title}',
                          description=description,
                          color=discord.Color(0x4f9406))
    embed.set_footer(
        text='👍 : ' + str(definition[n]['votes']['up']) + ' | 👎 : ' + str(definition[n]['votes']['down']))

    return embed


class Search(commands.Cog, name='Search Commands'):
    '''
    Search Commands
    With this you can search for content on various websites :)
    '''

    def __init__(self, client):
        self.client = client

        
    @commands.command(aliases=['ub'])
    async def urban(self, ctx, *, query=' '):
        """
        : Looks up a term on Urban Dictionary
        """
        if query != ' ':
            definition = await urban.getDefinitions(query)
            if definition != -1:
                def_index = 0
                msg = await ctx.send(embed=await generate_urban_embed(definition, def_index, query))
                await msg.add_reaction('◀️')
                await msg.add_reaction('⏹️')
                await msg.add_reaction('▶️')

                # Checks if the reaction is forward or backwards, if it is the user that invoked the command and if
                # it is on the correct message.
                def check(reaction, user):
                    return str(reaction.emoji) in ['▶️', '⏹️', '◀️'] and user == ctx.message.author

                async def move_loop(index):
                    try:
                        # Waits for a reaction that passes the check
                        reaction, user = await self.client.wait_for('reaction_add', timeout=60.0, check=check)
                    except asyncio.TimeoutError:
                        # Is invoked if the timeout is reached without a passed check
                        # Clear all reactions
                        await msg.clear_reaction('▶️')
                        await msg.clear_reaction('⏹️')
                        await msg.clear_reaction('◀️')
                    else:
                        # Is invoked once the check is passed

                        # Changes the index if right or left arrow is hit
                        if str(reaction.emoji) == '▶️' and (index + 1) < len(definition):
                            index += 1
                        if str(reaction.emoji) == '◀️' and (index - 1) >= 0:
                            index -= 1

                        # If the stop button isn't hit
                        if str(reaction.emoji) != '⏹️':
                            # Edit the message with the new embed with the new index
                            await msg.edit(embed=await generate_urban_embed(definition, index, query))

                            # Remove the used reaction
                            await msg.remove_reaction(str(reaction.emoji), ctx.author)

                            # Restart the reaction check loop
                            await move_loop(index)
                        else:
                            # Clear all reactions
                            await msg.clear_reaction('▶️')
                            await msg.clear_reaction('⏹️')
                            await msg.clear_reaction('◀️')

                await move_loop(def_index)

            else:
                await ctx.send(f'I could not find anything with the query `{query}` :(')
        else:
            await ctx.send('You did not give me a query :(')

    @commands.command()
    async def weather(self, ctx, *, query=' '):
        '''
        Gives you the weather :)
        '''
        data = await weather.get_current(query)

        if query == ' ':
            await ctx.send('You did not give me a location :(')
        else:
            if data is not None:
                response = '```\n'
                sign = constants.WEATHER_SYMBOL_WEGO[constants.WWO_CODE[data['weatherCode']]]

                response += sign[0] + f'{data["weatherDesc"][0]["value"]}\n'
                response += sign[1] + f'{data["FeelsLikeC"]}..{data["temp_C"]} °C | {data["FeelsLikeF"]}..{data["temp_F"]} °F\n '
                response += sign[2] + f'{data["windspeedKmph"]} km/h | {data["windspeedMiles"]} mph\n'
                response += sign[3] + f'{data["humidity"]}%\n'
                response += sign[4] + f'{data["precipMM"]}\n'
                response += '```'
                await ctx.send(response)
            else:
                await ctx.send(f'I couldn\'t find the place `{query}` :(')

    @commands.command(aliases=['wouldyourather'])
    async def wyr(self, ctx, *, query=' '):
        options = await wyr.get_wyr()

        response = f'**Would you rather** (http://either.io/)\n:regional_indicator_a: {options["blue"]}'
        response += f'\n**OR**\n:regional_indicator_b: {options["red"]}'

        msg = await ctx.send(response)
        await msg.add_reaction('🇦')
        await msg.add_reaction('🇧')


def setup(client):
    client.add_cog(Search(client))
