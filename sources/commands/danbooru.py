from discord.ext import commands
from sources.lib.danbooru import sendDanbooruIm


class Danbooru(commands.Cog):

    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.command()
    async def danbooru(self, context, tag="*"):
        embed = await sendDanbooruIm(tag)
        await context.send(embed=embed)
        await context.message.delete()


def setup(bot: commands.Bot):
    bot.add_cog(Danbooru(bot))
