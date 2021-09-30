import threading

import discord
import os
import asyncio
import youtube_dl
from discord.ext import commands
from urllib.parse import urlparse
from async_timeout import timeout
import typing


class Player(commands.Cog):
    """ The player cog that handles everything regarding playing something over a voice channel """

    def __init__(self, bot):
        self.bot: discord.client = bot
        self.configuration = bot.get_cog("Configuration")
        self.volume: float = .5
        self.queue: asyncio.PriorityQueue = asyncio.PriorityQueue()
        self.context_list: [commands.Context] = []
        self.current_context: typing.Optional[commands.Context] = None
        self.current_song: typing.Optional[typing.Union[YTDLSource, MP3Source]] = None
        self.next: asyncio.Event = asyncio.Event()
        self.bot.loop.create_task(self.audio_player_task())
        self._is_paused : bool = False

        # Magic values right now. Should be set to something else. Just this for now while testing.
        self.mp3_priority: int = 10000
        self.yt_priority: int = 100000

    @commands.Cog.listener()
    async def on_ready(self):
        print("Player cog is loaded")

    # Prøv at gøre så vi kune prøver get inde i try og så resten af logikken derude efter. Tror måske det kan løse lidt.
    async def audio_player_task(self) -> None:
        """ A infinite loop that handles actually playing the next song in the queue """
        while True:
            current_song = await self.queue.get()
            current_song = current_song[1]
            self.current_song = current_song
            ctx = self.context_list.pop(0)
            self.current_context = ctx
            async with ctx.typing():
                ctx.voice_client.play(current_song.source)
                await ctx.send(embed=current_song.create_embed(), delete_after=int(current_song.source.duration_int))
            while ctx.voice_client.is_playing():
                await asyncio.sleep(5)

    @commands.command()
    async def play(self, ctx: commands.Context, *, search: str) -> None:
        """ Puts the next request into queue and determines whether the request is a youtube link or mp3 file """
        async with ctx.typing():
            if self._is_url(search):
                try:
                    source = await YTDLSource.from_url(ctx, search, loop=self.bot.loop, stream=True)
                except Exception as e:
                    print(e)
                else:
                    await self._insert_next_song_in_queue(ctx, source)
                    await ctx.send(f'Enqueued {str(source)}', delete_after=self.configuration.short_delete_after_time)
            else:
                try:
                    # Error handling så den ikke bare æder alle strings :o)
                    # Måske lidt trim og sådan noget fint noget.
                    mp3_path = self.configuration.mp3_folder_path + search + ".mp3"
                    source = await MP3Source.create_source(ctx, mp3_path, title=search)
                except Exception as e:
                    print(e)
                else:
                    if ctx.voice_client.is_playing():
                        current_audio_source = ctx.voice_client.source
                        ctx.voice_client.pause()
                        await self._insert_next_song_in_queue(ctx, current_audio_source)
                        await self._insert_next_song_in_queue(ctx, source)
                        await ctx.send(f'Enqueued {str(source)}',
                                       delete_after=self.configuration.short_delete_after_time)
                    else:
                        await self._insert_next_song_in_queue(ctx, source)
                        await ctx.send(f'Enqueued {str(source)}',
                                       delete_after=self.configuration.short_delete_after_time)

    @staticmethod
    def _is_url(search: str) -> bool:
        """ Returns true if the string is a url """
        x = urlparse(search)
        return bool(x.scheme)

    # Do something about no type hint here for source
    async def _add_to_queue(self, song) -> None:  # source: YTDLSource or MP3Source
        """ Determines where in the queue the current source should be placed and places it into the queue """
        if isinstance(song.source, YTDLSource):
            await self.queue.put((self.yt_priority, song))
            self.yt_priority -= 1
        else:
            await self.queue.put((self.mp3_priority, song))
            self.mp3_priority -= 1

    async def _insert_next_song_in_queue(self, ctx, source) -> None:
        """ Appends the next song into the queue """
        song = Song(source)
        self.context_list.append(ctx)
        await self._add_to_queue(song)

    @commands.command(brief="Makes the bot join a desired voice channel",
                      help="Defaults to the channel the author is in. "
                           "Can connect to other channels by specifying the channels id after the command ")
    async def connect(self, ctx: commands.Context, *, channel: discord.VoiceChannel = None) -> None:
        """ Connects the bot to a voice channel either based on passed channel id or the authors channel """
        if not channel and not ctx.author.voice:
            await ctx.send("No channel specified and author not in room.",
                           delete_after=self.configuration.short_delete_after_time)

        destination = channel or ctx.author.voice.channel
        await destination.connect()

    @commands.command(help="Makes the bot leave voice channel")
    async def stop(self, ctx: commands.Context) -> None:
        """ Makes the bot disconnect from the voice channel """
        await ctx.voice_client.disconnect()

    # De her virker ikke pt fordi pause jo nu bliver brugt deroppe i det der andet noget.
    # Måske bare lige en bette bool ? :o)
    #@commands.command(brief="Pauses the current song")
    #async def pause(self, ctx: commands.Context) -> None:
    #    """ Makes the bot pause the currently playing song """
    #    ctx.voice_client.pause()
    #    await ctx.send("Paused", delete_after=self.configuration.short_delete_after_time)

    #@commands.command(brief="Resumes the current song")
    #async def resume(self, ctx: commands.Context) -> None:
    #    """ Makes the bot resume playing from a paused state """
    #    ctx.voice_client.resume()
    #    await ctx.send("Resumed", delete_after=self.configuration.short_delete_after_time)

    @commands.command(brief="Skips to the next audio in the queue")
    async def skip(self, ctx: commands.Context) -> None:
        """ Skips the currently playing song in the queue and starts playing the next song """
        if self.queue:
            ctx.voice_client.stop()
            await ctx.send(f"Skipping the current song: {self.current_song.source.title}",
                           delete_after=self.configuration.short_delete_after_time)
        else:
            await ctx.send("Unable to skip. The queue is empty.",
                           delete_after=self.configuration.short_delete_after_time)

    @commands.command(brief="Changes the volume the bot is playing", help="I.e. .volume 60 sets the volume to 60%",
                      aliases=['v', 'vol'])
    async def volume(self, ctx: commands.Context, volume: int) -> discord.Message:
        """ Adjusts the volume of the bot. Sends a message to notify if not connected to a voice channel """
        if ctx.voice_client is None:
            return await ctx.send("Not connected to a voice channel.",
                                  delete_after=self.configuration.short_delete_after_time)

        self.volume = volume / 100
        ctx.voice_client.source.volume = self.volume
        await ctx.send(f"Changed volume to {volume}%", delete_after=self.configuration.short_delete_after_time)

    @commands.command(help="Shows all the current mp3 files")
    async def available(self, ctx: commands.Context) -> None:
        """ Gets all the currently available mp3 files for playing and sends them to the user """
        available_mp3_files = self._available()
        await ctx.send(available_mp3_files, delete_after=self.configuration.very_long_delete_after_time)

    def _available(self) -> str:
        """ Returns a formatted string with all the available mp3 files from the self.configuration.mp3_folder_path """
        available_mp3_files = "```**Available mp3 files:**\n"
        for filename in os.listdir(self.configuration.mp3_folder_path):
            if filename.endswith('.mp3'):
                available_mp3_files += f"{filename[:-4]}\n"
        available_mp3_files += "```"
        return available_mp3_files

    @commands.command(name="channels", brief="Returns all voice channels with members connected")
    async def available_channels(self, ctx: commands.Context) -> None:
        """ Command that gets all channels for the users and sends them back to the user """
        embed = self._get_all_channels_with_users_connected(ctx.guild.id)
        await ctx.send(embed=embed, delete_after=self.configuration.very_long_delete_after_time)

    def _get_all_channels_with_users_connected(self, guild_id: int) -> discord.Embed:
        """ Returns an embed with all the channels with users connected to them with their information """
        embed = discord.Embed(title="Voice channels with members connected")
        guild = self.bot.get_guild(guild_id)
        for channel in guild.channels:
            if isinstance(channel, discord.VoiceChannel):
                if channel.members:
                    members_string = ""
                    for member in channel.members:
                        members_string += f'{member.name}\n'
                    embed.add_field(name=f'**{channel.name}**',
                                    value=f'>ID: {channel.id}\n'
                                          f'>Members: \n{members_string}\n')
        return embed

    @play.before_invoke
    async def ensure_voice(self, ctx: commands.Context) -> None:
        """ Ensures that the bot is in a voice channel. This is called before the play command is invoked """
        if ctx.voice_client is None:
            if ctx.author.voice:
                await ctx.author.voice.channel.connect()
            else:
                await ctx.send("You are not connected to a voice channel.")
                raise commands.CommandError("Author not connected to a voice channel.")


