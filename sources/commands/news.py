import discord
from discord.ext import commands, tasks
from sources.lib.animeNews import Newsletter


class News(commands.Cog):

    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.__newsletter = Newsletter()
        self.query_news.start()

    @tasks.loop(minutes=20)
    async def query_news(self):

        news = await self.__newsletter.query_news()
        anime_news = []
        manga_news = []

        for article in news:

            try:
                categories = article['category']
                if type(categories) != list and 'link' in article.keys():
                    categories = [categories]

                for cat in categories:
                    if cat['@term'] == 'Anime' and 'link' in article.keys():
                        anime_news.append(article)

                    elif cat['@term'] == 'Manga' and 'link' in article.keys():
                        manga_news.append(article)

            except KeyError:
                pass

        anime_news = [x['link']['@href'] for x in anime_news if 'link' in x.keys()]
        manga_news = [x['link']['@href'] for x in manga_news if 'link' in x.keys()]

        for guild in self.bot.guilds:
            anime_channel = discord.utils.get(guild.channels, name='anime-webonews')
            manga_channel = discord.utils.get(guild.channels, name='manga-webonews')

            if anime_channel:
                for article in anime_news:
                    await anime_channel.send(article)

            if manga_channel:
                for article in manga_news:
                    await manga_channel.send(article)

    @query_news.before_loop
    async def wait(self):
        await self.bot.wait_until_ready()


def setup(bot: commands.Bot):
    bot.add_cog(News(bot))
