# A Discord Bot

## Commands
* [help command](#help)
* [music commands](#music)
* [danbooru commands](#danbooru)
* [sauce commands](#sauce)
* [anilits commands](#anilist)
---
## Features
* [anime/manga news](#news)
* [emotes](#emotes)
* [pekofy](#peko)
---
<h3 id="help" style="text-decoration: underline">Help command</h3>
Shows information about the commands supported by the bot.
<br>

[See more...](sources/commands/misc.py)

<h3 id="music"> Music commands </h3>
Supports searching by name, YouTube videos and playlist, and Spotify albums and playlists.

* [**play** <url/name/number>](sources/commands/music.py)
* [**playlist**](sources/commands/music.py)                    _Shows current playlist._
* [**loop** <off/single/all>](sources/commands/music.py)       _Changes current loop settings._
* [**skip** number](sources/commands/music.py)                 _If no number is provided, skips to the next song._
* [**song**](sources/commands/music.py)                        _Displays info about the current song._
* [**empty**](sources/commands/music.py)                       _Removes all songs from the playlist._
* [**remove** number](sources/commands/music.py)               _Removes specific song from the playlist._
* [**shuffle**](sources/commands/music.py)                     _Shuffles the playlist._
<br>
[See more...](sources/lib/music.py)

<h3 id="danbooru">Danbooru commands</h3>

* [**danbooru** tags](sources/commands/danbooru.py)          _Sends a random image from danbooru with the specified tag._
<br>
[See more...](sources/lib/danbooru.py)
<h3 id="sauce"> Saucenao commands</h3>

* [**sauce** url](sources/commands/sauces.py)              _Finds the source for the image in the url._
<br>
[See more...](sources/lib/sauces.py)
<br>
If an image is attached to a message, the search will be done fot that image.

<h3 id="anilist"> Anilist commands</h3>

* [**anime** name](sources/commands/anime.py)       _Gets the remaining time until the next episode of the specified anime._
<br>
[See more...](sources/lib/animeStuff.py)
---
<h3 id="news">Anime news</h3>

First you must have 2 discord channels called "anime-webonews" and "manga-webonews" or change the channels name in [news.py](sources/commands/news.py)'s header, called _ANIME_CHANNEL_ and _MANGA_CHANNEL_.

Then, every 20 mins the bot will send the most recent anime news.

Created using the [animenewsnetwork.com](https://www.animenewsnetwork.com) newsfeed.

[File here](https://www.animenewsnetwork.com/news/atom.xml)

<h3 id="emotes">Emotes</h3>

The bot will send an image related to the text, try it yourself
* yes
* no
* pray
* please
* smug
* trembling
* pekora
* haacham
<br>
[See more...](sources/commands/images.py)

<h3 id="peko">Pekofy</h3>

Pekofies the text replied to:
> This is an example

to:
> This is an example peko
<br>

[See more...](sources/commands/misc.py)