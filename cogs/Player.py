import discord
import os
import asyncio
import youtube_dl
from discord.ext import commands
from urllib.parse import urlparse
from async_timeout import timeout


class Player(commands.Cog):
    # Some documentation

    def __init__(self, bot):
        self.bot = bot
        self.configuration = bot.get_cog("Configuration")
        self.volume = .5
        self.queue = asyncio.PriorityQueue()
        self.context_list = []
        self.current_context = None
        self.current_song = None
        self.next = asyncio.Event()
        self.bot.loop.create_task(self.audio_player_task())

        # Magic values right now. Should be set to something else. Just this for now while testing.
        self.mp3_priority = 20
        self.yt_priority = 0

    @commands.Cog.listener()
    async def on_ready(self):
        print("Player cog is loaded")

    # Prøv at gøre så vi kune prøver get inde i try og så resten af logikken derude efter. Tror måske det kan løse lidt.
    async def audio_player_task(self):
        while True:
            self.next.clear()
            #try:
            #async with timeout(self.configuration.timeout_time):
            current_song = await self.queue.get()
            current_song = current_song[1]
            self.current_song = current_song
            ctx = self.context_list.pop(0)
            self.current_context = ctx
            async with ctx.typing():
                ctx.voice_client.play(current_song.source, after=lambda e: self.bot.loop.call_soon_threadsafe(self.next.set))
                await ctx.send(embed=current_song.create_embed(), delete_after=int(current_song.source.duration_int))
            await self.next.wait()
        #except asyncio.TimeoutError:
            #    print("TimeoutError")
            #    if not self.current_context.voice_client.is_playing():
            #        await self.current_context.voice_client.disconnect()
            #        print("Timed out. Leaving!")

    @commands.command()
    async def play(self, ctx: commands.Context, *, search: str):
        async with ctx.typing():
            if self._is_url(search):
                try:
                    source = await YTDLSource.from_url(ctx, search, loop=self.bot.loop, stream=True)
                except Exception as e:
                    print(e)
                else:  # This way this code is only run if no exceptions WAIT ISNT THIS REALLY STUPID? Just write it after the other things in try. Im so stupid
                    await self._insert_next_song_in_queue(ctx, source)
                    await ctx.send(f'Enqueued {str(source)}', delete_after=self.configuration.short_delete_after_time)
            else:
                try:
                    mp3_path = self.configuration.mp3_folder_path + search + ".mp3"
                    source = await MP3Source.create_source(ctx, mp3_path, title=search)
                except Exception as e:
                    print("Not url or mp3")
                    print(e)
                else:
                    if ctx.voice_client.is_playing():
                        current_audio_source = ctx.voice_client.source
                        ctx.voice_client.stop()
                        await self._insert_next_song_in_queue(ctx, source)
                        await self._insert_next_song_in_queue(ctx, current_audio_source)
                        await ctx.send(f'Enqueued {str(source)}', delete_after=self.configuration.short_delete_after_time)
                        self.next.set()
                    else:
                        await self._insert_next_song_in_queue(ctx, source)
                        await ctx.send(f'Enqueued {str(source)}', delete_after=self.configuration.short_delete_after_time)
                        self.next.set()

    @staticmethod
    def _is_url(search: str):
        x = urlparse(search)
        return bool(x.scheme)

    async def _add_to_queue(self, source):  # source: YTDLSource or MP3Source
        if isinstance(source, YTDLSource):
            await self.queue.put((self.yt_priority, source))
            self.yt_priority += 1
        else:
            await self.queue.put((self.mp3_priority, source))
            self.mp3_priority -= 1

    async def _insert_next_song_in_queue(self, ctx, source):
        song = Song(source)
        self.context_list.append(ctx)
        await self._add_to_queue(song)

    @commands.command(brief="Makes the bot join a desired voice channel",
                      help="Defaults to the channel the author is in. "
                           "Can connect to other channels by specifying the channels id after the command ")
    async def connect(self, ctx: commands.Context, *, channel: discord.VoiceChannel = None):
        if not channel and not ctx.author.voice:
            ctx.send("No channel specified and author not in room.", delete_after=self.configuration.short_delete_after_time)

        if not channel and not ctx.author.voice:
            ctx.send("No channel specified and author not in room.",
                     delete_after=self.configuration.short_delete_after_time)

        destination = channel or ctx.author.voice.channel
        if ctx.voice_state.voice:
            await ctx.voice.voice.move_to(destination)
            return

        ctx.voice_state.voice = await destination.connect()

    @commands.command(help="Makes the bot leave voice channel")
    async def stop(self, ctx: commands.Context):
        await ctx.voice_client.disconnect()

    @commands.command(brief="Pauses the current song")
    async def pause(self, ctx: commands.Context):
        ctx.voice_client.pause()
        await ctx.send("Paused", delete_after=self.configuration.short_delete_after_time)

    @commands.command(brief="Resumes the current song")
    async def resume(self, ctx: commands.Context):
        ctx.voice_client.resume()
        await ctx.send("Resumed", delete_after=self.configuration.short_delete_after_time)

    @commands.command(brief="Skips to the next audio in the queue")
    async def skip(self, ctx: commands.Context):
        if self.queue:
            ctx.voice_client.stop()
            self.next.set()
            await ctx.send(f"Skipping the current song: {self.current_song.source.title}", delete_after=self.configuration.short_delete_after_time)
        else:
            await ctx.send("Unable to skip. The queue is empty.", delete_after=self.configuration.short_delete_after_time)

    @commands.command(brief="Changes the volume the bot is playing", help="I.e. .volume 60 sets the volume to 60%",
                      aliases=['v', 'vol'])
    async def volume(self, ctx: commands.Context, volume: int):
        if ctx.voice_client is None:
            return await ctx.send("Not connected to a voice channel.",
                                  delete_after=self.configuration.short_delete_after_time)

        self.volume = volume / 100
        ctx.voice_client.source.volume = self.volume
        await ctx.send(f"Changed volume to {volume}%", delete_after=self.configuration.short_delete_after_time)

    @commands.command(help="Shows all the current mp3 files")
    async def available(self, ctx: commands.Context):
        available_mp3_files = self._available()
        await ctx.send(available_mp3_files, delete_after=self.configuration.very_long_delete_after_time)

    def _available(self):
        available_mp3_files = "```**Available mp3 files:**\n"
        for filename in os.listdir(self.configuration.mp3_folder_path):
            if filename.endswith('.mp3'):
                available_mp3_files += f"{filename[:-4]}\n"
        available_mp3_files += "```"
        return available_mp3_files

    @commands.command(name="channels", brief="Returns all voice channels with members connected")
    async def available_channels(self, ctx: commands.Context):
        embed = self._get_all_channels_with_users_connected()
        await ctx.send(embed=embed, delete_after=self.configuration.very_long_delete_after_time)

    def _get_all_channels_with_users_connected(self):
        embed = discord.Embed(title="Voice channels with members connected")
        guild = self.bot.get_guild(self.configuration.guild_id)
        for channel in guild.channels:
            if isinstance(channel, discord.VoiceChannel):
                if channel.members:
                    members_string = ""
                    for member in channel.members:
                        members_string += f'{member.name}\n'
                    embed.add_field(name=f'**{channel.name}**',
                                    value=f'>ID: {channel.id}\n'
                                          f'>Members: {members_string}\n')
        return embed

    @play.before_invoke
    async def ensure_voice(self, ctx: commands.Context):
        if ctx.voice_client is None:
            if ctx.author.voice:
                await ctx.author.voice.channel.connect()
            else:
                await ctx.send("You are not connected to a voice channel.")
                raise commands.CommandError("Author not connected to a voice channel.")


