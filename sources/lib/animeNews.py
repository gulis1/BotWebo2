import xmltodict as xml
from datetime import datetime
from sources.lib.myRequests import getStringResponse
from itertools import takewhile


class Newsletter:

    """ This class is used to send almost real time anime/manga news using "www.animenewsnetwork.com". """

    def __init__(self):
        self.__last_time = None
        self.__source = "https://www.animenewsnetwork.com/news/atom.xml"

    async def query_news(self):

        # parses XML source file
        response = await getStringResponse(self.__source)
        data = xml.parse(response)['feed']['entry']

        if self.__last_time is None:
            self.__last_time = datetime.fromisoformat(data[0]['published'][:-1])

        # Gets all articles from now and 15min ago
        articles = list(takewhile(lambda x: self.__last_time < datetime.fromisoformat(x['published'][:-1]), data))

        # parses the info of every article to send it more clearly
        # Shorten url if api token is available.
        
        if self.__last_time is not None:
            self.__last_time = datetime.fromisoformat(data[0]['published'][:-1])
        articles = list(takewhile(lambda x: self.__last_time < datetime.fromisoformat(x['published'][:-1]), data))

        self.__last_time = datetime.fromisoformat(data[0]['published'][:-1])
        print(f'{datetime.now()}: {len(articles)} new articles found. Last one: {self.__last_time}')
        return articles
