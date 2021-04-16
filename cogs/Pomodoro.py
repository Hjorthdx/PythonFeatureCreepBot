import discord
import datetime
import asyncio
from discord.ext import commands
import Db

CONSTANT_SECONDS_IN_AN_HOUR = 3600
CONSTANT_SECONDS_IN_A_MINUTE = 60


class PomodoroCog(commands.Cog, name="Pomodoro"):
    # Some documentation

    def __init__(self, bot):
        self.bot = bot
        self.configuration = bot.get_cog("Configuration")
        self.pomodoro_manager = PomodoroManager()
        self.in_room_counter = 0

    @commands.Cog.listener()
    async def on_ready(self):
        print("Pomodoro cog is loaded")

    # Not refactored yet
    @commands.Cog.listener()
    async def on_voice_state_update(self, member, before, after):
        if after.channel is None:
            self.in_room_counter = self.in_room_counter - 1
        elif before is None and after is not None:
            self.in_room_counter = self.in_room_counter + 1
        
        if self.in_room_counter >= 2 and not self.current_timers:
            x = self.bot.get_channel(619094316106907660)
            await x.send("Pomodoro?", delete_after=self.configuration.very_long_delete_after_time)

    # Læs indtil der ikke er mere. Sidste parameter kun. Prøv at læs doc
    @commands.command()
    async def pomodoro(self, ctx, work_length=None, break_length=None, name=None):
        await ctx.invoke(self.bot.get_command('play'), user_input="bamse")
        player_cog = self.bot.get_cog("Player")
        if work_length is None or break_length is None:
            work_length, break_length = self._get_work_break_length(ctx.message.author.id)

        work_duration = datetime.timedelta(minutes=int(work_length))
        break_duration = datetime.timedelta(minutes=int(break_length))

        new_pomodoro = self.pomodoro_manager.start_new_pomodoro(ctx.message.channel.category_id, work_duration, break_duration, name)

        await ctx.send(f"Starting pomodoro with timers: "
                       f"{self._to_minutes(new_pomodoro.work_timer.duration)} / {self._to_minutes(new_pomodoro.break_timer.duration)}!\n"
                       f"Work ends at: {new_pomodoro.get_end_work_time()}\n"
                       f"Break ends at: {new_pomodoro.get_end_break_time()}\n",
                       delete_after=new_pomodoro.total_time.total_seconds())
        await new_pomodoro.work_timer.start()
        #await player_cog.ensure_voice(ctx=ctx)
        await ctx.invoke(self.bot.get_command('play'), user_input="bamse")

        await ctx.send(f"Work is over!\n"
                       f"Kick back, relax, and grab yourself a beverage!\n"
                       f"Break ends at {new_pomodoro.get_end_break_time()}",
                       delete_after=self.configuration.long_delete_after_time)
        await new_pomodoro.break_timer.start()
        await player_cog.play(ctx=ctx, user_input="bamse")
        await ctx.send(f"Break is over!\n"
                       f"Perhabs time to start a new timer?",
                       delete_after=self.configuration.long_delete_after_time)
        Db.add_pomodoro_to_db(self._to_minutes(new_pomodoro.work_timer.duration), self._to_minutes(new_pomodoro.break_timer.duration), ctx.message.author.id, new_pomodoro.work_timer.starting_time)

    @staticmethod
    def _get_work_break_length(author_id):
        user = Db.get_user_by_id(author_id)
        return user.preferred_work_timer, user.preferred_break_timer

    @staticmethod
    def _to_minutes(timedelta):
        return timedelta.total_seconds() / CONSTANT_SECONDS_IN_A_MINUTE


def setup(bot):
    bot.add_cog(PomodoroCog(bot))


class Timer:
    def __init__(self, duration: datetime.timedelta):
        self.duration = duration
        self.starting_time = None

    async def start(self):
        self.starting_time = datetime.datetime.now()
        await asyncio.sleep(self.duration.total_seconds())

    def get_remaining_time_in_seconds(self):
        return datetime.timedelta(datetime.datetime.now() - self.starting_time)


class PomodoroTimer:
    def __init__(self, category_id, work_duration, break_duration, name=None):
        self.category_id = category_id
        self.work_timer = Timer(work_duration)
        self.break_timer = Timer(break_duration)
        self.name = name
        self.total_time = self.work_timer.duration + self.break_timer.duration
        self.starting_time = datetime.datetime.now()

    def get_end_work_time(self):
        return self.starting_time + self.work_timer.duration

    def get_end_break_time(self):
        return self.starting_time + self.break_timer.duration

    def __eq__(self, other):
        return isinstance(other, PomodoroTimer) and \
               other.category_id == self.category_id and \
               other.work_timer.duration == self.work_timer.duration and \
               other.break_timer.duration == self.break_timer.duration and \
               other.name == self.name


class PomodoroManager:
    def __init__(self):
        self._list_of_pomodoros = []

    def start_new_pomodoro(self, category_id, work_duration, break_duration, name=None):
        new_pomodoro = PomodoroTimer(category_id, work_duration, break_duration, name)
        self._list_of_pomodoros.append(new_pomodoro)
        return new_pomodoro

    def find_pomodoro_timer(self, name=None, category_id=None):
        return [e for e in self._list_of_pomodoros if (e.name == name and name is not None) or e.category_id == category_id]




    '''

    def get_remaining_time(self):
        hours = 0
        minutes = 0
        elapsed_time_in_seconds = (datetime.datetime.now() - self.starting_time).total_seconds()

        remaining_time_in_seconds = self.length - elapsed_time_in_seconds

        while remaining_time_in_seconds > self.seconds_in_an_hour:
            hours, remaining_time_in_seconds = divmod(remaining_time_in_seconds, self.seconds_in_an_hour)
        while remaining_time_in_seconds > self.seconds_in_a_minute:
            minutes, remaining_time_in_seconds = divmod(remaining_time_in_seconds, self.seconds_in_a_minute)

        formatted_remaining_time = ('%02d:%02d:%02d' % (hours, minutes, remaining_time_in_seconds))
        return formatted_remaining_time

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






class Timer:
    def __init__(self, author_id, work_length, break_length):
        self.author_id = author_id
        self.work_length = work_length
        self.break_length = break_length
        self.starting_time = datetime.datetime.now()
        self.starting_date = datetime.datetime.now().date() # A little hack for now
        self.workBool = True

    async def work_timer(self):
        self.workBool = True
        await asyncio.sleep(self.work_length)

    async def break_timer(self):
        self.workBool = False
        await asyncio.sleep(self.break_length)

    def calculate_remaining_time(self):
        hours = 0
        minutes = 0
        duration = datetime.datetime.now() - self.starting_time
        durationInSeconds = duration.total_seconds()

        if self.workBool:
            remainingTimeInSeconds = self.work_length - durationInSeconds
        else:
            remainingTimeInSeconds = self.break_length - durationInSeconds
        
        if remainingTimeInSeconds > 3600:
            hours, remainingTimeInSeconds = divmod(remainingTimeInSeconds, 3600)
        if remainingTimeInSeconds > 60:
            minutes, remainingTimeInSeconds = divmod(remainingTimeInSeconds, 60)

        formattedRemainingTime = ('%02d:%02d:%02d' % (hours, minutes, remainingTimeInSeconds))
        print(formattedRemainingTime)
        return formattedRemainingTime
'''