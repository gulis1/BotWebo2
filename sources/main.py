#!/usr/bin/python3 -u
from discord.ext import commands
from discord import Intents
from dotenv import load_dotenv, find_dotenv
from os import getenv

intents = Intents.default()
intents.members = True
bot = commands.Bot("!", intents=intents)


@bot.event
async def on_ready():
    print('Ready')


def main():
    load_dotenv(find_dotenv())
    discord_token = getenv("DISCORD_TOKEN")

    bot.load_extension("sources.commands")
    bot.run(discord_token)


if __name__ == "__main__":
    main()
