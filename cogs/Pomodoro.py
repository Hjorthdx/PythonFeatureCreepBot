import discord
import datetime
import asyncio
from discord.ext import commands
import Db
import requests

CONSTANT_SECONDS_IN_AN_HOUR = 3600
CONSTANT_SECONDS_IN_A_MINUTE = 60


class PomodoroCog(commands.Cog, name="Pomodoro"):
    # Some documentation

    def __init__(self, bot):
        self.bot = bot
        self.configuration = bot.get_cog("Configuration")
        self.pomodoro_manager = PomodoroManager()
        self.group_size = 3
        self.generel_message_created_at = None
        self.test_created_at = None

    @commands.Cog.listener()
    async def on_ready(self):
        print("Pomodoro cog is loaded")

    @commands.Cog.listener()
    async def on_voice_state_update(self, member, before, after):
        if after.channel is None or self._is_schedule_booked():
            return
        if len(after.channel.members) == self.group_size and before is None:
            if self._is_category_without_timer(after.channel.category_id, self.configuration.project_category_id):
                reminder_message = await self._send_pomodoro_reminder_message(self.configuration.generel_room_id)

            elif self._is_category_without_timer(after.channel.category_id, self.configuration.pensionist_category_id):
                await self._send_pomodoro_reminder_message(self.configuration.pensionist_generel_room_id)

            elif self._is_category_without_timer(after.channel.category_id, self.configuration.young_guns_category_id):
                await self._send_pomodoro_reminder_message(self.configuration.young_guns_generel_room_id)
        '''
        elif self._is_category_without_timer(after.channel.category_id, 630796890182516737) and \
                self._has_time_passed(self.test_created_at):
            print("test3")
            channel = self.bot.get_channel(630796890182516738)
            current_message = await channel.send("Pomodoro?", delete_after=10)
            self.test_created_at = current_message.created_at
        '''

    def _is_schedule_booked(self):
        response = requests.get(self.configuration.schedule_check_API_LINK)
        if response.status_code == 200:
            if response.content == b'True':
                return True
            elif response.content == b'False':
                return False
        else:
            print("Api did not return status code 200")
            return False

    def _is_category_without_timer(self, after_category_id, category_id):
        if after_category_id == category_id and self.pomodoro_manager.is_category_without_timer(category_id):
            return True
        else:
            return False

    '''
    # Hvis jeg ændrer til en anden variabel i delete_after over, så skal det også ændres her.
    # Kan man ikke få det til at linke sammen? Altså så de bare passer sammen
    def _has_time_passed(self, created_at):
        if created_at is None:
            return True
        print("I am called")
        y = datetime.datetime.now() - created_at
        x = y > 10
        print(f"x: {x}")
        return x
    '''

    async def _send_pomodoro_reminder_message(self, room_id):
        channel = self.bot.get_channel(room_id)
        message = await channel.send("Did you forget to start a pomodoro?",
                           delete_after=self.configuration.very_long_delete_after_time)
        return message

    @commands.command(aliases=['po', 'pom', 'pomo', 'pomdro', 'pomdoro'])
    async def pomodoro(self, ctx, work_length=None, break_length=None, name=None):
        # Temporary fix
        # This is done to be able to use the command with the syntax .po mytimer
        # and it would accept it as name mytimer with your default preferred timers.
        # Could possibly be done better with the paramters of the command itself.
        if work_length is not None:
            if not work_length.isdigit():
                name = work_length
                work_length = None

        player_cog = self.bot.get_cog("Player")
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
        await player_cog.ensure_voice(ctx=ctx)
        await player_cog.play(ctx=ctx, user_input="bamse")

        await ctx.send(f"Work is over!\n"
                       f"Kick back, relax, and grab yourself a beverage!\n"
                       f"Break ends at {self._to_string_format(new_pomodoro.get_end_break_time())}",
                       delete_after=self.configuration.long_delete_after_time)
        await new_pomodoro.break_timer.start()
        await player_cog.ensure_voice(ctx=ctx)
        await player_cog.play(ctx=ctx, user_input="bamse")
        await ctx.send(f"Break is over!\n"
                       f"Perhabs time to start a new timer?",
                       delete_after=self.configuration.long_delete_after_time)
        Db.add_pomodoro_to_db(self._to_minutes(new_pomodoro.work_timer.duration),
                              self._to_minutes(new_pomodoro.break_timer.duration), ctx.message.author.id,
                              new_pomodoro.work_timer.starting_time)

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
        return [e for e in self._list_of_pomodoros if
                (e.name == name and name is not None) or e.category_id == category_id]

    def is_list_of_pomodoros_empty(self):
        return not self._list_of_pomodoros

    # Kan det her one lines?
    def is_category_without_timer(self, category_id):
        timers_attached_to_category = [e for e in self._list_of_pomodoros if (e.category_id == category_id)]
        if not timers_attached_to_category:
            return True
        else:
            return False
