from typing import Tuple
import discord
import datetime
import asyncio
from discord.ext import commands
import Db
import requests

CONSTANT_SECONDS_IN_AN_HOUR = 3600
CONSTANT_SECONDS_IN_A_MINUTE = 60


class PomodoroCog(commands.Cog, name="Pomodoro"):
    """ Pomodoro cog that is responsible for handling user inputs """

    def __init__(self, bot):
        self.bot: discord.client = bot
        self.configuration = bot.get_cog("Configuration")
        self.player_cog = self.bot.get_cog("Player")
        self.pomodoro_manager: PomodoroManager = PomodoroManager()
        self.group_size: int = 6
        self.reminder_message_id: int = 0  # Måske none prøv lige at teste med det der

    @commands.Cog.listener()
    async def on_ready(self):
        print("Pomodoro cog is loaded")

    @commands.Cog.listener()
    async def on_voice_state_update(self, member: discord.Member, before: discord.VoiceState, after: discord.VoiceState) -> None:
        if not self._is_pomodoro_ready(before, after):
            return None

        channel = self.bot.get_channel(self.configuration.p7_generel_room_id)
        try:
            message = await channel.fetch_message(self.reminder_message_id)
            return None
        except discord.NotFound as error:
            reminder_message = await self._send_pomodoro_reminder_message(self.configuration.p7_generel_room_id)
            self.reminder_message_id = reminder_message.id

    def _is_pomodoro_ready(self, before: discord.VoiceState, after: discord.VoiceState) -> bool:
        return after.channel is not None or \
                not self._is_schedule_booked() or \
                before.channel is None or \
                len(after.channel.members) >= self.group_size or \
                self.pomodoro_manager.is_category_without_timer(self.configuration.p7_category_id)

    def _is_schedule_booked(self) -> bool:
        """ Calls the schedule api endpoint and returns true or false based on if the schedule is currently booked """
        response = requests.get(self.configuration.schedule_check_API_LINK)
        if response.status_code == 200:
            if response.content == b'True':
                return True
            elif response.content == b'False':
                return False
        else:
            print("Api did not return status code 200")
            return False

    def _is_category_without_timer(self, after_category_id: int, category_id: int) -> bool:
        """ Returns a bool that says if a category does have a timer currently or not """
        if after_category_id == category_id and self.pomodoro_manager.is_category_without_timer(category_id):
            return True
        else:
            return False

    async def _send_pomodoro_reminder_message(self, room_id: int) -> discord.message:
        """ Sends a pomodoro reminder message in a channel based on room id and returns the message """
        channel = self.bot.get_channel(room_id)
        message = await channel.send("Did you forget to start a pomodoro?",
                                     delete_after=self.configuration.very_long_delete_after_time)
        return message

    # Burde man bare her  sige fuck det lorte og så bare tage en ting ind i.e. input, og så på den så fanger vi info ud af den?
    # Fordi problemet med det her er jo at der findes de her cases
    # .po 50 10
    # .po 50 10 "my timer"
    # .po 50 10  my timer # idk om det her faktisk virker
    # .po "my timer"
    # .po my timer # igen uden "" her.
    @commands.command(aliases=['po', 'pom', 'pomo', 'pomdro', 'pomdoro'])
    async def pomodoro(self, ctx, work_length=None, break_length=None, name: str = None) -> None:
        # Temporary fix
        # This is done to be able to use the command with the syntax .po mytimer
        # and it would accept it as name mytimer with your default preferred timers.
        # Could possibly be done better with the paramters of the command itself.
        if work_length is not None:
            if not work_length.isdigit():
                name = work_length
                work_length = None

        if work_length is None or break_length is None:
            work_length, break_length = self._get_work_break_length(ctx.message.author.id)

        work_duration = datetime.timedelta(minutes=int(work_length))
        break_duration = datetime.timedelta(minutes=int(break_length))

        new_pomodoro = self.pomodoro_manager.start_new_pomodoro(ctx.message.channel.category_id, work_duration,
                                                                break_duration, name)

        await ctx.send(f"Starting pomodoro!\n"
                       f"Name: {new_pomodoro.name}\n"
                       f"Timers: {self._to_minutes(new_pomodoro.work_timer.duration)} / {self._to_minutes(new_pomodoro.break_timer.duration)}\n"
                       f"Work ends at: {self._to_string_format(new_pomodoro.get_end_work_time())}\n"
                       f"Break ends at: {self._to_string_format(new_pomodoro.get_end_break_time())}\n",
                       delete_after=new_pomodoro.total_time.total_seconds())
        await new_pomodoro.work_timer.start()
        await self.player_cog.ensure_voice(ctx=ctx)
        await self.player_cog.play(ctx=ctx, search="bamse")

        await ctx.send(f"Work is over!\n"
                       f"Kick back, relax, and grab yourself a beverage!\n"
                       f"Break ends at {self._to_string_format(new_pomodoro.get_end_break_time())}",
                       delete_after=new_pomodoro.break_timer.duration.total_seconds())
        await new_pomodoro.break_timer.start()
        await self.player_cog.ensure_voice(ctx=ctx)
        await self.player_cog.play(ctx=ctx, search="bamse")
        await ctx.send(f"Break is over!\n"
                       f"Perhabs time to start a new timer?",
                       delete_after=self.configuration.long_delete_after_time)
        Db.add_pomodoro_to_db(self._to_minutes(new_pomodoro.work_timer.duration),
                              self._to_minutes(new_pomodoro.break_timer.duration), ctx.message.author.id,
                              new_pomodoro.work_timer.starting_time)

    @staticmethod
    def _get_work_break_length(author_id: int) -> Tuple[int, int]:
        """ Gets the work and break length from the db based on the authors id and returns tuple with lengths """
        user = Db.get_user_by_id(author_id)
        return user.preferred_work_timer, user.preferred_break_timer

    @staticmethod
    def _to_minutes(timedelta: datetime.timedelta) -> float:
        """ Returns the amount of minutes left based on the time delta """
        return timedelta.total_seconds() / CONSTANT_SECONDS_IN_A_MINUTE

    @staticmethod
    def _to_string_format(time: datetime) -> str:
        """ Returns the time in a formatted string """
        return time.strftime("%H:%M:%S")

    @commands.command(name="changeDefault", brief=".default 25 5 e.g.", aliases=['default', 'changedefault', 'change'])
    async def change_default(self, ctx: commands.Context, preferred_work_timer: int = None,
                             preferred_break_timer: int = None) -> None:
        """ Updates the users default preferences for timers """
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
    async def get_remaining_time(self, ctx: commands.Context, name: str = None) -> None:
        """ Gets the remaining time of a timer based on either name or category and sends it to the user """
        if name is not None:
            timer = self.pomodoro_manager.find_pomodoro_timer(name=name)
        else:
            timer = self.pomodoro_manager.find_pomodoro_timer(category_id=ctx.message.channel.category_id)
        if not timer:
            await ctx.send("Could not find any timers!", delete_after=self.configuration.medium_delete_after_time)
        else:
            if timer[0].is_work_over():
                break_timer_remaining_time = timer[0].break_timer.get_remaining_time()
                await ctx.send(f"Remaining time: {self._timedelta_to_string_format(break_timer_remaining_time)}",
                               delete_after=self.configuration.medium_delete_after_time)
            else:
                work_timer_remaining_time = timer[0].work_timer.get_remaining_time()
                await ctx.send(f"Remaining time: {self._timedelta_to_string_format(work_timer_remaining_time)}",
                               delete_after=self.configuration.medium_delete_after_time)

    @staticmethod
    def _timedelta_to_string_format(time_delta: datetime.timedelta) -> str:
        """ Returns the timedelta object and returns it into a formatted string """
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
    """ A single timer that has the responsibility of sleeping for the desired amount """

    def __init__(self, duration: datetime.timedelta):
        self.duration = duration
        self.starting_time = datetime
        self.end_time = datetime

    async def start(self) -> None:
        """ Starts the timer and sleeps for the duration that is specified """
        self.starting_time = datetime.datetime.now()
        self.end_time = self.starting_time + self.duration
        await asyncio.sleep(self.duration.total_seconds())

    def get_remaining_time(self) -> datetime.timedelta:
        """ Gets the remaining time of the timer and returns a timedelta object """
        return self.duration - (datetime.datetime.now() - self.starting_time)


