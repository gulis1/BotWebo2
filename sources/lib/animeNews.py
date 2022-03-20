import xmltodict as xml
from datetime import datetime
from sources.lib.myRequests import getStringResponse, postJson
from itertools import takewhile
from os import getenv

tiny_token = getenv('TINY_URL')

class Newsletter:

    def __init__(self):
        self.__last_time = datetime.utcnow()
        self.__source = "https://www.animenewsnetwork.com/all/atom.xml"

    async def query_news(self):

        response = await getStringResponse(self.__source)
        data = xml.parse(response)['feed']['entry']

        articles = list(takewhile(lambda x: self.__last_time < datetime.fromisoformat(x['published'][:-1]), data))

        # Shorten retrieved article's links.
        for article in articles:
            link = article['link']['@href']
            response = await postJson('https://api.tinyurl.com/create', headers={'Authorization': f'Bearer {tiny_token}'}, body={'url': link})

            if response['status'] != 200:
                print('Error with tiny-url api')
            else:
                article['link']['@href'] = response['content']['data']['tiny_url']

        self.__last_time = datetime.utcnow()
        print(f'{datetime.now()}: {len(articles)} new articles.')
        return articles
