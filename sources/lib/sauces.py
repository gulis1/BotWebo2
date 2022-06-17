import discord
from sources.lib.myRequests import getJsonResponse
from os import getenv

api_key = getenv("SAUCENAO_KEY") # takes the TOKEN from the SAUCENAO_KEY on env.example
api_call = "https://saucenao.com/search.php?output_type=2&api_key={0}&url={1}" # API url


async def getSauce(url: str) -> discord.Embed:

    """ Gets the source of an image, using 'saucenao.com'. """

    # try to get any response for the web
    response = await getJsonResponse(api_call.format(api_key, url))
    # no response
    if response is None:
        return discord.Embed(title="Unknown error.", colour=discord.Color.lighter_gray())
    # no image send
    elif response["header"]["status"] == -3:
        return discord.Embed(title="That's not an image.", colour=discord.Color.lighter_gray())
    # gets an image
    elif response["header"]["status"] == 0:
        # gets the number of results
        filtered_sauces = list(filter(lambda x: float(x["header"]["similarity"]) > 65, response["results"]))
        # no results
        if len(filtered_sauces) == 0:
            return discord.Embed(title="No relevant results found.", colour=discord.Color.lighter_gray())
        # returns a list of the results got
        else:

            embed = discord.Embed(title="Sources:", colour=discord.Color.lighter_gray())

            for ind, sauce in enumerate(filtered_sauces):
                keys = sauce["data"].keys()
                msg = ""
                for tag in keys:

                    if type(sauce["data"][tag]) == list:
                        msg += tag + ": " + str(sauce["data"][tag][0]) + "\n"

                    else:
                        msg += tag + ": " + str(sauce["data"][tag]) + "\n"

                embed.add_field(name=str(ind + 1) + ")", value=msg, inline=False)

            return embed
