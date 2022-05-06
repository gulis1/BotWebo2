import discord
from discord.ext import commands


class Misc(commands.Cog):

    def __init__(self, bot: commands.Bot):
        bot.remove_command("help")
        self.bot = bot

    @commands.command()
    async def pekofy(self, context):

        if context.message.reference is None or context.message.reference.resolved.content is None:
            await context.message.channel.send(embed=discord.Embed(title="You need to reply to a message peko.", colour=discord.Color.red()))

        else:
            replied_message = context.message.reference.resolved.content
            new_message = replied_message.replace(".", " peko.").replace("!", " peko!").replace("?", " peko?")

            if new_message[-6:-1] != " peko":
                new_message += " peko."

            await context.message.channel.send(new_message)

    @commands.command()
    async def help(self, context, part=None):
        if part == "music":
            text = """
                •  ;play <url/nombre/numero> (r) (Supports searching by name, youtube videos and playlists and spotify playlists and albums.)
                •  ;playlist
                •  ;song
                •  ;empty
                •  ;loop <off/single/all>
                •  ;skip (ind)
                •  ;leave 
                •  ;remove
           """

        elif part == "danbooru":
            text = """
                •  ;danbooru <tags>
                •  ;tags <tags>
           """

        elif part == "sauces":
            text = """
                •  ;sauce <url> 
           """

        elif part == "anime":
            text = """
            •  ;anime <name>
        """

        elif part == "imagenes":
            text = """
                •  ;pekora
                •  ;yes
                •  ;no
                •  ;pray
                •  ;haachama
                •  ;smug
            """

        else:

            text = """
                •  ;help music
                •  ;help danbooru
                •  ;help sauces
                •  ;help anime
                •  ;help imagenes
            """

        await context.send(embed=discord.Embed(title="Help:", description=text, colour=discord.Color.green()))


def setup(bot):
    bot.add_cog(Misc(bot))