def setup(bot):
    bot.add_cog(Player(bot))


class MP3Source(discord.PCMVolumeTransformer):
    def __init__(self, ctx: commands.Context, source: discord.FFmpegPCMAudio, title: str, volume: float = 0.5):
        super().__init__(source, volume)

        self.title = title
        self.requester = ctx.author
        self.duration_int = 15  # A hack for now. Don't know how I should know the length of these clips.

    def __str__(self):
        return f'**{self.title}** requested by **{self.requester}**'

    @classmethod
    async def create_source(cls, ctx: commands.Context, mp3_path: str, title: str):
        return cls(ctx, discord.FFmpegPCMAudio(mp3_path), title)


class YTDLSource(discord.PCMVolumeTransformer):
    ytdl_format_options = {
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

    ffmpeg_options = {
        'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'
    }

    ytdl = youtube_dl.YoutubeDL(ytdl_format_options)

    def __init__(self, ctx, source, *, data, volume=0.5):
        super().__init__(source, volume)

        self.requester = ctx.author
        self.data = data

        self.uploader = data.get('uploader')
        self.uploader_url = data.get('uploader_url')
        date = data.get('upload_date')
        self.upload_date = date[6:8] + '.' + date[4:6] + '.' + date[0:4]
        self.title = data.get('title')
        self.thumbnail = data.get('thumbnail')
        self.description = data.get('description')
        self.duration = self._parse_duration(int(data.get('duration')))
        self.duration_int = int(data.get('duration'))
        self.url = data.get('webpage_url')
        self.stream_url = data.get('url')

    def __str__(self):
        return f'**{self.title}** by **{self.uploader}**'

    @classmethod
    async def from_url(cls, ctx, url, *, loop=None, stream=False):
        loop = loop or asyncio.get_event_loop()
        data = await loop.run_in_executor(None, lambda: cls.ytdl.extract_info(url, download=not stream))

        if 'entries' in data:
            # take first item from a playlist
            data = data['entries'][0]

        filename = data['url'] if stream else cls.ytdl.prepare_filename(data)
        return cls(ctx, discord.FFmpegPCMAudio(filename, **cls.ffmpeg_options), data=data)

    @staticmethod
    def _parse_duration(duration: int):
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
    def __init__(self, source: YTDLSource or MP3Source):
        self.source = source
        self.requester = source.requester

    def create_embed(self):
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
