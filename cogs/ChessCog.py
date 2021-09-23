import discord
from discord.ext import commands
import chess
import chess.svg
from cairosvg import svg2png
import random
import typing


class ChessCog(commands.Cog, name="Chess"):
    """ Chess cog that is responsible for handling user inputs and handle playing a game of chess """

    def __init__(self, bot):
        self.bot: discord.client = bot
        self.configuration = bot.get_cog("Configuration")
        self.white: typing.Optional[discord.abc.User] = None
        self.black: typing.Optional[discord.abc.User] = None
        self.board: chess.Board = chess.Board()
        self.allSendMsgs: [discord.Message] = []
        self.whiteTurn: bool = True

    @commands.Cog.listener()
    async def on_ready(self):
        print("Chess cog is loaded")

    @commands.command(name="startGame", brief="Starts a new chess game",
                      help="startGame @user to start a game with the mentioned user")
    async def start_game(self, ctx: commands.Context) -> discord.Message:
        """ Verifies that a game is ready to be started based on certain conditions.
            Opponent is based on @user from the user calling the command """
        if self.white is not None and self.black is not None:
            return await ctx.send("Game already running", delete_after=self.configuration.short_delete_after_time)
        elif len(ctx.message.mentions) == 0:
            return await ctx.send("Specify opponent", delete_after=self.configuration.short_delete_after_time)
        elif len(ctx.message.mentions) > 1:
            return await ctx.send("Too many players", delete_after=self.configuration.short_delete_after_time)
        elif ctx.message.mentions[0] == ctx.message.author:
            return await ctx.send("Sadly you cant play against yourself cause",
                                  delete_after=self.configuration.short_delete_after_time)
        self._start_game(ctx.message.author, ctx.message.mentions[0])
        x = await ctx.send(file=discord.File('board.png'))
        self.allSendMsgs.append(x)

    @commands.command(brief="Followed by the chess move",
                      help="Followed by coordinate: \npawn = just coordinate\nknight = N\nBishop = B\nQueen = Q\nRook "
                           "= R (Rhg1 e.g. if both rooks can get to g1)\nCapture = x e.g. exd5")
    async def move(self, ctx: commands.Context, move: str) -> None:
        """ Makes a move in the game of chess if it is a valid move """
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
    async def reset_chess(self) -> None:
        """ Reset command to restart the game for the users """
        await self._reset()

    def _start_game(self, player_one: discord.abc.User, player_two: discord.abc.User):
        """ The method that actually starts the game of game of chess """
        rng = random.randrange(0, 1)
        if rng == 0:
            self.white = player_one
            self.black = player_two
        else:
            self.white = player_two
            self.black = player_one
        self._get_png(False)

    def _get_png(self, flipped: bool):
        """ Gets the png for the current board position """
        data = chess.svg.board(self.board, flipped=flipped)
        svg2png(bytestring=data, write_to="board.png")

    async def _reset(self) -> None:
        """ The function that actually resets the game of chess and deletes all messages that is linked to the game """
        self.white = None
        self.black = None
        self.board = chess.Board()
        self.whiteTurn = True

        for msg in self.allSendMsgs:
            await msg.delete()

        self.allSendMsgs = []


def setup(bot):
    bot.add_cog(ChessCog(bot))
