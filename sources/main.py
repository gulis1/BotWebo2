#!/usr/bin/python3 -u
from discord.ext import commands
from discord import Intents
from dotenv import load_dotenv, find_dotenv
from os import getenv

intents = Intents.default()
intents.members = True
COMMAND_PREFIX = ";" # The COMMAND_PREFIX
bot = commands.Bot(COMMAND_PREFIX, intents=intents)


@bot.event
async def on_ready():

    """ What the bot do when its ready to work """

    print('Ready')


def main():

    """ main method """

    load_dotenv(find_dotenv())
    discord_token = getenv("DISCORD_TOKEN") # takes the TOKEN from the DISCORD_TOKEN on env.example

    bot.load_extension("sources.commands")
    bot.run(discord_token)


if __name__ == "__main__":
    main()