class PomodoroTimer:
    """ A single pomodoro timer that encapsulates both the work timer and break timer """

    def __init__(self, category_id: int, work_duration: datetime.timedelta, break_duration: datetime.timedelta,
                 name=None):
        self.category_id = category_id
        self.work_timer = Timer(work_duration)
        self.break_timer = Timer(break_duration)
        self.name = name
        self.total_time = self.work_timer.duration + self.break_timer.duration
        self.starting_time = datetime.datetime.now()

    def get_end_work_time(self) -> datetime:
        """ Gets the datetime object of the time when the work period is over """
        return self.starting_time + self.work_timer.duration

    def get_end_break_time(self) -> datetime:
        """ Gets the datetime object of the time when the break period is over """
        return self.starting_time + self.work_timer.duration + self.break_timer.duration

    def is_work_over(self) -> bool:
        """ Returns a bool that says if the current time is after the work period """
        return datetime.datetime.now() > (self.work_timer.starting_time + self.work_timer.duration)

    def __eq__(self, other) -> bool:
        return isinstance(other, PomodoroTimer) and \
               other.category_id == self.category_id and \
               other.work_timer.duration == self.work_timer.duration and \
               other.break_timer.duration == self.break_timer.duration and \
               other.name == self.name


class PomodoroManager:
    """ Manages all pomodoro timers """

    def __init__(self):
        self._list_of_pomodoro_timers = []

    def start_new_pomodoro(self, category_id: int, work_duration: datetime.timedelta,
                           break_duration: datetime.timedelta, name=None) -> PomodoroTimer:
        """ Creates a new pomodoro timer and adds it to the list of current running timers """
        new_pomodoro = PomodoroTimer(category_id, work_duration, break_duration, name)
        self._list_of_pomodoro_timers.append(new_pomodoro)
        return new_pomodoro

    def find_pomodoro_timer(self, name: str = None, category_id: int = None) -> [PomodoroTimer]:
        """ Finds a pomodoro either by name or category id.
            Returns a list of pomodoro timers that match or None if no timers match """
        return [e for e in self._list_of_pomodoro_timers if
                (e.name == name and name is not None) or e.category_id == category_id]

    def is_list_of_pomodoros_empty(self) -> bool:
        """ Returns whether the current list of Pomodoro timers is empty, i.e. does any timers exist? """
        return not self._list_of_pomodoro_timers

    # Kan det her one lines?
    def is_category_without_timer(self, category_id: int) -> bool:
        """ Returns a True if a category (as in Discord category on a server) does not a timer currently running """
        timers_attached_to_category = [e for e in self._list_of_pomodoro_timers if (e.category_id == category_id)]
        if not timers_attached_to_category:
            return True
        else:
            return False
