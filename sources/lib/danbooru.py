import discord
from .myRequests import getJsonResponse


async def sendDanbooruIm(tag: str) -> discord.Embed:
    tag_list = await getJsonResponse("https://danbooru.donmai.us/tags.json?search[name_or_alias_matches]=" + tag)

    embed = discord.Embed(colour=discord.Color.blue())

    if len(tag_list) != 0:
        image_url = await getRandomImage(tag)
        embed.set_image(url=image_url)

    else:
        embed.title = "Tag list:"
        embed.description = await getTagList(tag)

    return embed


# Gets a random image from danbooru
async def getRandomImage(tag: str) -> str:
    image_url = None
    while image_url is None:
        post = await getJsonResponse("https://danbooru.donmai.us/posts/random.json?tags=" + tag)
        if "file_url" in post.keys():
            image_url = post["file_url"]

    return image_url


async def getTagList(tag: str) -> str:
    tag_list = await getJsonResponse("https://danbooru.donmai.us/tags.json?search[order]=count&search["
                                     "name_or_alias_matches]=" + tag + "*")

    return "".join(["  - " + elem["name"] + "\n" for elem in tag_list])
