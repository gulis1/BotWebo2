from discord.ext import commands
from sources.lib.danbooru import sendDanbooruIm


class Danbooru(commands.Cog):

    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.command()
    async def danbooru(self, context, tag="*"):

        """ Multiple usages:
                [COMMAND_PREFIX]danbooru: gets a random image
                [COMMAND_PREFIX]danbooru [tag]: gets a random image for the tag given
        """

        embed = await sendDanbooruIm(tag)
        await context.send(embed=embed)
        await context.message.delete()


def setup(bot: commands.Bot):
    bot.add_cog(Danbooru(bot))
