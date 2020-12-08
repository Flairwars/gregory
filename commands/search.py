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

    @commands.command()
    async def urban(self, ctx, *, query = ' '):
        """
        : Looks up a term on Urban Dictionary
        """
        if query != ' ':
            definition = await urban.getDefinitions(query)
            if definition != -1:
                meaning = definition[0]['meaning']
                example = definition[0]['example']
                if len(meaning) + len(example) > 1800:
                    if len(definition) > 500:
                        meaning = meaning[:500]
                        meaning = meaning[:meaning.rfind(" ")]
                        meaning += "[[...]](https://www.urbandictionary.com/define.php?term=" + query.lower() + ")"
                    if len(example) > 500:
                        example = example[:500]
                        example = example[:example.rfind(" ")]
                        example += "[[...]](https://www.urbandictionary.com/define.php?term=" + query.lower() + ")"
                authorName = definition[0]['contributor']['author']
                authorLink = definition[0]['contributor']['link']
                author = f'[{authorName}]({authorLink})'

                embed = discord.Embed(title=f'Urban Dictionary\'s results for {query}', description= f'__**Definition**__\n{meaning}\n\n__**Example**__\n{example}\n\n__**Author**__\n{author}', color=discord.Color(0x4f9406))
                embed.set_footer(text='👍 : ' + str(definition[0]['votes']['up']) + ' | 👎 : ' + str(definition[0]['votes']['down']))
                await ctx.send(embed=embed)
            else:
                await ctx.send(f'I could not find anything with the query `{query} :(`')
        else:
            await ctx.send('You did not give me a query :(')

    

def setup(client):
    client.add_cog(search(client))