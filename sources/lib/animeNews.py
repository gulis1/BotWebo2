import xmltodict as xml
from datetime import datetime


from sources.lib.myRequests import getStringResponse
from itertools import takewhile

class Newsletter:

    def __init__(self):
        self.__last_time = None
        self.__source = "https://www.animenewsnetwork.com/news/atom.xml"

    async def query_news(self):

        response = await getStringResponse(self.__source)
        data = xml.parse(response)['feed']['entry']

        if self.__last_time is None:
            self.__last_time = datetime.fromisoformat(data[0]['published'][:-1])

        articles = list(takewhile(lambda x: self.__last_time < datetime.fromisoformat(x['published'][:-1]), data))

        self.__last_time = datetime.fromisoformat(data[0]['published'][:-1])
        print(f'{datetime.now()}: {len(articles)} new articles found. Last one: {self.__last_time}')
        return articles
