#!/usr/bin/python3 -u
import asyncio

from discord.ext import commands
from discord import Intents
from dotenv import load_dotenv, find_dotenv
from os import getenv

intents = Intents.default()
intents.members = True
intents.message_content = True
COMMAND_PREFIX = ";" # The COMMAND_PREFIX
bot = commands.Bot(command_prefix=COMMAND_PREFIX, intents=intents)


@bot.event
async def on_ready():

    """ What the bot do when its ready to work """

    print('Ready')


async def main():

    """ main method """

    load_dotenv(find_dotenv())
    discord_token = getenv("DISCORD_TOKEN") # takes the TOKEN from the DISCORD_TOKEN on env.example

    await bot.load_extension("sources.commands")
    await bot.start(discord_token)



if __name__ == "__main__":
   asyncio.run(main())
