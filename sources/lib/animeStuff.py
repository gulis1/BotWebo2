from .myRequests import postJson
import discord
from datetime import timedelta


async def timeUntilAiring(title: str) -> discord.Embed:
    url = 'https://graphql.anilist.co'

    query = '''
    query($name: String) {
    Media (search: $name, type: ANIME) {
    episodes
    status(version: 2)
    season
    seasonYear
    nextAiringEpisode{
        timeUntilAiring
        episode
    }
    title {
    romaji
    }

    }
    }
    '''

    variables = {
        'name': title
    }

    res = await postJson(url, query=query, variables=variables)

    if res is None:
        return discord.Embed(colour=discord.Color.dark_teal(), title="An error has occurred.")

    else:
        embed = discord.Embed(colour=discord.Color.dark_teal())

        if res["status"] == 404:
            embed.title = f'Could not find show "{title}"'

        else:
            anime_info = res["content"]["data"]["Media"]
            embed.title = anime_info["title"]["romaji"]

            if anime_info["status"] == "FINISHED":
                embed.description = "Show has **already ended.** ({0} episodes)".format(
                    anime_info["episodes"])

            if anime_info["nextAiringEpisode"] is not None:
                time = timedelta(seconds=anime_info["nextAiringEpisode"]["timeUntilAiring"])
                embed.description = "Episode **{0}** airs in **{1}**".format(
                    anime_info["nextAiringEpisode"]["episode"], time)

            elif anime_info["status"] == "NOT_YET_RELEASED":

                if anime_info["seasonYear"] is not None:
                    embed.description = "Airing in **" + str(anime_info["seasonYear"])
                    if anime_info["seasonYear"] is not None:
                        embed.description += ", " + anime_info["season"]
                    embed.description += "**"

                else:
                    embed.description = "Unknown release date"

        return embed
