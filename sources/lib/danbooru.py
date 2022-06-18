import discord
from .myRequests import getJsonResponse


async def send_danbooru_image(tag: str) -> discord.Embed:
    """ Sends an image from "danbooru.donmai.us" on an embed Discord message. """

    # Search whether the tag set by parameter exists
    tag_list = await getJsonResponse("https://danbooru.donmai.us/tags.json?search[name_or_alias_matches]=" + tag)

    embed = discord.Embed(colour=discord.Color.blue())

    if len(tag_list) == 0 or tag_list[0]["post_count"] == 0:
        embed.title = "Maybe you meant:"
        embed.description = await get_similar_tags(tag)

    else:
        image_url = await get_random_image(tag)
        embed.set_image(url=image_url)

    return embed


async def get_random_image(tag: str) -> str:
    """ Gets a random image. """

    image_url = None
    while image_url is None:

        post = await getJsonResponse("https://danbooru.donmai.us/posts/random.json?tags=" + tag)
        if "file_url" in post.keys():
            image_url = post["file_url"]

    return image_url


async def get_similar_tags(tag: str) -> str:
    """ Gets a list of tags that are similar to the provided one."""

    tag_list = await getJsonResponse("https://danbooru.donmai.us/tags.json"
                                     "?limit=5"
                                     "&search[hide_empty]=true"
                                     "&search[order]=count"
                                     "&search[fuzzy_name_matches]=" + tag)

    return "".join(["• " + elem["name"] + "\n" for elem in tag_list])
