import asyncio

import discord
from discord.ext import commands

from apis import urban

class search(commands.Cog, name='Search Commands'):
    '''
    Search Commands
    With this you can search for content on various websites :)
    '''
    def __init__(self, client):
        self.client = client

    async def generate_urban_embed(self, definition, n):
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

        embed = discord.Embed(title=f'Urban Dictionary\'s results for {title}', description= f'[{n+1}/{len(definition)}]\n__**Definition**__\n{meaning}\n\n__**Example**__\n{example}\n\n__**Author**__\n{author}', color=discord.Color(0x4f9406))
        embed.set_footer(text='👍 : ' + str(definition[n]['votes']['up']) + ' | 👎 : ' + str(definition[n]['votes']['down']))

        return embed

    @commands.command()
    async def urban(self, ctx, *, query = ' '):
        """
        : Looks up a term on Urban Dictionary
        """
        if query != ' ':
            definition = await urban.getDefinitions(query)
            if definition != -1:
                def_index = 0
                msg = await ctx.send(embed=await self.generate_urban_embed(definition, def_index))
                await msg.add_reaction('◀️')
                await msg.add_reaction('⏹️')
                await msg.add_reaction('▶️')
                
                # Checks if the reaction is forward or backwards, if it is the user that invoked the command and if it is on the correct message.
                def check(reaction, user):
                    return str(reaction.emoji) in ['▶️','⏹️','◀️'] and user == ctx.message.author# and reaction.message.id == msg.id

                async def moveLoop(def_index):
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
                        if str(reaction.emoji) == '▶️' and (def_index + 1) < len(definition):
                            def_index += 1
                        if str(reaction.emoji) == '◀️' and (def_index - 1) >= 0:
                            def_index -= 1

                        # If the stop button isn't hit
                        if str(reaction.emoji) != '⏹️':
                            # Edit the message with the new embed with the new index
                            await msg.edit(embed= await self.generate_urban_embed(definition, def_index))
                            
                            # Remove the used reaction
                            await msg.remove_reaction(str(reaction.emoji), ctx.author)
                            
                            # Restart the reaction check loop
                            await moveLoop(def_index)
                        else:
                            # Clear all reactions
                            await msg.clear_reaction('▶️')
                            await msg.clear_reaction('⏹️')
                            await msg.clear_reaction('◀️')
                
                await moveLoop(def_index)

            else:
                await ctx.send(f'I could not find anything with the query `{query} :(`')
        else:
            await ctx.send('You did not give me a query :(')

    

def setup(client):
    client.add_cog(search(client))