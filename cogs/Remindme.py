import discord
import datetime
import dateutil
import asyncio
import re
from discord.ext import commands


class Remindme(commands.Cog):
    # Some documentation

    def __init__(self, bot):
        self.bot = bot
        self.configuration = bot.get_cog("Configuration")
        self.reminder_manager = ReminderManager()

    @commands.Cog.listener()
    async def on_ready(self):
        print("Remindme cog is loaded")

    @commands.command()
    async def remindme_time(self, ctx, time, *, message):
        #reminder_old = reminder_old(time, message, ctx.message.author)
        return None



    @commands.command()
    async def remindme(self, ctx, time, *, message):
        author = ctx.message.author

        new_reminder = self.reminder_manager.add_new_reminder(ctx, author, time, message)

        if new_reminder is None:
            await ctx.send("Could not determine datetime. Please try again!", delete_after=self.configuration.short_delete_after_time)
        else:
            await ctx.send("I'll remind you then!", delete_after=self.configuration.short_delete_after_time)


def setup(bot):
    bot.add_cog(Remindme(bot))


class Reminder:
    def __init__(self, ctx: commands.Context, author: int, text: str, time: datetime):
        self.ctx = ctx
        self.author = author
        self.text = text
        self.time = time

    async def sleep(self):
        await asyncio.sleep(self.time.total_seconds())

from datetime import datetime
from dateutil import parser
from dateutil import tz
from dateutil.relativedelta import relativedelta

class ReminderManager:
    def __init__(self, reminders: Reminder = None):
        self.reminders = []

    def add_new_reminder(self, ctx: commands.Context, author: int, time, message: str):
        date_time = self._parse_datetime(time)
        if date_time is None:
            print("Could not determine datetime")
            # Burde den skrive til brugeren her? Vel ikke.
            # Den skal vel returnerer noget som siger om det gik godt til cog'et så den ved hvad den skal skrive.
            return None

        new_reminder = Reminder(ctx, author, message, date_time)
        self.reminders.append(new_reminder)
        new_reminder.sleep()
        return new_reminder

    def _parse_datetime(self, message: discord.message):
        compiled = re.compile("""(?:(?P<years>[0-9])(?:years?|y))?
                                     (?:(?P<months>[0-9]{1,2})(?:months?|mo))?
                                     (?:(?P<weeks>[0-9]{1,4})(?:weeks?|w))?
                                     (?:(?P<days>[0-9]{1,5})(?:days?|d))?
                                     (?:(?P<hours>[0-9]{1,5})(?:hours?|h))?
                                     (?:(?P<minutes>[0-9]{1,5})(?:minutes?|m))?
                                     (?:(?P<seconds>[0-9]{1,5})(?:seconds?|s))?
                                     """, re.VERBOSE)
        match = compiled.fullmatch(message)
        if match is None or not match.group(0):
            try:
                message = parser.parse(f"{message} GMT+2", tzinfos=tz.gettz("Europe/Copenhagen"))
                return message
            except:
                return None

        data = { k: int(v) for k, v in match.groupdict(default=0).items() }
        now = datetime.datetime.now()
        message = now + relativedelta(**data)
        return message


class reminder_old:
    def __init__(self, time: str, text: str):
        print(time)
        self.time = time
        self.text = text
        self.totalSeconds = self.calculate_total_seconds()

    def calculate_total_seconds(self):
        days = 0
        hours = 0
        minutes = 0
        seconds = 0
        totalSeconds = 0
        remain = self.time
        if "days" in self.time.lower() or "day" in self.time.lower():
            days = self.time.split("day", 1)[0]
            remain = self.time.split("day", 1)[1]
            totalSeconds += int(days) * 60 * 60 * 24
        if "hours" in self.time.lower() or "hour" in self.time.lower():
            x = remain.split("hour", 1)[0]
            remain = remain.split("hour", 1)[1]
            hours = [int(s) for s in x.split() if s.isdigit()]
            totalSeconds += hours[0] * 60 * 60
        if "minutes" in self.time.lower() or "minute" in self.time.lower():
            x = remain.split("minute", 1)[0]
            remain = remain.split("minute", 1)[1]
            minutes = [int(s) for s in x.split() if s.isdigit()]
            totalSeconds += minutes[0] * 60
        if "seconds" in self.time.lower() or "second" in self.time.lower():
            x = remain.split("second", 1)[0]
            remain = remain.split("second", 1)[1]
            seconds = [int(s) for s in x.split() if s.isdigit()]
            totalSeconds += seconds[0]

        if days:
            print(f"days: {days}")

        if hours:
            print(f"hours: {hours[0]}")

        if minutes:
            print(f"minutes: {minutes[0]}")

        if seconds:
            print(f"seconds: {seconds[0]}")

        print(totalSeconds)
        return totalSeconds

    async def start_reminder(self):
        await asyncio.sleep(self.totalSeconds)