def setup(bot):
    bot.add_cog(Player(bot))


class MP3Source(discord.PCMVolumeTransformer):
    """ Represents a MP3Source which is an audio clip from a local mp3 file """
    def __init__(self, ctx: commands.Context, source: discord.FFmpegPCMAudio, title: str, volume: float = 0.5):
        super().__init__(source, volume)
        self.title: str = title
        self.requester: typing.Union[discord.Member, discord.User] = ctx.author
        self.duration_int: int = 15  # A hack for now. Don't know how I should know the length of these clips.

    def __str__(self):
        return f'**{self.title}** requested by **{self.requester}**'

    # Not sure how to type hint the return value of this?
    @classmethod
    async def create_source(cls, ctx: commands.Context, mp3_path: str, title: str):
        """ Creates a instance of MP3Source given the mp3 path and title """
        return cls(ctx, discord.FFmpegPCMAudio(mp3_path), title)


class YTDLSource(discord.PCMVolumeTransformer):
    """ Represents a YoutubeDownloadSource which is the audio from a youtube link which the class also handles """
    ytdl_format_options: dict = {
        'format': 'bestaudio/best',
        'outtmpl': '%(extractor)s-%(id)s-%(title)s.%(ext)s',
        'restrictfilenames': True,
        'noplaylist': True,
        'nocheckcertificate': True,
        'ignoreerrors': False,
        'logtostderr': False,
        'quiet': True,
        'no_warnings': True,
        'default_search': 'auto',
        'source_address': '0.0.0.0'  # bind to ipv4 since ipv6 addresses cause issues sometimes
    }

    ffmpeg_options: dict = {
        'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'
    }

    ytdl: youtube_dl.YoutubeDL = youtube_dl.YoutubeDL(ytdl_format_options)

    def __init__(self, ctx, source, *, data, volume=0.5):
        super().__init__(source, volume)

        self.requester: typing.Union[discord.Member, discord.User] = ctx.author
        self.data: dict = data

        self.uploader: str = data.get('uploader')
        self.uploader_url: str = data.get('uploader_url')
        date: str = data.get('upload_date')
        self.upload_date = date[6:8] + '.' + date[4:6] + '.' + date[0:4]
        self.title: str = data.get('title')
        self.thumbnail: str = data.get('thumbnail')
        self.description: str = data.get('description')
        self.duration: str = self._parse_duration(int(data.get('duration'))) # Tror den her fucker op hvis det er en live stream.
        self.duration_int: int = int(data.get('duration'))
        self.url: str = data.get('webpage_url')
        self.stream_url: str = data.get('url')

    def __str__(self):
        return f'**{self.title}** by **{self.uploader}**'

    # Not sure how to type hint the return value of this?
    @classmethod
    async def from_url(cls, ctx: commands.Context, url: str, *, loop: asyncio.AbstractEventLoop = None,
                       stream: bool = False):
        """ Creates an instance of the class from an url """
        loop = loop or asyncio.get_event_loop()
        data = await loop.run_in_executor(None, lambda: cls.ytdl.extract_info(url, download=not stream))

        if 'entries' in data:
            # take first item from a playlist
            data = data['entries'][0]

        filename = data['url'] if stream else cls.ytdl.prepare_filename(data)
        return cls(ctx, discord.FFmpegPCMAudio(filename, **cls.ffmpeg_options), data=data)

    @staticmethod
    def _parse_duration(duration: int) -> str:
        """ Parses the duration from an int and creates a formatted string from it """
        minutes, seconds = divmod(duration, 60)
        hours, minutes = divmod(minutes, 60)
        days, hours = divmod(hours, 24)

        duration = []

        if days > 0:
            duration.append(f'{days} days')
        if hours > 0:
            duration.append(f'{hours} hours')
        if minutes > 0:
            duration.append(f'{minutes} minutes')
        if seconds > 0:
            duration.append(f'{seconds} seconds')

        return ', '.join(duration)


class Song:
    """ Represents a single song which could either be YTDLSource or a MP3Source """
    def __init__(self, source: YTDLSource or MP3Source):
        self.source: YTDLSource or MP3Source = source
        self.requester: typing.Union[discord.Member, discord.User] = source.requester

    def create_embed(self) -> discord.Embed:
        """ Creates an embed for the song with the varies information about the song """
        if isinstance(self.source, YTDLSource):
            embed = (discord.Embed(title='Now playing',
                                   description=f'\n{self.source.title}\n',
                                   color=discord.Color.blurple())
                     .add_field(name='Duration', value=self.source.duration)
                     .add_field(name='Requested by', value=self.requester.mention)
                     .add_field(name='Uploader', value=f'[{self.source.uploader}]({self.source.uploader_url})')
                     .add_field(name='URL', value=f'[Click]({self.source.url})')
                     .set_thumbnail(url=self.source.thumbnail))
        else:
            embed = (discord.Embed(title='Now playing',
                                   description=f'\n{self.source.title}\n',
                                   color=discord.Color.blurple())
                     .add_field(name='Requested by', value=self.requester.mention))
        return embed
