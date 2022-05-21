import xmltodict as xml
from datetime import datetime

from aiohttp import ClientError

from sources.lib.myRequests import getStringResponse, postJson
from itertools import takewhile
from os import getenv

tiny_token = getenv('TINY_URL')


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

        # Shorten url if api token is available.
        try:
            if tiny_token is not None:

                for article in articles:
                    link = article['link']['@href']
                    response = await postJson('https://api.tinyurl.com/create', headers={'Authorization': f'Bearer {tiny_token}'}, url=link)

                    if response['status'] != 200:
                        print('Error with tiny-url api')
                        break
                    else:
                        article['link']['@href'] = response['content']['data']['tiny_url']

        except ClientError:
            print("Unknown error occurred during url shortening.")

        self.__last_time = datetime.fromisoformat(data[0]['published'][:-1])
        print(f'{datetime.now()}: {len(articles)} new articles found. Last one: {self.__last_time}')
        return articles
