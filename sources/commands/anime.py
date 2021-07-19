import discord
from discord.ext import commands
from sources.lib.animeStuff import timeUntilAiring


class AniList(commands.Cog):

    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.command()
    async def anime(self, context, *args):

        if len(args) == 0:
            embed = discord.Embed(title="An anime is required.", colour=discord.Colour.red())

        else:
            title = " ".join(args)
            embed = await timeUntilAiring(title)

        await context.send(embed=embed)
        await context.message.delete()


def setup(bot: commands.Bot):
    bot.add_cog(AniList(bot))
