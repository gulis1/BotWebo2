import discord
from .myRequests import getJsonResponse


async def sendDanbooruIm(tag: str) -> discord.Embed:

    """ Sends an image from "danbooru.donmai.us" on an embed Discord message. """

    # Search wether or not the tag set by parameter exists
    tag_list = await getJsonResponse("https://danbooru.donmai.us/tags.json?search[name_or_alias_matches]=" + tag)

    embed = discord.Embed(colour=discord.Color.blue())

    # If no tag sends random image
    if len(tag_list) != 0:
        image_url = await getRandomImage(tag)
        embed.set_image(url=image_url)

    else:
        embed.title = "Tag list:"
        embed.description = await getTagList(tag)

    return embed


async def getRandomImage(tag: str) -> str:

    """ Gets a random image. """

    image_url = None
    while image_url is None:
        # Gets and parses a random image
        post = await getJsonResponse("https://danbooru.donmai.us/posts/random.json?tags=" + tag)
        if "file_url" in post.keys():
            image_url = post["file_url"]

    return image_url


async def getTagList(tag: str) -> str:

    """ Gets a random image from the tag provided. """

    # Gets and parses a random image from the tag provided
    tag_list = await getJsonResponse("https://danbooru.donmai.us/tags.json?search[order]=count&search["
                                     "name_or_alias_matches]=" + tag + "*")

    return "".join(["  - " + elem["name"] + "\n" for elem in tag_list])
