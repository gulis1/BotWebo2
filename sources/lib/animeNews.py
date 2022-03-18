import xmltodict as xml
from datetime import datetime
from sources.lib.myRequests import getStringResponse
from itertools import takewhile


class Newsletter:

    def __init__(self):
        self.__last_time = datetime.utcnow()
        self.__source = "https://www.animenewsnetwork.com/all/atom.xml"

    async def query_news(self):
        response = await getStringResponse(self.__source)
        data = xml.parse(response)['feed']['entry']

        articles = list(takewhile(lambda x: self.__last_time < datetime.fromisoformat(x['published'][:-1]), data))

        print(f'{datetime.now()}: {len(articles)} new articles.')
        return articles
