from discord.ext import commands
import discord
from sources.lib.music import getGuildInstance
from sources.lib.decorators import userConnectedToGuildVoice, botIsConnectedToGuildVoice
import re


class Music(commands.Cog):

    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.guild_only()
    @commands.check(userConnectedToGuildVoice)
    @commands.check(botIsConnectedToGuildVoice)
    @commands.command()
    async def empty(self, context):

        guild_instance = getGuildInstance(context.message.guild.id)
        guild_instance.textChannel = context.message.channel

        guild_instance.emptyPlaylist()

        await guild_instance.textChannel.send(
            embed=discord.Embed(title="The playlist has been emptied.", color=discord.Color.green()))
        await context.message.delete()

    @commands.guild_only()
    @commands.check(userConnectedToGuildVoice)
    @commands.check(botIsConnectedToGuildVoice)
    @commands.command()
    async def loop(self, context, msg):

        guild_instance = getGuildInstance(context.message.guild.id)
        guild_instance.textChannel = context.message.channel

        if msg == "off":
            guild_instance.loop = 0
            await context.message.channel.send(
                embed=discord.Embed(title="Loop set to off", color=discord.Color.green()))

        elif msg == "single":
            guild_instance.loop = 1
            #guild_instance.playlist.append(guild_instance.currentSong)
            await context.message.channel.send(
                embed=discord.Embed(title="Loop set to single", color=discord.Color.green()))

        elif msg == "all":
            guild_instance.loop = 2
            await context.message.channel.send(
                embed=discord.Embed(title="Loop set to all", color=discord.Color.green()))

        await context.message.delete()

    @commands.guild_only()
    @commands.check(userConnectedToGuildVoice)
    @commands.command()
    async def play(self, context, url):

        guild_instance = getGuildInstance(context.message.guild.id)
        guild_instance.textChannel = context.message.channel

        if guild_instance.random == True:
            await guild_instance.textChannel.send(
                embed=discord.Embed(title="Stop random with ;rstop first", color=discord.Color.red()))
            return

        if url.startswith("http"):
            yt_playlist = re.search("(youtube.com|youtu.be)(\/playlist\?list=)([a-zA-Z0-9\-\_]+)", url)
            yt_video = re.search("(youtu\.be\/|v\/|u\/\w\/|embed\/|watch\?v=|\&v=)([^#\&\?]*)", url)

            spotify_playlist = re.search("(https:\/\/open.spotify.com)(\/user\/spotify\/playlist\/|\/playlist\/)(\w+)",
                                         url)
            spotify_album = re.search("(https:\/\/open.spotify.com)(\/user\/spotify\/playlist\/|\/album\/)(\w+)", url)

            if yt_playlist is not None:
                await guild_instance.getYoutubePlaylist(yt_playlist[3])

            elif yt_video is not None:
                await guild_instance.addVideoToPlaylist(yt_video[2])

            elif spotify_playlist is not None:
                await guild_instance.getSpotifyPlaylist(spotify_playlist[3])

            elif spotify_album is not None:
                await guild_instance.getSpotifyAlbum(spotify_album[3])

            else:
                await guild_instance.textChannel.send(
                    embed=discord.Embed(title="Wrong URL", colour=discord.Color.red()))
                return

        elif url.isnumeric():
            await guild_instance.addToPlaylistFromSearchList(int(url) - 1)

        elif url is None:
            await guild_instance.textChannel.send(
                embed=discord.Embed(title="need a parameter", colour=discord.Color.red()))
        else:
            await guild_instance.youtubeSearch(context.message.content[5:])
            await context.message.delete()
            return

        await context.message.delete()
        await guild_instance.player(context.message.author.voice.channel)


    @commands.guild_only()
    @commands.check(userConnectedToGuildVoice)
    @commands.check(botIsConnectedToGuildVoice)
    @commands.command()
    async def playlist(self, context):

        guild_instance = getGuildInstance(context.message.guild.id)
        guild_instance.textChannel = context.message.channel

        if guild_instance.loop == 0:
            loop = "off"

        elif guild_instance.loop == 1:
            loop = "single"

        else:
            loop = "all"

        if guild_instance.currentSong is not None:
            text = f"• **Actual:** {guild_instance.currentSong.title} \n• **Loop:** {loop}\n \n"
        else:
            text = ""

        for num, video in enumerate(guild_instance.playlist):
            text += '**' + str(num + 1) + ")  " + '**' + video.title + "\n \n"

        embed = discord.Embed(title="Playlist:", description=text, colour=discord.Color.green())
        await guild_instance.textChannel.send(embed=embed)
        await context.message.delete()

    @commands.guild_only()
    @commands.check(userConnectedToGuildVoice)
    @commands.check(botIsConnectedToGuildVoice)
    @commands.command()
    async def remove(self, context, ind: int):

        guild_instance = getGuildInstance(context.message.guild.id)
        guild_instance.textChannel = context.message.channel

        try:
            ind = int(ind) - 1
            await guild_instance.remove(ind)

        except ValueError:
            await guild_instance.textChannelsend(
                embed=discord.Embed(title="Index out of range", color=discord.Color.green()))

        await context.message.delete()

    @commands.guild_only()
    @commands.check(userConnectedToGuildVoice)
    @commands.check(botIsConnectedToGuildVoice)
    @commands.cooldown(1, 30, commands.BucketType.guild)
    @commands.command()
    async def shuffle(self, context):

        guild_instance = getGuildInstance(context.message.guild.id, create_if_missing=False)
        await guild_instance.shuffleList()

        await context.message.delete()

    @shuffle.error
    async def shuffle_error(self, ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            await ctx.send(
                embed=discord.Embed(title=f'Please wait {round(error.retry_after)}s before shuffling again.', color=discord.Color.red()))
            await ctx.message.delete()
        else:
            raise error

    @commands.guild_only()
    @commands.check(userConnectedToGuildVoice)
    @commands.check(botIsConnectedToGuildVoice)
    @commands.command()
    async def skip(self, context, ind=None):

        guild_instance = getGuildInstance(context.message.guild.id)
        guild_instance.textChannel = context.message.channel

        if ind is None:
            await guild_instance.skip()

        else:
            try:
                ind = int(ind) - 1
                await guild_instance.skip(ind)

            except ValueError:
                await guild_instance.textChannel.send(
                    embed=discord.Embed(title="Index out of range", color=discord.Color.green()))

        await context.message.delete()

    @commands.guild_only()
    @commands.check(userConnectedToGuildVoice)
    @commands.check(botIsConnectedToGuildVoice)
    @commands.command()
    async def song(self, context):

        guild_instance = getGuildInstance(context.message.guild.id)
        guild_instance.textChannel = context.message.channel

        embed = discord.Embed(colour=discord.Color.green())

        if guild_instance.voiceClient is not None and guild_instance.voiceClient.is_playing():
            msg = "------------------------------"
            if guild_instance.currentSong is not None:
                ind = round(len(msg) * (guild_instance.currentSong.perCentPlayed()))

                msg = msg[:ind] + "**|**" + msg[ind + 1:]
                embed.title = guild_instance.currentSong.title
                embed.description = msg
            else:
                embed.title = guild_instance.randomSong + " " + guild_instance.randomSongSlug
                embed.set_image(url=guild_instance.randomSongImage)
        else:
            embed.title = "No song is playing."

        await guild_instance.textChannel.send(embed=embed)
        await context.message.delete()

    @commands.guild_only()
    @commands.check(userConnectedToGuildVoice)
    @commands.command()
    async def rload(self, context, username=None):

        guild_instance = getGuildInstance(context.message.guild.id)
        guild_instance.textChannel = context.message.channel

        if username is not None:
            try:
                await guild_instance.getAnilistData(username)
            except Exception as e:
                await guild_instance.textChannel.send(embed=discord.Embed(title=str(e),color=discord.Color.red()))
                await context.message.delete()
                return
        else:
            await guild_instance.textChannel.send(
                embed=discord.Embed(title="needs AniList username: ;rload [username].", color=discord.Color.red()))
            await context.message.delete()
            return
        await guild_instance.textChannel.send(embed=discord.Embed(title=f"{username}'s list loaded", color=discord.Color.green()))
        await context.message.delete()

    @commands.guild_only()
    @commands.check(userConnectedToGuildVoice)
    @commands.command()
    async def rplay(self,context):
        guild_instance = getGuildInstance(context.message.guild.id)
        guild_instance.textChannel = context.message.channel
        try:
            await guild_instance.randomThemePlayer(context.message.author.voice.channel)
        except Exception as e:
            await guild_instance.textChannel.send(embed=discord.Embed(title=str(e), color=discord.Color.red()))
            await context.message.delete()

    @commands.guild_only()
    @commands.check(userConnectedToGuildVoice)
    @commands.check(botIsConnectedToGuildVoice)
    @commands.command()
    async def rstop(self,context):
        guild_instance = getGuildInstance(context.message.guild.id)
        guild_instance.textChannel = context.message.channel

        await guild_instance.stopRandomTheme()

    @commands.guild_only()
    @commands.check(userConnectedToGuildVoice)
    @commands.command()
    async def ruser(self,context):

        guild_instance = getGuildInstance(context.message.guild.id)
        guild_instance.textChannel = context.message.channel
        try:
            await guild_instance.checkListUser()
        except Exception as e:
            await guild_instance.textChannel.send(embed=discord.Embed(title=str(e), color=discord.Color.red()))
        await context.message.delete()

def setup(bot: commands.Bot):
    bot.add_cog(Music(bot))
