import aiohttp


async def getJsonResponse(url: str):

    """ Parses an url data to JSON type. """

    content = None

    async with aiohttp.ClientSession() as session:
        async with session.get(url) as r:

            if r.status == 200:
                content = await r.json()

    return content


async def getStringResponse(url: str) -> str:

    """ Parses an url data to STRING type. """

    content = None

    async with aiohttp.ClientSession() as session:
        async with session.get(url) as r:

            if r.status == 200:
                content = await r.text()

    return content


async def postJson(_url: str, headers=None, **kwargs):

    """ Post JSON """

    if headers is None:
        headers = {}

    timeout = aiohttp.ClientTimeout(total=None, sock_connect=10, sock_read=10)
    async with aiohttp.ClientSession(timeout=timeout) as session:

        for key, value in headers.items():
            session.headers.add(key, value)

        r = await session.post(_url, json=kwargs)
        return {"status": r.status, "content": await r.json()}


