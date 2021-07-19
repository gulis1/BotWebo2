import discord
from sources.lib.music import getGuildInstance


async def userConnectedToGuildVoice(context):
    server_id = context.message.guild.id

    if context.message.author.voice is not None and context.message.author.voice.channel.guild.id == server_id:
        return True

    else:
        embed = discord.Embed(title="You need to be in a voice channel of this server.", colour=discord.Color.red())
        await context.message.channel.send(embed=embed)
        return False


async def botIsConnectedToGuildVoice(context):
    server_id = context.message.guild.id
    guild_instance = getGuildInstance(server_id, create_if_missing=False)

    if guild_instance is None or guild_instance.voiceClient is None:
        embed = discord.Embed(title="I'm not connected yet.", colour=discord.Color.red())
        await context.message.channel.send(embed=embed)
        return False

    else:
        return True
