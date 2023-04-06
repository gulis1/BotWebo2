import discord
from discord.ext import commands

images = {"no": "https://cdn.discordapp.com/attachments/734750766895595581/843267512022859816/no.gif",
          "yes": "https://cdn.discordapp.com/attachments/734750766895595581/843267625975021568/yes.gif",
          "haachama": "https://cdn.discordapp.com/attachments/734750766895595581/843267894686908442/haachama.jpg",
          "pekora": "https://cdn.discordapp.com/attachments/734750766895595581/843268060445016105/pekora.jpg",
          "smug": "https://cdn.discordapp.com/attachments/734750766895595581/843268167089258517/smug.jpg",
          "pray": "https://cdn.discordapp.com/attachments/649025469219340288/853772957028319292/unknown.png",
          "please": "https://i1.sndcdn.com/avatars-Izsdy6YmsiXZk1Sr-8AXfwA-t500x500.jpg",
          "trembling": "https://cdn.discordapp.com/attachments/709788450408366162/972992631456030830/the-quintessential-quintuplets-itsuki.gif"
          }


class Images(commands.Cog):

    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.command()
    async def no(self, context):
        await context.message.channel.send(images["no"])
        await context.message.delete()

    @commands.command()
    async def yes(self, context):
        await context.message.channel.send(images["yes"])
        await context.message.delete()

    @commands.command()
    async def haachama(self, context):
        await context.message.channel.send(images["haachama"])
        await context.message.delete()

    @commands.command()
    async def pekora(self, context):
        await context.message.channel.send(images["pekora"])
        await context.message.delete()

    @commands.command()
    async def smug(self, context):
        await context.message.channel.send(images["smug"])
        await context.message.delete()

    @commands.command()
    async def pray(self, context):
        await context.message.channel.send(images["pray"])
        await context.message.delete()

    @commands.command()
    async def please(self, context):
        await context.message.channel.send(images["please"])
        await context.message.delete()

    @commands.command()
    async def trembling(self, context):
        await context.message.channel.send(images["trembling"])
        await context.message.delete()

async def setup(bot: commands.Bot):
    await bot.add_cog(Images(bot))
