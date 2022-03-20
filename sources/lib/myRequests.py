import aiohttp


async def getJsonResponse(url: str):
    content = None

    async with aiohttp.ClientSession() as session:
        async with session.get(url) as r:

            if r.status == 200:
                content = await r.json()

    return content


async def getStringResponse(url: str) -> str:
    content = None

    async with aiohttp.ClientSession() as session:
        async with session.get(url) as r:

            if r.status == 200:
                content = await r.text()

    return content


async def postJson(url: str, headers=None, **kwargs):

    if headers is None:
        headers = {}

    content = None
    async with aiohttp.ClientSession() as session:

        for key, value in headers.items():
            session.headers.add(key, value)

        r = await session.post(url, json=kwargs['body'])
        return {"status": r.status, "content": await r.json()}


