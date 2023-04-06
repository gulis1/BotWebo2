import discord
from discord.ext import commands
from sources.lib.animeStuff import timeUntilAiring


class AniList(commands.Cog):

    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.command()
    async def anime(self, context, *args):

        """ Usage
            --------
                [COMMAND_PREFIX]anime [ANIME_NAME]
        """

        if len(args) == 0:
            embed = discord.Embed(title="An anime is required.", colour=discord.Colour.red())

        else:
            title = " ".join(args)
            embed = await timeUntilAiring(title)

        await context.send(embed=embed)
        await context.message.delete()


async def setup(bot: commands.Bot):
    await bot.add_cog(AniList(bot))
