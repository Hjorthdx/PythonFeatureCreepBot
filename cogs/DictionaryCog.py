import discord
from discord.ext import commands
from nltk.corpus import wordnet
import random
import re
import typing


# Hint command ?

class DictionaryCog(commands.Cog, name="Dictionary"):
    """ Dictionary cog that has the responsibility of handling all word related tasks for the user """

    def __init__(self, bot):
        self.bot: discord.client = bot
        self.configuration = bot.get_cog("Configuration")
        self.guessing_game: GuessingGame = GuessingGame()

    @commands.Cog.listener()
    async def on_ready(self):
        print("DictionaryCog cog is loaded")

    @commands.command(help="Just a stupid little game", aliases=['g'])
    async def guess(self, ctx: commands.Context, *, user_guess: str) -> None:
        """ Command with the responsibility of handling a guess in the guess a word game """
        print("Random word is: {}".format(self.guessing_game.random_word))
        if self.guessing_game.is_guessed_before(user_guess):
            await ctx.send(f"The word: {user_guess} has already been guessed!",
                           delete_after=self.configuration.short_delete_after_time)
        elif not self.guessing_game.is_in_word_list(user_guess):
            await ctx.send("{} is not in the words list!".format(user_guess),
                           delete_after=self.configuration.short_delete_after_time)
        elif self.guessing_game.is_correct(user_guess):
            await ctx.send("The word was indeed {}! Congratz {} you got it!".format(self.guessing_game.random_word,
                                                                                    ctx.author.name),
                           delete_after=self.configuration.short_delete_after_time)
            await self.guessing_game.reset()
        elif self.guessing_game.is_before_correct_word(user_guess):
            await ctx.send("The word is before {}".format(user_guess),
                           delete_after=self.configuration.short_delete_after_time)
            await self._update_guessed_words_message(ctx)
        elif self.guessing_game.is_after_correct_word(user_guess):
            await ctx.send("The word is after {}".format(user_guess),
                           delete_after=self.configuration.short_delete_after_time)
            await self._update_guessed_words_message(ctx)

    async def _update_guessed_words_message(self, ctx: commands.Context) -> None:
        """ Updates the current message with all the guessed words """
        if self.guessing_game.guessed_words_msg is None:
            self.guessing_game.guessed_words_msg = await ctx.send(
                "Current guessed words:\n {} {} {}".format(self.guessing_game.guessed_words_before,
                                                           self.guessing_game.your_word,
                                                           self.guessing_game.guessed_words_after))
        else:
            await self.guessing_game.guessed_words_msg.edit(
                content="Current guessed words:\n {} {} {}".format(self.guessing_game.guessed_words_before,
                                                                   self.guessing_game.your_word,
                                                                   self.guessing_game.guessed_words_after))

    @commands.command(brief="Prints out the alphabet for you", aliases=['abc', 'alph'])
    async def alphabet(self, ctx: commands.Context) -> None:
        """ Returns the alphabet for the users """
        await ctx.send("A B C D E F G H I J K L M N O P Q R S T U V W X Y Z",
                       delete_after=self.configuration.very_long_delete_after_time)

    @commands.command(name="giveup", brief="Resets and generates a new word.")
    async def give_up(self, ctx: commands.Context) -> None:
        """ Gives up on the current game of the guessing game and starts a new game """
        await ctx.send("The word was: {}".format(self.guessing_game.random_word),
                       delete_after=self.configuration.short_delete_after_time)
        await self.guessing_game.reset()
        await ctx.send("A new random word has been generated. Good luck.",
                       delete_after=self.configuration.short_delete_after_time)

    @commands.command(brief="Returns synonyms", help=" e.g. .synonyms good, would return synonyms for the word good.",
                      aliases=['synonym'])
    async def synonyms(self, ctx: commands.Context, *, word: str) -> None:
        """ Gets a list of synonyms and sends these to the user """
        synonyms_for_word = self._synonyms(word)
        await ctx.send(f"Synonyms for: {word}\n{synonyms_for_word}",
                       delete_after=self.configuration.long_delete_after_time)

    @staticmethod
    def _synonyms(word: str) -> [str]:
        """ Gets and returns a list of strings with synonyms of a word """
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
    async def antonyms(self, ctx: commands.Context, *, word: str) -> None:
        """ Gets a list of antonyms and sends these to the user """
        antonyms_for_word = self._antonyms(word)
        await ctx.send(f"Antonyms for: {word}\n{antonyms_for_word}",
                       delete_after=self.configuration.long_delete_after_time)

    @staticmethod
    def _antonyms(word: str) -> [str]:
        """ Gets and returns a list of strings with antonyms of a word """
        antonyms_for_word = []
        for syn in wordnet.synsets(word):
            for lemma in syn.lemmas():
                if lemma.antonyms():
                    antonyms_for_word.append(lemma.antonyms()[0].name())

        for x in antonyms_for_word:
            if x == word:
                antonyms_for_word.remove(x)

        return antonyms_for_word

    @commands.command(brief="Returns definition of a word", aliases=['getDefinition', 'getdef', 'def'])
    async def definition(self, ctx: commands.Context, *, word: str) -> None:
        """ Gets and sends the definition of a word to the user """
        syns = wordnet.synsets(word)
        try:
            await ctx.send(f"Definition of {word} is:\n{syns[0].definition()}",
                           delete_after=self.configuration.short_delete_after_time)
        except IndexError:
            print(f"Got the error here with the word {word}.")  # Not sure if this is me making the error or what it is.
            await ctx.send("Index out of range error", delete_after=self.configuration.short_delete_after_time)


