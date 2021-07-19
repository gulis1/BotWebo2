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


async def postJson(url: str, **kwargs):
    content = None

    async with aiohttp.ClientSession() as session:
        r = await session.post(url, json=kwargs)
        return {"status": r.status, "content": await r.json()}


