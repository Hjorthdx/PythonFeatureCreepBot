import discord, os
from discord.ext import commands
from trello import TrelloClient

class Trello(commands.Cog):
    # Some documentation

    def __init__(self, bot):
        self.bot = bot
        self.client = TrelloClient( # Hide this before push :)
            api_key=os.getenv("TRELLO_APIKEY"),
            token=os.getenv("TRELLO_TOKEN")
        )
        self.trelloBoard = self.client.list_boards()[-1]
        self.trelloLists = self.trelloBoard.list_lists()

    # This is very interesting. Perhabs it has a future in the feature creep bot.
    # Keep digging into this.
    @commands.Cog.listener()
    async def on_ready(self):
        print("Trello cog is loaded")
        '''
        all_boards = self.client.list_boards()
        print("\nAll the boards:")
        for board in all_boards:
            print(board.name)

        last_board = all_boards[-1]
        print("\nLast board name:")
        print(last_board.name)

        allLists = last_board.list_lists()
        print("\nThe lists:")
        print(allLists)
        print("\nList ID's:")
        for e in allLists:
            print(e.id)
            e.add_card("TESTXD")

        list1 = last_board.get_list('5f62a498b28d5c3943f066c9')
        print("\nCard names in list:")
        for card in list1.list_cards():
            print(card.name)
            #card.comment('This is a test comment')

        print("\nCard comments:")
        for card in list1.list_cards():
            print(card.get_comments())
            card.change_list("5f62a49a2d2d32431ccaaa69")
        '''
        
    @commands.command(help="")
    async def addcard(self, ctx, name: str, description: str, id: str):
        trelloList = self.trelloBoard.get_lists(id)
        trelloList.add_card(name=name, description=description)
        await ctx.send("Added card to {}, with name: {} and description: {}".format(id, name, description))

def setup(bot):
    bot.add_cog(Trello(bot))
