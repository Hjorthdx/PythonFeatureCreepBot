import os
import discord
import Db
from dotenv import load_dotenv
from discord.ext import commands

load_dotenv()

bot = commands.Bot(command_prefix='.')


@bot.command(hidden=True)
async def load(ctx, extension):
    if ctx.author.id == 140195461519769601:
        bot.load_extension(f'cogs.{extension}')
        await ctx.message.delete()


@bot.command(hidden=True)
async def unload(ctx, extension):
    if ctx.author.id == 140195461519769601:
        bot.unload_extension(f'cogs.{extension}')
        await ctx.message.delete()


@bot.command(hidden=True)
async def reload(ctx, extension):
    if ctx.author.id == 140195461519769601:
        bot.unload_extension(f'cogs.{extension}')
        bot.load_extension(f'cogs.{extension}')
        await ctx.message.delete()


@bot.event
async def on_ready():
    print(f'{bot.user} has connected to Discord!')


@bot.event
async def on_command_error(ctx, error):
    print(error)
    await ctx.send(error, delete_after=15)
    await ctx.message.delete()


for filename in os.listdir('C:/Users/Sren/PycharmProjects/DiscordFeatureCreepBot/cogs/'):
    if filename.endswith('.py'):
        bot.load_extension(f'cogs.{filename[:-3]}')

bot.run(os.getenv("TOKEN"))