def setup(bot):
    bot.add_cog(DictionaryCog(bot))


class GuessingGame:
    """ A single guessing game which is able to handle"""
    def __init__(self):
        self.easy_words_wist_path: str = "C:/Users/Sren/PycharmProjects/DiscordFeatureCreepBot/easier_words.txt"
        my_file = open(self.easy_words_wist_path, 'r')
        self.words_list: str = my_file.read()
        self.random_word: str = random.choice(list(open(self.easy_words_wist_path))).rstrip("\n")
        self.guessed_words_msg: typing.Optional[discord.message] = None
        self.guessed_words_before: [discord.message] = []
        self.guessed_words_after: [discord.message] = []
        self.your_word: str = "Your word"

    def is_guessed_before(self, user_guess: str) -> bool:
        """ Returns true if the word has been guessed before """
        return user_guess in self.guessed_words_before or user_guess in self.guessed_words_after

    def is_correct(self, user_guess: str) -> bool:
        """ Returns whether the guess is the correct word """
        return user_guess == self.random_word

    def is_in_word_list(self, user_guess: str) -> bool:
        """ Returns whether a word is in the words list (Which is kind of our dictionary) """
        if re.search(r'\b{}\b'.format(user_guess), self.words_list):
            return True
        else:
            return False

    def is_before_correct_word(self, user_guess: str) -> bool:
        """ Returns whether the guessed word is before the correct word """
        temp_list = [self.random_word, user_guess]
        temp_list.sort()
        if temp_list[0] == self.random_word:
            self.guessed_words_after.append(user_guess)
            self.guessed_words_after.sort()
            return True

    def is_after_correct_word(self, user_guess: str) -> bool:
        """ Returns whether the guessed word is after the correct word """
        temp_list = [self.random_word, user_guess]
        temp_list.sort()
        if temp_list[1] == self.random_word:
            self.guessed_words_before.append(user_guess)
            self.guessed_words_before.sort()
            return True

    async def reset(self) -> None:
        """ Resets the current game of the guessing game. Deletes all the old messages that is related to the game """
        self.random_word = random.choice(list(open(self.easy_words_wist_path))).rstrip("\n")
        await self.guessed_words_msg.delete()
        self.guessed_words_msg = None
        self.guessed_words_before = []
        self.guessed_words_after = []
