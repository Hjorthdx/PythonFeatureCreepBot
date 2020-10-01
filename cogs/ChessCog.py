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
        self.white = None
        self.black = None
        self.board = chess.Board()
        self.allSendMsgs = []
        self.whiteTurn = True

    @commands.Cog.listener()
    async def on_ready(self):
        print("Chess cog is loaded")

    @commands.command(brief="Starts a new chess game", help="startGame @user to start a game with the mentioned user")
    async def startGame(self, ctx):
        if self.white is not None and self.black is not None:
            return await ctx.send("Game already running", delete_after=15)
        elif len(ctx.message.mentions) == 0:
            return await ctx.send("Specify opponent", delete_after=15)
        elif len(ctx.message.mentions) > 1:
            return await ctx.send("Too many players", delete_after=15)
        elif ctx.message.mentions[0] == ctx.message.author:
            return await ctx.send("Sadly you cant play against yourself cause", delete_after=15)
        rng = random.randrange(0,1)
        if rng == 0:
            self.white = ctx.message.author
            self.black = ctx.message.mentions[0]
        else:
            self.white = ctx.message.mentions[0]
            self.black = ctx.message.author

        self.getpng(False)
        x = await ctx.send(file=discord.File('board.png'))
        self.allSendMsgs.append(x)
        await ctx.message.delete()

    # Needs to check if it is one of the two players playing the game that is making the move.
    @commands.command(brief="Followed by the chess move", help="Followed by coordinate: \npawn = just coordinate\nknight = N\nBishop = B\nQueen = Q\nRook = R (Rhg1 e.g. if both rooks can get to g1)\nCapture = x e.g. exd5")
    async def move(self, ctx, move: str):
        if self.white is None and self.black is None:
            await ctx.send("No game started", delete_after=15)
        elif move == '':
            await ctx.send("Specify move", delete_after=15)
        try:
            self.board.push_san(move)
            if self.board.is_game_over():
                await ctx.send(file=discord.File('board.png'), delete_after=30)
                await ctx.send("Game over", delete_after=30)
                await self.Reset()
            else:
                self.getpng(self.whiteTurn)
                self.whiteTurn = not self.whiteTurn
                x = await ctx.send(file=discord.File('board.png'))
                self.allSendMsgs.append(x)
        except ValueError:
            await ctx.send("{} is an illegal move".format(move), delete_after=15)

        await ctx.message.delete()

    @commands.command(brief="Resets the chess game")
    async def resetChess(self, ctx):
        await self.Reset()
        await ctx.message.delete()

    def getpng(self, flipped):
        data = chess.svg.board(self.board, flipped=flipped)
        svg2png(bytestring=data, write_to="board.png")

    async def Reset(self):
        self.white = None
        self.black = None
        self.board = chess.Board()
        self.whiteTurn = True

        for msg in self.allSendMsgs:
            await msg.delete()

        self.allSendMsgs = []

def setup(bot):
    bot.add_cog(Chess(bot))