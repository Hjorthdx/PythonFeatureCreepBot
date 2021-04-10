import discord
import os
import asyncio
import youtube_dl
from discord.ext import commands


class Player(commands.Cog):
    # Some documentation

    def __init__(self, bot):
        self.bot = bot
        self.configuration = bot.get_cog("Configuration")
        self.base_path = "C:/Users/Sren/PycharmProjects/DiscordFeatureCreepBot/mp3-files/"
        self.volume = .5
        self.queue = asyncio.PriorityQueue()
        self.context_list = []
        self.next = asyncio.Event()
        self.bot.loop.create_task(self.audio_player_task())

        # Magic values right now. Should be set to something else. Just this for now while testing.
        self.play_priority = 20
        self.yt_priority = 0

    @commands.Cog.listener()
    async def on_ready(self):
        print("Player cog is loaded")

    async def audio_player_task(self):
        while True:
            self.next.clear()
            current_song = await self.queue.get()
            current_song = current_song[2]
            ctx = self.context_list.pop(0)
            async with ctx.typing():
                if isinstance(current_song, discord.PCMVolumeTransformer):
                    ctx.voice_client.play(current_song, after=lambda e: self.bot.loop.call_soon_threadsafe(self.next.set))
                else:
                    audio_source = await YTDLSource.from_url(current_song, loop=self.bot.loop, stream=True)
                    audio_source.volume = self.volume
                    ctx.voice_client.play(audio_source, after=lambda e: self.bot.loop.call_soon_threadsafe(self.next.set))
                    await ctx.send(f'Now playing: {audio_source.title} at {self.volume * 100}%',
                           delete_after=audio_source.duration)  # Only writes for yt. Does not write anything for .play
            await self.next.wait()

    @commands.command(brief="play slet dem. !available for list of all mp3's")
    async def play(self, ctx, *, user_input):
        mp3_path = self.base_path + user_input + ".mp3"
        if ctx.voice_client.is_playing():
            current_audio_source = ctx.voice_client.source
            ctx.voice_client.pause()
            await self._add_to_queue(ctx, source=current_audio_source)
            source = discord.PCMVolumeTransformer(discord.FFmpegPCMAudio(mp3_path))
            await self._add_to_queue(ctx, source=source)
            self.next.set()
        else:
            source = discord.PCMVolumeTransformer(discord.FFmpegPCMAudio(mp3_path))
            await self._add_to_queue(ctx, source=source)
            self.next.set()

    @commands.command(help="yt youtube link", aliases=['youtube'])
    async def yt(self, ctx, *, url):
        await self._add_to_queue(ctx, url=url)
        await ctx.send(f"Url added to the queue", delete_after=self.configuration.short_delete_after_time)

    async def _add_to_queue(self, ctx, url=None, source=None):
        if url is not None:
            await self.queue.put((self.yt_priority, url))
            self.yt_priority += 1
            self.context_list.append(ctx)
        else:
            await self.queue.put((self.play_priority, source))
            self.play_priority -= 1
            self.context_list.append(ctx)


    @commands.command(help="Shows all the current mp3 files")
    async def available(self, ctx):
        available_mp3_files = self._available()
        await ctx.send(available_mp3_files, delete_after=self.configuration.very_long_delete_after_time)

    def _available(self):
        available_mp3_files = "```**Available mp3 files:**\n"
        for filename in os.listdir(self.base_path):
            if filename.endswith('.mp3'):
                available_mp3_files += f"{filename[:-4]}\n"
        available_mp3_files += "```"
        return available_mp3_files

    @commands.command(brief="Changes the volume the bot is playing", help="I.e. !volume 60 sets the volume to 60%",
                      aliases=['v'])
    async def volume(self, ctx, volume: int):
        if ctx.voice_client is None:
            return await ctx.send("Not connected to a voice channel.", delete_after=self.configuration.short_delete_after_time)

        self.volume = volume / 100
        ctx.voice_client.source.volume = self.volume
        await ctx.send(f"Changed volume to {volume}%", delete_after=self.configuration.short_delete_after_time)

    @commands.command(brief="Makes the bot join a desired voice channel",
                      help="Defaults to the channel the author is in. "
                           "Can connect to other channels by specifying the channels id after the command ")
    async def connect(self, ctx, *, channel: discord.VoiceChannel = None):
        if ctx.voice_client is not None:
            await ctx.voice_client.move_to(channel)
            return

        if channel is None:
            if ctx.author.voice:
                await ctx.author.voice.channel.connect()
                return

        await channel.connect()

    @commands.command(name="channels", brief="Returns all voice channels with members connected")
    async def available_channels(self, ctx):
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

    @commands.command(help="Makes the bot leave voice channel")
    async def stop(self, ctx):
        await ctx.voice_client.disconnect()

    @commands.command(brief="Pauses the current song")
    async def pause(self, ctx):
        ctx.voice_client.pause()
        await ctx.send("Paused", delete_after=self.configuration.short_delete_after_time)

    @commands.command(brief="Resumes the current song")
    async def resume(self, ctx):
        ctx.voice_client.resume()
        await ctx.send("Resumed", delete_after=self.configuration.short_delete_after_time)

    @commands.command(brief="Skips to the next audio in the queue")
    async def skip(self, ctx):
        if self.queue:
            ctx.voice_client.pause()
            self.next.set()
            await ctx.send("Skipped the current song.", delete_after=self.configuration.short_delete_after_time)
        else:
            ctx.send("Queue is empty", delete_after=self.configuration.short_delete_after_time)

    @play.before_invoke
    @yt.before_invoke
    async def ensure_voice(self, ctx):
        if ctx.voice_client is None:
            if ctx.author.voice:
                await ctx.author.voice.channel.connect()
            else:
                await ctx.send("You are not connected to a voice channel.")
                raise commands.CommandError("Author not connected to a voice channel.")

    async def leave_voice(self, ctx):
        if self.queue:
            # Sleeping while still playing audio.
            await asyncio.sleep(1)
        await ctx.voice_client.disconnect()


def setup(bot):
    bot.add_cog(Player(bot))


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


class YTDLSource(discord.PCMVolumeTransformer):
    def __init__(self, source, *, data, volume=0.5):
        super().__init__(source, volume)

        self.data = data

        self.title = data.get('title')
        self.url = data.get('url')
        self.duration = data.get('duration')

    @classmethod
    async def from_url(cls, url, *, loop=None, stream=False):
        loop = loop or asyncio.get_event_loop()
        data = await loop.run_in_executor(None, lambda: ytdl.extract_info(url, download=not stream))

        if 'entries' in data:
            # take first item from a playlist
            data = data['entries'][0]

        filename = data['url'] if stream else ytdl.prepare_filename(data)
        return cls(discord.FFmpegPCMAudio(filename, **ffmpeg_options), data=data)
