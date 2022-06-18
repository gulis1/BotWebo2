import discord
from discord.ext import commands, tasks
from sources.lib.animeNews import Newsletter

# where the news are sent, you can change for your own channel or you must have it 
ANIME_CHANNEL = "anime-webonews"
MANGA_CHANNEL = "manga-webonews"

class News(commands.Cog):

    """ Gets the anime news from https://www.animenewsnetwork.com """

    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.__newsletter = Newsletter()
        self.query_news.start()

    @tasks.loop(minutes=20) # every 20min search for new info
    async def query_news(self):
        """ Gets the info and sends the """
        # parses from an XML file
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

        # Removes unnecessary parts of the URL.
        def shorten(link: str): return "https://www.animenewsnetwork.com/" + link.split('/')[-1]

        anime_news = [shorten(x['link']['@href']) for x in anime_news if 'link' in x.keys()]
        manga_news = [shorten(x['link']['@href']) for x in manga_news if 'link' in x.keys()]

        for guild in self.bot.guilds:
            anime_channel = discord.utils.get(guild.channels, name=ANIME_CHANNEL)
            manga_channel = discord.utils.get(guild.channels, name=MANGA_CHANNEL)

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
