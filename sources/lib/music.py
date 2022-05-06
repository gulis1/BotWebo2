from random import shuffle
from time import time
from os import getenv
from asyncio import sleep, get_event_loop
from os import remove
import yt_dlp
from spotify import HTTPClient
import discord

from sources.lib.myRequests import getJsonResponse

yt_key = getenv("YT_KEY")
spotifyClientId = getenv("SPOTIFY_ID")
spotifySecretId = getenv("SPOTIFY_SECRET")

spotifyClient = HTTPClient(spotifyClientId, spotifySecretId)

MAX_SONGS = 30
MAX_VIDEO_DURATION = 900

COLOR_RED = discord.Color.red()
COLOR_GREEN = discord.Color.green()


class Video:

    def __init__(self, video_id: str, title: str, duration: int = None):
        self.id = video_id
        self.title = title
        self.duration = duration
        self.startTime = None

    def perCentPlayed(self):
        return (time() - self.startTime) / self.duration if self.duration != 0 else 0


class GuildInstance:

    def __init__(self, guild_id: int):
        self.guild_id = guild_id
        self.textChannel = None
        self.voiceClient: discord.VoiceClient or None = None
        self.playlist = []
        self.searchResults = []
        self.loop: int = 0
        self.currentSong: Video or None = None
        self.data = {"playlist_id": "", "nextPageToken": ""}

    def emptyPlaylist(self):

        self.playlist = []

        self.data["playlist_id"] = ""
        self.data["nextPageToken"] = ""

    async def shuffleList(self):

        shuffle(self.playlist)
        await self.textChannel.send(embed=discord.Embed(title="Playlist shuffled.", color=COLOR_GREEN))

    async def disconnect(self) -> None:

        self.loop = 0
        self.playlist.clear()
        self.currentSong = None

        await self.voiceClient.disconnect(force=True)
        self.voiceClient = None

        try:
            remove("serverAudio/" + str(self.guild_id) + ".mp3")
        except FileNotFoundError:
            pass

    async def addVideoToPlaylist(self, url: str) -> None:
        r = await getJsonResponse(
            f"https://www.googleapis.com/youtube/v3/videos?key={yt_key}&part=snippet, contentDetails&id={url}")

        if r is not None:

            if len(self.playlist) < MAX_SONGS:
                self.playlist.append(Video(r["items"][0]["id"], r["items"][0]["snippet"]["title"]))
                await self.textChannel.send(embed = discord.Embed(title=f'Added "{r["items"][0]["snippet"]["title"]}" to the playlist', color=COLOR_GREEN))

            else:
                await self.textChannel.send(embed=discord.Embed(title='The playlist is full already.', colour=COLOR_RED))

        else:
            await self.textChannel.send(embed=discord.Embed(title='Wrong url.', colour=COLOR_RED))

    async def addToPlaylistFromSearchList(self, ind: int) -> None:

        try:
            self.playlist.append(self.searchResults[ind])
            await self.textChannel.send(embed=discord.Embed(title="Song added to the playlist", colour=COLOR_GREEN))

        except IndexError:
            await self.textChannel.send("Index out of range.")

    async def getYoutubePlaylist(self, playlist_id: str) -> None:

        self.data["playlist_id"] = playlist_id


        results = await getJsonResponse(
            f"https://www.googleapis.com/youtube/v3/playlistItems?pageToken={self.data['nextPageToken']}&key={yt_key}&part=snippet,contentDetails&maxResults=30&playlistId={self.data['playlist_id']}")
        video_list = [Video(vid["snippet"]["resourceId"]["videoId"], vid["snippet"]["title"]) for vid in
                      results["items"] if vid["snippet"]["title"] != 'Deleted video' and vid["snippet"]["title"] != 'Private video']

        cont = 0
        for video in video_list:
            self.playlist.append(video)
            cont += 1
            if len(self.playlist) >= 30:
                break
        try:
            self.data["nextPageToken"] = results["nextPageToken"]
        except KeyError:
            self.data["nextPageToken"] = ""

        await self.textChannel.send(embed=discord.Embed(title=f"{cont} song(s) where added to the playlist.", colour=COLOR_GREEN))

    async def findYoutubeEquivalent(self):

        results = await getJsonResponse(
            f"https://www.googleapis.com/youtube/v3/search?key={yt_key}&part=snippet&type=video&q={self.currentSong.title}")

        try:
            self.currentSong.id = results["items"][0]["id"]["videoId"]

        except IndexError:
            await self.textChannel.send(embed=discord.Embed(title=f'Could not find a youtube video for song {self.currentSong.title}', colour=COLOR_RED))

    async def youtubeSearch(self, string: str) -> None:

        results = await getJsonResponse(
            f"https://www.googleapis.com/youtube/v3/search?key={yt_key}&part=snippet&type=video&q={string}")

        if results is None:
            await self.textChannel.send(embed=discord.Embed(title="An error has occurred.", colour=COLOR_RED))

        elif len(results["items"]) == 0:
            await self.textChannel.send(embed=discord.Embed(title="No results.", colour=COLOR_GREEN))

        else:
            self.searchResults.clear()

            for num, vid in enumerate(results["items"]):

                embed = discord.Embed(title=str(num + 1) + ") " + vid["snippet"]["title"], colour=COLOR_GREEN)
                embed.set_image(url=vid["snippet"]["thumbnails"]["default"]["url"])
                await self.textChannel.send(embed=embed)

                self.searchResults.append(Video(vid["id"]["videoId"], vid["snippet"]["title"]))

    async def getYoutubeVidDuration(self) -> None:

        r = await getJsonResponse(
            f"https://www.googleapis.com/youtube/v3/videos?key={yt_key}&part=contentDetails&id={self.currentSong.id}")

        self.currentSong.duration = convertTime(r["items"][0]["contentDetails"]["duration"]) if r is not None else 0

    async def getSpotifyAlbum(self, albumID: str) -> None:

        album = await spotifyClient.album(albumID)
        lista = album["tracks"]["items"]

        cont = 0
        for song in album["tracks"]["items"]:

            self.playlist.append(Video(None, song["name"] + " " + song["artists"][0]["name"]))
            cont += 1
            if len(self.playlist) >= 30:
                break

        await self.textChannel.send(embed=discord.Embed(title=f"{cont} song(s) where added to the playlist.", colour=COLOR_GREEN))

    async def getSpotifyPlaylist(self, playlist_id: str) -> None:

        playlist = await spotifyClient.get_playlist(playlist_id)

        lista = playlist["tracks"]["items"]

        cont = 0
        for song in playlist["tracks"]["items"]:

            self.playlist.append(Video(None, song["track"]["name"] + " " + song["track"]["artists"][0]["name"]))
            cont += 1
            if len(self.playlist) >= 30:
                break

        await self.textChannel.send(embed=discord.Embed(title=f"{cont} song(s) where added to the playlist.", colour=COLOR_GREEN))

    async def player(self, voice_channel: discord.VoiceChannel) -> None:

        try:
            self.voiceClient = await voice_channel.connect()

        except discord.ClientException:
            return

        reason = None
        while reason is None:

            if self.voiceClient is None:
                reason = "Leave command."

            else:

                if not self.voiceClient.is_connected():
                    reason = "I got kicked :cry:"

                elif len(self.voiceClient.channel.members) == 1:
                    reason = "Channel is empty."

                elif not self.voiceClient.is_playing():

                    if len(self.playlist) > 0 or self.loop == 1:
                        await self.playSong()

                    elif self.data["nextPageToken"] != "":
                        await self.getYoutubePlaylist(self.data["playlist_id"])
                    else:
                        reason = "Playlist is empty."

            await sleep(3)

        await self.disconnect()
        await self.textChannel.send(embed=discord.Embed(title=f"Leaving the channel: {reason}", colour=discord.Color.green()))


    async def playSong(self) -> None:
        global MAX_VIDEO_DURATION

        # Changes current song info if loop != single
        if self.loop != 1:

            # Adds ended song to the end of the playlist if loop == all
            if self.loop == 2:
                self.playlist.append(self.currentSong)

            if len(self.playlist) > 0:
                self.currentSong = self.playlist[0]
                self.playlist.pop(0)

            else:
                self.currentSong = None
                return


            # If the song has no id (Most likely becasue it comes from a spotify playlist), here a yt video will be found for that song
        if self.currentSong.id is None:
            await self.findYoutubeEquivalent()

        await self.getYoutubeVidDuration()

        # Skips videos that are too long.
        if self.currentSong.duration > MAX_VIDEO_DURATION:
            await self.textChannel.send(f"Skipped {self.currentSong.title} because it was too long.")
            return

        path = f"serverAudio/{self.guild_id}.mp3"
        # Downloads the song if loop is not on single.
        if self.loop != 1:

            try:
                remove(path)
            except FileNotFoundError:
                pass

            loop = get_event_loop()
            await loop.run_in_executor(None, downloadSong, self.currentSong.id, path)

        try:
            self.voiceClient.play(discord.FFmpegPCMAudio(path))
            self.currentSong.startTime = time()
        except FileNotFoundError:
            self.textChannel.send(embed=discord.Embed(title="Could not download video", colour=COLOR_RED))

    async def skip(self, ind: int = None) -> None:

        if self.loop == 1:
            self.loop = 0

        if ind is not None:

            try:
                ind = int(ind)

                self.playlist.insert(0, self.playlist[ind])
                self.playlist.pop(ind + 1)

            except IndexError:
                await self.textChannel.send(
                    embed=discord.Embed(title="Index out of range", color=COLOR_RED))

        self.voiceClient.stop()
        await self.textChannel.send(embed=discord.Embed(title="Song skipped", color=COLOR_RED))

    async def remove(self, ind: int) -> None:

        try:
            title = self.playlist[ind].title
            self.playlist.pop(ind)
            embed = embed = discord.Embed(title=f'Song  "{title}" has been removed from the playlist.', colour=COLOR_GREEN)
            await self.textChannel.send(embed=embed)

        except IndexError:
            await self.textChannel.send(
                embed=discord.Embed(title="Index out of range", color=COLOR_RED))


guilds = {}


def getGuildInstance(guild_id: int, create_if_missing: bool = True) -> GuildInstance or None:
    global guilds

    if guild_id in guilds:
        return guilds.get(guild_id)

    elif create_if_missing:
        guild = GuildInstance(guild_id)
        guilds[guild_id] = guild
        return guild

    else:
        return None


def downloadSong(videoId: str, path: str) -> None:
    url = "https://www.youtube.com/watch?v={0}".format(videoId)

    ydl_opts = {'format': 'bestaudio/best', 'quiet': False, 'noplaylist': True, "outtmpl": path}

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])  # Download into the current working directory


def convertTime(string: str) -> int:
    n = ""
    H = 0
    M = 0
    S = 0

    for x in string:

        if x.isnumeric():
            n += x

        elif x == "H":
            H = int(n)
            n = ""

        elif x == "M":
            M = int(n)
            n = ""

        elif x == "S":
            S = int(n)
            n = ""

    return H * 3600 + M * 60 + S
