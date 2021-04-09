import discord
from discord.ext import commands
import chess
import chess.svg
from cairosvg import svg2png
import random


class Chess(commands.Cog):
    # Some documentation

    def __init__(self, bot):
        self.bot = bot
        self.configuration = bot.get_cog("Configuration")
        self.white = None
        self.black = None
        self.board = chess.Board()
        self.allSendMsgs = []
        self.whiteTurn = True


    @commands.Cog.listener()
    async def on_ready(self):
        print("Chess cog is loaded")

    @commands.command(name="startGame", brief="Starts a new chess game", help="startGame @user to start a game with the mentioned user")
    async def start_game(self, ctx):
        if self.white is not None and self.black is not None:
            return await ctx.send("Game already running", delete_after=self.configuration.short_delete_after_time)
        elif len(ctx.message.mentions) == 0:
            return await ctx.send("Specify opponent", delete_after=self.configuration.short_delete_after_time)
        elif len(ctx.message.mentions) > 1:
            return await ctx.send("Too many players", delete_after=self.configuration.short_delete_after_time)
        elif ctx.message.mentions[0] == ctx.message.author:
            return await ctx.send("Sadly you cant play against yourself cause", delete_after=self.configuration.short_delete_after_time)
        self._start_game(ctx.message.author, ctx.message.mentions[0])
        x = await ctx.send(file=discord.File('board.png'))
        self.allSendMsgs.append(x)

    # Needs to check if it is one of the two players playing the game that is making the move.
    @commands.command(brief="Followed by the chess move",
                      help="Followed by coordinate: \npawn = just coordinate\nknight = N\nBishop = B\nQueen = Q\nRook "
                           "= R (Rhg1 e.g. if both rooks can get to g1)\nCapture = x e.g. exd5")
    async def move(self, ctx, move: str):
        if self.white is None and self.black is None:
            await ctx.send("No game started", delete_after=self.configuration.short_delete_after_time)
        elif move == '':
            await ctx.send("Specify move", delete_after=self.configuration.short_delete_after_time)
        elif ctx.message.author is not self.white or ctx.message.author is not self.black:
            await ctx.send("You are not one of the players", delete_after=self.configuration.short_delete_after_time)

        try:
            self.board.push_san(move)
            if self.board.is_game_over():
                await ctx.send(file=discord.File('board.png'), delete_after=self.configuration.medium_delete_after_time)
                await ctx.send("Game over", delete_after=self.configuration.medium_delete_after_time)
                await self._reset()
            else:
                self._get_png(self.whiteTurn)
                self.whiteTurn = not self.whiteTurn
                x = await ctx.send(file=discord.File('board.png'))
                self.allSendMsgs.append(x)
        except ValueError:
            await ctx.send("{} is an illegal move".format(move), delete_after=self.configuration.short_delete_after_time)

    @commands.command(name="resetChess", brief="Resets the chess game")
    async def reset_chess(self, ctx):
        await self._reset()

    def _start_game(self, player_one, player_two):
        rng = random.randrange(0, 1)
        if rng == 0:
            self.white = player_one
            self.black = player_two
        else:
            self.white = player_two
            self.black = player_one
        self._get_png(False)

    def _get_png(self, flipped):
        data = chess.svg.board(self.board, flipped=flipped)
        svg2png(bytestring=data, write_to="board.png")

    async def _reset(self):
        self.white = None
        self.black = None
        self.board = chess.Board()
        self.whiteTurn = True

        for msg in self.allSendMsgs:
            await msg.delete()

        self.allSendMsgs = []


def setup(bot):
    bot.add_cog(Chess(bot))
