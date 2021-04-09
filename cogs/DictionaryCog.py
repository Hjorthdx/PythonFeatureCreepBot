import discord
from discord.ext import commands
from nltk.corpus import words
from itertools import chain
from nltk.corpus import wordnet
import nltk
# from random import sample
import random
import re
from Constants import *


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
        self.easy_words_wist_path = "C:/Users/Sren/PycharmProjects/DiscordFeatureCreepBot/easier_words.txt"
        my_file = open(self.easy_words_wist_path, 'r')
        self.words_list = my_file.read()
        self.random_word = random.choice(list(open(self.easy_words_wist_path))).rstrip("\n")
        self.guessed_words_msg = None
        self.guessed_words_before = []
        self.guessed_words_after = []
        self.your_word = "Your word"
        # nltk.download('words')
        # nltk.download('wordnet')

    @commands.Cog.listener()
    async def on_ready(self):
        print("DictionaryCog cog is loaded")

    @commands.command(help="Just a stupid little game", aliases=['g'])
    async def guess(self, ctx, *, user_guess: str):
        your_word = "Your word"
        print("Random word is: {}".format(self.random_word))
        result = self._guess(user_guess)
        if result == 0:
            await ctx.send(f"The word: {user_guess} has already been guessed!", delete_after=CONSTANT_SHORT_DELETE_AFTER_TIME)
        elif result == 1:
            await ctx.send(
                "The word was indeed {}! Congratz {} you got it".format(self.random_word, ctx.author.name),
                delete_after=CONSTANT_SHORT_DELETE_AFTER_TIME)
            await self._reset()
        elif result == 2:
            await ctx.send("The word is before {}".format(user_guess), delete_after=CONSTANT_SHORT_DELETE_AFTER_TIME)
            await self._update_guessed_words_message(ctx)
        elif result == 3:
            await ctx.send("The word is after {}".format(user_guess), delete_after=CONSTANT_SHORT_DELETE_AFTER_TIME)
            await self._update_guessed_words_message(ctx)
        elif result == 4:
            await ctx.send("{} is not in the words list!".format(user_guess), delete_after=CONSTANT_SHORT_DELETE_AFTER_TIME)

    def _guess(self, user_guess: str):
        print("Random word is: {}".format(self.random_word))  # Just for debugging
        if user_guess in self.guessed_words_before or user_guess in self.guessed_words_after:
            return 0
        if re.search(r'\b{}\b'.format(user_guess), self.words_list):
            if user_guess == self.random_word:
                return 1  # We have guessed the word correctly.
            x = [self.random_word, user_guess]
            x.sort()
            if x[0] == self.random_word:
                self.guessed_words_after.append(user_guess)
                self.guessed_words_after.sort()
                return 2  # Guess before the random word.
            if x[1] == self.random_word:
                self.guessed_words_before.append(user_guess)
                self.guessed_words_before.sort()
                return 3  # Guess after the random word.
        else:
            return 4  # Word not in word list.

    async def _update_guessed_words_message(self, ctx):
        if self.guessed_words_msg is None:
            self.guessed_words_msg = await ctx.send(
                "Current guessed words:\n {} {} {}".format(self.guessed_words_before, self.your_word,
                                                           self.guessed_words_after))
        else:
            await self.guessed_words_msg.edit(
                content="Current guessed words:\n {} {} {}".format(self.guessed_words_before, self.your_word,
                                                                   self.guessed_words_after))

    @commands.command(brief="Prints out the alphabet for your convenience", aliases=['abc', 'alph'])
    async def alphabet(self, ctx):
        await ctx.send("A B C D E F G H I J K L M N O P Q R S T U V W X Y Z", delete_after=CONSTANT_VERY_LONG_DELETE_AFTER_TIME)

    @commands.command(name="giveup", brief="Resets and generates a new word.")
    async def give_up(self, ctx):
        await ctx.send("The word was: {}".format(self.random_word), delete_after=CONSTANT_SHORT_DELETE_AFTER_TIME)
        await self._reset()
        await ctx.send("A new random word has been generated. Good luck.", delete_after=CONSTANT_SHORT_DELETE_AFTER_TIME)

    async def _reset(self):
        self.random_word = random.choice(list(open(self.easy_words_wist_path))).rstrip("\n")
        await self.guessed_words_msg.delete()
        self.guessed_words_msg = None

    @commands.command(brief="Returns synonyms", help=" e.g. .synonyms good, would return synonyms for the word good.",
                      aliases=['synonym'])
    async def synonyms(self, ctx, *, word):
        synonyms_for_word = self._synonyms(word)
        await ctx.send("Synonyms for: {}\n{}".format(word, synonyms_for_word), delete_after=CONSTANT_LONG_DELETE_AFTER_TIME)

    @staticmethod
    def _synonyms(word):
        synonyms_for_word = []
        for syn in wordnet.synsets(word):
            for name in syn.lemma_names():
                synonyms_for_word.append(name)

        for x in synonyms_for_word:
            if x == word:
                synonyms_for_word.remove(x)

        return synonyms_for_word

    @commands.command(brief="Returns antonyms", help=" e.g. .antonyms good, would return antonyms for the word good.",
                      aliases=['antonym'])
    async def antonyms(self, ctx, *, word):
        antonyms_for_word = self._antonyms(word)
        await ctx.send("Antonyms for: {}\n{}".format(word, antonyms_for_word), delete_after=CONSTANT_LONG_DELETE_AFTER_TIME)

    @staticmethod
    def _antonyms(word):
        antonyms_for_word = []
        for syn in wordnet.synsets(word):
            for l in syn.lemmas():
                if l.antonyms():
                    antonyms_for_word.append(l.antonyms()[0].name())

        for x in antonyms_for_word:
            if x == word:
                antonyms_for_word.remove(x)

        return antonyms_for_word

    @commands.command(brief="Returns definition of a word", aliases=['getDefinition', 'getdef', 'def'])
    async def definition(self, ctx, *, word):
        syns = wordnet.synsets(word)
        try:
            await ctx.send("Definition of {} is:\n{}".format(word, syns[0].definition()), delete_after=CONSTANT_SHORT_DELETE_AFTER_TIME)
        except IndexError:
            print(f"Got the error here with the word {word}.") #  Not sure if this is me making the error or what it is.
            await ctx.send("Index out of range error", delete_after=CONSTANT_SHORT_DELETE_AFTER_TIME)


def setup(bot):
    bot.add_cog(DictionaryCog(bot))
