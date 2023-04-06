import discord
from discord.ext import commands


class Misc(commands.Cog):

    """ Miscelaneus function """

    def __init__(self, bot: commands.Bot):
        bot.remove_command("help")
        self.bot = bot

    @commands.command()
    async def pekofy(self, context):

        """ Only the chosen will know. """

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

        """ Help msg. """

        if part == "music":
            text = """
                **•  play <url/nombre/numero> (r)** _Supports searching by name, youtube videos and playlists and spotify playlists and albums_
                **•  playlist** _Shows the current playlist_
                **•  song** _Shows the current song and its duration_
                **•  empty** _Empties the playlist_
                **•  loop <off/single/all>** _Loops one (single) song or the whole playlist (all) or unloops it (off)_
                **•  skip (ind)** _Skips the current song or advance to the index_
                **•  leave** _Force the Bot to leave the channel
                **•  remove** _Removes the current song from the playlist_
                **•  rload** _Loads completed anime list from anilist username_
                **•  rplay** _Plays random songs from the anime list loaded_
                **•  rstop** _Stop playing random theme_
                **•  ruser** _Shows current list owner_
           """

        elif part == "danbooru":
            text = """
                **•  danbooru <tags>** _Sends an img from the tag given or a random img if no tag_
                **•  tags <tags>** _Shows a list of possible tags related to the tag_
           """

        elif part == "sauces":
            text = """
                **•  sauce <url>** _Searchs for the img given and sends the source of the img if exists_
           """

        elif part == "anime":
            text = """
                **•  anime <name>** _Search if the anime exists, if exists sends the state (airing/finished/not_yet_released)_
            """

        elif part == "imagenes":
            text = """
                **•  pekora**
                **•  yes**
                **•  no**
                **•  pray**
                **•  haachama**
                **•  smug**
                **•  pray**
                **•  please**
                **•  trembling**
            """

        else:

            text = """
                **•  help music**
                **•  help danbooru**
                **•  help sauces**
                **•  help anime**
                **•  help imagenes**
            """

        await context.send(embed=discord.Embed(title=("Help " + part + ":") , description=text, colour=discord.Color.green()))


async def setup(bot):
    await bot.add_cog(Misc(bot))
