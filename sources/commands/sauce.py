from discord.ext import commands
from sources.lib.sauces import getSauce


class Sauce(commands.Cog):

    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.command()
    async def sauce(self, context):
        message = context.message

        if len(message.attachments) == 0:
            embed = await getSauce(message.content[7:])

        else:
            embed = await getSauce(message.attachments[0].proxy_url)

        await context.send(embed=embed)


def setup(bot: commands.Bot):
    bot.add_cog(Sauce(bot))
