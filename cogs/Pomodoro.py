import discord
import datetime
import asyncio
from discord.ext import commands
import Db


class Pomodoro(commands.Cog):
    # Some documentation

    def __init__(self, bot):
        self.bot = bot
        self.current_timers = []
        self.in_room_counter = 0

    @commands.Cog.listener()
    async def on_ready(self):
        print("Pomodoro cog is loaded")

    @commands.Cog.listener()
    async def on_voice_state_update(self, member, before, after):
        if after.channel is None:
            self.in_room_counter = self.in_room_counter - 1
        elif before is None and after is not None:
            self.in_room_counter = self.in_room_counter + 1
        
        if self.in_room_counter >= 2 and not self.current_timers:
            x = self.bot.get_channel(619094316106907660)
            await x.send("Pomodoro?", delete_after=300)

    # Timer skal komme ind som en parameter så ejg kan dependency inject den og så kan der unit testes !
    @commands.command(brief="Default value 50/10", help=".pomodoro x y, where x is work length and y is break length.", aliases=['p'])
    async def pomodoro(self, ctx):
        play_cmd = self.bot.get_command("play_pomodoro")
        work_length, break_length = await self.get_lengths_from_message(ctx.message)
        new_timer = Timer(ctx.message.author.id, work_length, break_length)
        work_end_time, break_end_time = self.format_time(work_length, break_length, new_timer)
        await ctx.send("Starting timers: {} / {} minutes. \nWork ends at {} \nBreak ends at {}".format(work_length / 60, break_length / 60, work_end_time, break_end_time), delete_after=new_timer.workLength + new_timer.breakLength)
        self.current_timers.append(new_timer)

        await new_timer.work_timer()
        await ctx.send("Works over! Break starts now", delete_after=break_length)
        # Ensures voice. This is a "hack".
        # Lav da det der get_command med ensure voice.
        if ctx.voice_client is None:
            if ctx.author.voice:
                await ctx.author.voice.channel.connect()
        await ctx.invoke(play_cmd)

        await new_timer.break_timer()
        await ctx.send("Breaks over!", delete_after=15)

        # Ensures voice. This is a "hack".
        if ctx.voice_client is None:
            if ctx.author.voice:
                await ctx.author.voice.channel.connect()
        await ctx.invoke(play_cmd)

        query = 'INSERT INTO pomodoros ("startingTime", "workLength", "breakLength", author) VALUES ({}, {}, {}, {})'.format(new_timer.startingDate, new_timer.workLength, new_timer.breakLength, new_timer.author_id)
        await Db.myfetch(query)
        
        await ctx.message.delete()

    @staticmethod
    async def get_lengths_from_message(message):
        x = [int(s) for s in message.content.split() if s.isdigit()] # Gets all the digits from the string and saves in a list of integers.
        if len(x) == 0:
            author_id = message.author.id
            query = 'SELECT "prefWorkTimer", "prefBreakTimer" FROM users WHERE id={}'.format(author_id)
            y = await Db.myfetch(query)
            work_timer = y[0][0]
            break_timer = y[0][1]
            return work_timer * 60, break_timer * 60
        elif len(x) == 2:
            work_length = x[0]
            break_length = x[1]
            return work_length * 60, break_length * 60
        else:
            print("Something went wrong.")

    # Idk something needs to be done with this formatting. Its not doing it right xd
    # strftime eller sådan noget
    @staticmethod
    def format_time(work_length, break_length, new_timer):
        x = new_timer.startingTime + datetime.timedelta(seconds=work_length)
        y = new_timer.startingTime + datetime.timedelta(seconds=work_length + break_length)
        work_minute = x.minute
        work_second = x.second
        break_minute = y.minute
        break_second = y.second
        if x.minute <= 9:
            work_minute = int(str(0) + str(x.minute))
        if x.second <= 9:
            work_second = int(str(0) + str(x.second))
        if y.minute <= 9:
            break_minute = int(str(0) + str(y.minute))
        if x.second <= 9:
            break_second = int(str(0) + str(y.second))

        workEndTime = "{}:{}:{}".format(x.hour, work_minute, work_second)
        breakEndTime = "{}:{}:{}".format(y.hour, break_minute, break_second)
        return workEndTime, breakEndTime

    @commands.command(name='time', brief="Remaining time on pomodoro timer", help="time timerName, currently needs this timer name cause its not fully operational yet :D")
    async def _time(self, ctx):
        needed_timer = self.current_timers[0]
        for timer in self.current_timers:
            if ctx.message.author.id == timer.author_id:
                needed_timer = timer
        remaining_time = needed_timer.calculate_remaining_time()
        await ctx.send("remaining time on timer {}: {}".format(needed_timer.name, remaining_time), delete_after=15)
        await ctx.message.delete()

    @commands.command(name="changeDefault", brief=".default 25 5 e.g.", aliases=['default', 'changedefault', 'change'])
    async def change_default(self, ctx, pref_work, pref_break):
        if pref_work is None or pref_break is None:
            query = 'SELECT "prefWorkTimer", "prefBreakTimer" FROM users WHERE id={}'.format(ctx.message.author.id)
            x = await Db.myfetch(query)
            await ctx.send(f"Please specify both preferred work length and break length. Your current defaults are: {x[0][0]} / {x[0][1]}", delete_after=15)
        query = 'UPDATE users SET "prefWorkTimer" = {}, "prefBreakTimer" = {} WHERE id={}'.format(pref_work, pref_break, ctx.message.author.id)
        await Db.myfetch(query)
        await ctx.send(f"Updated your default values to {pref_work} / {pref_break}", delete_after=15)
        await ctx.message.delete()


def setup(bot):
    bot.add_cog(Pomodoro(bot))


class Timer:
    def __init__(self, author_id, work_length, break_length):
        self.author_id = author_id
        self.workLength = work_length
        self.breakLength = break_length
        self.startingTime = datetime.datetime.now()
        self.startingDate = datetime.datetime.now().date() # A little hack for now
        self.workBool = True

    async def work_timer(self):
        self.workBool = True
        await asyncio.sleep(self.workLength)

    async def break_timer(self):
        self.workBool = False
        await asyncio.sleep(self.breakLength)

    def calculate_remaining_time(self):
        hours = 0
        minutes = 0
        duration = datetime.datetime.now() - self.startingTime
        durationInSeconds = duration.total_seconds()

        if self.workBool:
            remainingTimeInSeconds = self.workLength - durationInSeconds
        else:
            remainingTimeInSeconds = self.breakLength - durationInSeconds
        
        if remainingTimeInSeconds > 3600:
            hours, remainingTimeInSeconds = divmod(remainingTimeInSeconds, 3600)
        if remainingTimeInSeconds > 60:
            minutes, remainingTimeInSeconds = divmod(remainingTimeInSeconds, 60)

        formattedRemainingTime = ('%02d:%02d:%02d' % (hours, minutes, remainingTimeInSeconds))
        print(formattedRemainingTime)
        return formattedRemainingTime
