import discord
from discord.ext import commands
from nltk.corpus import words
from itertools import chain
from nltk.corpus import wordnet
import nltk
# from random import sample
import random
import re


# Remove none used imports
# Hint command ?

# Come up with better name for this cog
# DictionaryCog ?
class DictionaryCog(commands.Cog):
    # Some documentation

    def __init__(self, bot):
        self.bot = bot
        # Hard words list
        # self.wordsList = words.words()
        # self.randomWord = ''.join(sample(self.wordsList, 1))
        self.easyWordsListPath = "C:/Users/Sren/Documents/GitHub/DiscordKarmaBot/easier_words.txt"
        my_file = open(self.easyWordsListPath, 'r')
        self.wordsList = my_file.read()
        self.randomWord = random.choice(list(open(self.easyWordsListPath))).rstrip("\n")
        self.guessedWordsMsg = None
        self.guessedWordsBefore = []
        self.guessedWordsAfter = []
        # nltk.download('words')
        # nltk.download('wordnet')

    @commands.Cog.listener()
    async def on_ready(self):
        print("DictionaryCog cog is loaded")

    @commands.command(help="Just a stupid little game", aliases=['g'])
    async def guess(self, ctx, *, user_guess: str):
        your_word = "Your word"
        print("Random word is:{}".format(self.randomWord))
        if re.search(r'\b{}\b'.format(user_guess), self.wordsList):
            if user_guess == self.randomWord:
                await ctx.send(
                    "The word was indeed {}! Congratz {} you got it".format(self.randomWord, ctx.author.name),
                    delete_after=15)
                await self.guessedWordsMsg.delete()
                self.guessedWordsMsg = None
                self.randomWord = random.choice(list(open(self.easyWordsListPath))).rstrip("\n")
                await ctx.message.delete()
                return
            x = [self.randomWord, user_guess]
            x.sort()
            if x[0] == self.randomWord:
                await ctx.send("The word is before {}".format(user_guess), delete_after=15)
                self.guessedWordsAfter.append(user_guess)
                self.guessedWordsAfter.sort()
                if self.guessedWordsMsg is None:
                    self.guessedWordsMsg = await ctx.send(
                        "Current guessed words:\n {} {} {}".format(self.guessedWordsBefore, your_word,
                                                                   self.guessedWordsAfter))
                else:
                    await self.guessedWordsMsg.edit(
                        content="Current guessed words:\n {} {} {}".format(self.guessedWordsBefore, your_word,
                                                                           self.guessedWordsAfter))
            if x[1] == self.randomWord:
                self.guessedWordsBefore.append(user_guess)
                self.guessedWordsBefore.sort()
                await ctx.send("The word is after {}".format(user_guess), delete_after=15)
                if self.guessedWordsMsg is None:
                    self.guessedWordsMsg = await ctx.send(
                        "Current guessed words:\n {} {} {}".format(self.guessedWordsBefore, your_word,
                                                                   self.guessedWordsAfter))
                else:
                    await self.guessedWordsMsg.edit(
                        content="Current guessed words:\n {} {} {}".format(self.guessedWordsBefore, your_word,
                                                                           self.guessedWordsAfter))
        else:
            await ctx.send("{} is not in the words list!".format(user_guess), delete_after=15)

        await ctx.message.delete()

    @commands.command(brief="Prints out the alphabet for your convenience", aliases=['abc', 'alph'])
    async def alphabet(self, ctx):
        await ctx.send("A B C D E F G H I J K L M N O P Q R S T U V W X Y Z", delete_after=15)
        await ctx.message.delete()

    @commands.command(brief="Resets and generates a new word.")
    async def giveup(self, ctx):
        await ctx.send("The word was: {}".format(self.randomWord), delete_after=15)
        # self.randomWord = ''.join(sample(self.wordsList, 1))
        self.randomWord = random.choice(list(open(self.easyWordsListPath))).rstrip("\n")
        await ctx.send("A new random word has been generated. Good luck.", delete_after=15)
        await self.guessedWordsMsg.delete()
        self.guessedWordsMsg = None
        await ctx.message.delete()

    @commands.command(brief="Returns synonyms", help=" e.g. .synonyms good, would return synonyms for the word good.",
                      aliases=['synonym'])
    async def synonyms(self, ctx, *, word):
        synonyms_for_word = []
        for syn in wordnet.synsets(word):
            for name in syn.lemma_names():
                synonyms_for_word.append(name)

        for x in synonyms_for_word:
            if x == word:
                synonyms_for_word.remove(x)

        await ctx.send("Synonyms for: {}\n{}".format(word, synonyms_for_word), delete_after=45)
        await ctx.message.delete()

    @commands.command(brief="Returns antonyms", help=" e.g. .antonyms good, would return antonyms for the word good.",
                      aliases=['antonym'])
    async def antonyms(self, ctx, *, word):
        antonyms_for_word = []
        for syn in wordnet.synsets(word):
            for l in syn.lemmas():
                if l.antonyms():
                    antonyms_for_word.append(l.antonyms()[0].name())

        for x in antonyms_for_word:
            if x == word:
                antonyms_for_word.remove(x)

        await ctx.send("Antonyms for: {}\n{}".format(word, antonyms_for_word), delete_after=45)
        await ctx.message.delete()

    @commands.command(brief="Returns definition of a word", aliases=['getDefinition', 'getdef', 'def'])
    async def definition(self, ctx, *, word):
        syns = wordnet.synsets(word)
        await ctx.send("Definition of {} is:\n{}".format(word, syns[0].definition()),
                       delete_after=15)  # Går nogengange out of index range.
        await ctx.message.delete()


def setup(bot):
    bot.add_cog(DictionaryCog(bot))
