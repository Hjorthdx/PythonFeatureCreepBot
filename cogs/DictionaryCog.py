import discord
from discord.ext import commands
from nltk.corpus import words
from itertools import chain
from nltk.corpus import wordnet
import nltk
#from random import sample
import random
import  re

# Remove none used imports
# Hint command ?

# Come up with better name for this cog
# DictionaryCog ?
class DictionaryCog(commands.Cog):
    # Some documentation

    def __init__(self, bot):
        self.bot = bot
        # Hard words list
        #self.wordsList = words.words()
        #self.randomWord = ''.join(sample(self.wordsList, 1))
        self.easyWordsListPath = "C:/Users/Sren/Documents/GitHub/DiscordKarmaBot/easier_words.txt"
        my_file = open(self.easyWordsListPath, 'r')
        self.wordsList=my_file.read()
        self.randomWord = random.choice(list(open(self.easyWordsListPath))).rstrip("\n")
        self.guessedWordsMsg = None
        self.guessedWordsBefore = []
        self.guessedWordsAfter = []
        #nltk.download('words')
        #nltk.download('wordnet')

    @commands.Cog.listener()
    async def on_ready(self):
        print("DictionaryCog cog is loaded")

    @commands.command(help="Just a stupid little game", aliases=['g'])
    async def guess(self, ctx, *, userGuess: str):
        YourWord = "Your word"
        print("Random word is:{}".format(self.randomWord))
        if re.search(r'\b{}\b'.format(userGuess), self.wordsList):
            if userGuess == self.randomWord:
                await ctx.send("The word was indeed {}! Congratz {} you got it".format(self.randomWord, ctx.author.name), delete_after=15)
                await self.guessedWordsMsg.delete()
                self.guessedWordsMsg = None
                self.randomWord = random.choice(list(open(self.easyWordsListPath))).rstrip("\n")
                await ctx.message.delete()
                return
            x = []
            x.append(self.randomWord)
            x.append(userGuess)
            x.sort()
            if x[0] == self.randomWord:
                await ctx.send("The word is before {}".format(userGuess), delete_after=15)
                self.guessedWordsAfter.append(userGuess)
                self.guessedWordsAfter.sort()
                if self.guessedWordsMsg is None:
                    self.guessedWordsMsg = await ctx.send("Current guessed words:\n {} {} {}".format(self.guessedWordsBefore, YourWord, self.guessedWordsAfter))
                else:
                    await self.guessedWordsMsg.edit(content="Current guessed words:\n {} {} {}".format(self.guessedWordsBefore, YourWord, self.guessedWordsAfter))
            if x[1] == self.randomWord:
                self.guessedWordsBefore.append(userGuess)
                self.guessedWordsBefore.sort()
                await ctx.send("The word is after {}".format(userGuess), delete_after=15)
                if self.guessedWordsMsg is None:
                    self.guessedWordsMsg = await ctx.send("Current guessed words:\n {} {} {}".format(self.guessedWordsBefore, YourWord, self.guessedWordsAfter))
                else:
                    await self.guessedWordsMsg.edit(content="Current guessed words:\n {} {} {}".format(self.guessedWordsBefore, YourWord, self.guessedWordsAfter))
        else:
            await ctx.send("{} is not in the words list!".format(userGuess), delete_after=15)
            
        await ctx.message.delete()

    @commands.command(brief="Prints out the alphabet for your convenience", aliases=['abc', 'alph'])
    async def alphabet(self, ctx):
        await ctx.send("A B C D E F G H I J K L M N O P Q R S T U V W X Y Z", delete_after=15)
        await ctx.message.delete()

    @commands.command(brief="Resets and generates a new word.")
    async def giveup(self, ctx):
        await ctx.send("The word was: {}".format(self.randomWord), delete_after=15)
        #self.randomWord = ''.join(sample(self.wordsList, 1))
        self.randomWord = random.choice(list(open(self.easyWordsListPath))).rstrip("\n")
        await ctx.send("A new random word has been generated. Good luck.", delete_after=15)
        await self.guessedWordsMsg.delete()
        self.guessedWordsMsg = None
        await ctx.message.delete()

    @commands.command(brief="Returns synonyms", help=" e.g. .synonyms good, would return synonyms for the word good.", aliases=['synonym'])
    async def synonyms(self, ctx, *, word):
        synonymsForWord = []
        for syn in wordnet.synsets(word):
             for name in syn.lemma_names():
                 synonymsForWord.append(name)

        for x in synonymsForWord:
            if x == word:
                synonymsForWord.remove(x)

        await ctx.send("Synonyms for: {}\n{}".format(word, synonymsForWord), delete_after=45)
        await ctx.message.delete()

    @commands.command(brief="Returns antonyms", help=" e.g. .antonyms good, would return antonyms for the word good.", aliases=['antonym'])
    async def antonyms(self, ctx, *, word):
        antonymsForWord = []
        for syn in wordnet.synsets(word): 
            for l in syn.lemmas(): 
                if l.antonyms(): 
                    antonymsForWord.append(l.antonyms()[0].name()) 

        for x in antonymsForWord:
            if x == word:
                antonymsForWord.remove(x)

        await ctx.send("Antonyms for: {}\n{}".format(word, antonymsForWord), delete_after=45)
        await ctx.message.delete()

    @commands.command(brief="Returns definition of a word", aliases=['getDefinition', 'getdef', 'def'])
    async def definition(self, ctx, *, word):
        syns = wordnet.synsets(word)
        await ctx.send("Definition of {} is:\n{}".format(word, syns[0].definition()), delete_after=15) # Går nogengange out of index range.
        await ctx.message.delete()

def setup(bot):
    bot.add_cog(DictionaryCog(bot))

