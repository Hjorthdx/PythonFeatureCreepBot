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
        player_cog = self.bot.get_cog("Player")
        if work_length is None or break_length is None:
            work_length, break_length = self._get_work_break_length(ctx.message.author.id)

        work_duration = datetime.timedelta(minutes=int(work_length))
        break_duration = datetime.timedelta(minutes=int(break_length))

        new_pomodoro = self.pomodoro_manager.start_new_pomodoro(ctx.message.channel.category_id, work_duration, break_duration, name)

        await ctx.send(f"Starting pomodoro with timers: "
                       f"{self._to_minutes(new_pomodoro.work_timer.duration)} / {self._to_minutes(new_pomodoro.break_timer.duration)}!\n"
                       f"Work ends at: {self._to_string_format(new_pomodoro.get_end_work_time())}\n"
                       f"Break ends at: {self._to_string_format(new_pomodoro.get_end_break_time())}\n",
                       delete_after=new_pomodoro.total_time.total_seconds())
        await new_pomodoro.work_timer.start()
        await player_cog.ensure_voice(ctx=ctx)
        await ctx.invoke(self.bot.get_command('play'), user_input="bamse")

        await ctx.send(f"Work is over!\n"
                       f"Kick back, relax, and grab yourself a beverage!\n"
                       f"Break ends at {new_pomodoro.get_end_break_time()}",
                       delete_after=self.configuration.long_delete_after_time)
        await new_pomodoro.break_timer.start()
        await player_cog.ensure_voice(ctx=ctx)
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

    @staticmethod
    def _to_string_format(time):
        return time.strftime("%H:%M:%S")

    @commands.command(name="changeDefault", brief=".default 25 5 e.g.", aliases=['default', 'changedefault', 'change'])
    async def change_default(self, ctx, preferred_work_timer=None, preferred_break_timer=None):
        if preferred_work_timer is None or preferred_break_timer is None:
            preferred_work_timer, preferred_break_timer = Db.get_preferred_work_and_break_timer(ctx.message.author.id)
            await ctx.send(f"Please specify both preferred work length and break length. Your current defaults are: "
                           f"{preferred_work_timer} / {preferred_break_timer}",
                           delete_after=self.configuration.short_delete_after_time)
        else:
            Db.update_preferred_work_and_break_timer(ctx.message.author.id, preferred_work_timer, preferred_break_timer)
            await ctx.send(f"Updated your default values to {preferred_work_timer} / {preferred_break_timer}",
                           delete_after=self.configuration.short_delete_after_time)

    @commands.command(name="time")
    async def get_remaining_time(self, ctx, name=None):
        if name is not None:
            timer = self.pomodoro_manager.find_pomodoro_timer(name=name)
        else:
            timer = self.pomodoro_manager.find_pomodoro_timer(category_id=ctx.message.channel.category_id)
        if not timer:
            print("Something went wrong")
            await ctx.send("Could not find any timers!", delete_after=self.configuration.medium_delete_after_time)
        else:
            if timer[0].is_work_over():
                break_timer_remaining_time = timer[0].break_timer.get_remaining_time().total_seconds()
                await ctx.send(f"Remaining time: {self._timedelta_to_string_format(break_timer_remaining_time)}",
                               delete_after=self.configuration.medium_delete_after_time)
            else:
                work_timer_remaining_time = timer[0].work_timer.get_remaining_time()
                await ctx.send(f"Remaining time: {self._timedelta_to_string_format(work_timer_remaining_time)}",
                               delete_after=self.configuration.medium_delete_after_time)

    @staticmethod
    def _timedelta_to_string_format(time_delta):
        hours = 0
        minutes = 0
        remaining_time_in_seconds = time_delta.total_seconds()

        if remaining_time_in_seconds > CONSTANT_SECONDS_IN_AN_HOUR:
            hours, remaining_time_in_seconds = divmod(remaining_time_in_seconds, CONSTANT_SECONDS_IN_AN_HOUR)
        if remaining_time_in_seconds > CONSTANT_SECONDS_IN_A_MINUTE:
            minutes, remaining_time_in_seconds = divmod(remaining_time_in_seconds, CONSTANT_SECONDS_IN_A_MINUTE)

        formatted_remaining_time = ('%02d:%02d:%02d' % (hours, minutes, remaining_time_in_seconds))
        return formatted_remaining_time


def setup(bot):
    bot.add_cog(PomodoroCog(bot))


class Timer:
    def __init__(self, duration: datetime.timedelta):
        self.duration = duration
        self.starting_time = None
        self.end_time = None

    async def start(self):
        self.starting_time = datetime.datetime.now()
        self.end_time = self.starting_time + self.duration
        await asyncio.sleep(self.duration.total_seconds())

    def get_remaining_time(self):
        return self.duration - (datetime.datetime.now() - self.starting_time)


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
        return self.starting_time + self.work_timer.duration + self.break_timer.duration

    def is_work_over(self):
        return datetime.datetime.now() > (self.work_timer.starting_time + self.work_timer.duration)

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
