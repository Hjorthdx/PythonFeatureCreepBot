import discord
from discord.ext import commands
import random
import asyncio


class Casino(commands.Cog):
    # Some documentation

    def __init__(self, bot):
        self.bot = bot
        self.configuration = bot.get_cog("Configuration")
        self.roulette = Roulette()

    @commands.Cog.listener()
    async def on_ready(self):
        print("Casino cog is loaded")

    # Should be expanded with the ability to place a bet aswell.
    # Perhabs give User another column with their balance
    # Only available for single player. Could be funny if it went idle and just kept spinning
    # Until everyone have placed their bets.
    @commands.command()
    async def roulette(self, ctx, bet=None, amount=None):
        random_number = self.roulette.get_next_spin()
        message = await ctx.send("Spinning the wheel :o)",
                       file=discord.File(self.configuration.gifs_folder_path + str(random_number) + '.gif'),
                       delete_after=self.configuration.long_delete_after_time)
        await asyncio.sleep(10)  # Should really be based on the video playing.
        await message.edit(content=f"The winning number is: {random_number}")

        if self.roulette.is_correct_guess(bet):
            await ctx.send(f"You guessed the right number!\n"
                           f"You win {amount} x 35 = {amount*35}",
                           delete_after=self.configuration.medium_delete_after_time)
        if self.roulette.is_even_number() and bet == 'black':
            await ctx.send(f"The number is an even number!\n"
                           f"You win {amount} x 2 = {amount*2}",
                           delete_after=self.configuration.medium_delete_after_time)
        if self.roulette.is_odd_number() and bet == 'red':
            await ctx.send(f"The number is an odd number!\n"
                           f"You win {amount} x 2 = {amount*2}",
                           delete_after=self.configuration.medium_delete_after_time)


def setup(bot):
    bot.add_cog(Casino(bot))


class Roulette:
    def __init__(self):
        self.green_number = 0
        self.black_numbers = [2, 4, 6, 8, 10, 11, 13, 15, 17, 20, 22, 24, 26, 28, 29, 31, 33, 35]
        self.red_numbers = [1, 3, 5, 7, 9, 12, 14, 16, 18, 19, 21, 23, 25, 27, 30, 32, 34, 36]
        self.random_number = None

    def get_next_spin(self):
        self.random_number = self._get_random_int(0, 37)
        return self.random_number

    @staticmethod
    def _get_random_int(_min, _max):
        return random.randint(_min, _max)

    def is_correct_guess(self, number):
        return number == self.random_number

    def is_odd_number(self):
        return self.random_number in self.red_numbers

    def is_even_number(self):
        return self.random_number in self.black_numbers



