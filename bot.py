import os

import asyncio
import discord
import discord.ext
from discord import app_commands
from discord.ext import commands
from discord.ui import Button, View
from dotenv import load_dotenv
from makeThreads import test_threads

import model
import game

MAKE_THREADS = "Make me some threads"
# CLEAR_THREADS = "Clear all threads"
CLEAR_THREADS = "/cthreads"
GREETINGS = "hi hello good evening good morning good night greeting welcome"
DISCORD_GUILD = "Hackathon 2023"


"""users = [async for member in ctx.guild.fetch_members(limit=None):
            print("{},{}".format(member,member.id), file=f,)]"""

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')


class WereWolfBot(commands.Bot):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.game_dict = {}

    async def on_ready(self):
        print(f"{self.user} is ready and on the roll")
        # Comment out later, otherwise dies
        # await self.tree.sync(guild=None)
        # print('Synced tree')


    async def on_message(self, message):
        """Sends a mocking message to you if you comment in a channel named 'testing'.
        Ignores bots.

        Args:
            message: message sent in channel
        """
        # If the author is a bot, do not do anything
        if message.author.bot:
            return

        if message.channel.name == 'testing' and not message.author.bot:
            # Allows you to make threads
            await self.handle_responses(message)

            # Rest is decorative (not useful for game)
            #await message.channel.send(f"{message.author} has send a message: {message.content}")
            insult = f"The *better* were-bot: {message.author} sent '"
            # inefficient insult generator code
            words_sent = (message.content).split(" ")
            for word in words_sent:
                new_word = ""
                for letter_num, letter in enumerate(word):
                    if letter_num % 2 == 1:
                        letter = letter.upper()
                    else:
                        letter = letter.lower()
                    new_word += letter
                if word == words_sent[-1]:
                    insult = insult + new_word + "'"
                else:
                    insult = insult + new_word + " "

            await message.channel.send(insult)


    async def handle_responses(self, message):
        # Gets what the content of the message is
        print(message.content)
        # If it is the Make threads message
        ###### BEGINNING OF GAME - MAKE THE THREADS #######
        if message.content == MAKE_THREADS:
            # It makes a new game, importing from game.py, giving the channel and who wrote the message
            users = []
            for user in message.guild.members:
                if not user.bot:
                    users.append(user)
            new_game = game.WerewolfGame(message.channel, users)
            print('made new game')
            # Creates new threads
            # so if we did something like    threads = await new_game.create_game_threads()
            # then the variable "threads" can be passed back to GameModel???
            await new_game.create_game_threads()
            await new_game.generate_players(users)
            await message.channel.send(await new_game.run_game())

        elif message.content == "/sync please":
            await self.tree.sync()
            await message.channel.send("Tree synced? Maybe? ;_;")

        # Thread clearing (clears all the threads in a channel)
        elif message.content == CLEAR_THREADS:
            for thread in message.channel.threads:
                await thread.delete()
            await message.channel.send("The threads be gone")

        elif message.content == "List names":
            for user in message.guild.members:
                await message.channel.send(user.name)
            await message.channel.send("All names given")
        
        # Just is happy to greet you
        elif message.content.lower() in GREETINGS:
            await message.channel.send(message.content + '~')
        else:
            p_message = message.content.split(' ')

            if p_message[0] == "Remove" and len(p_message) == 2:
                user_id = int(p_message[1])
                user = self.get_user(user_id)
                # need to convert to user id somehow
                await self.game_dict[0].deallocate_role(user, message.channel)
            elif len(p_message) == 3 and p_message[0] == 'Delete' and (p_message[1] == 'threads'):
                game_id = int(p_message[2])
                try:
                    await self.game_dict.get(game_id).delete()
                except AttributeError:
                    await message.channel.send("This game has already been deleted or hadn't been created")


    async def on_message_edit(self, before, after):
        if before.channel.name != 'testing' or before.author.bot:
            return
        await before.channel.send(
            f"{before.author} edited a message\n"
            f"before message: {before.content}\n"
            f"after message: {after.content}"
        )

# bot = WereWolfBot(
#     command_prefix='/',
#     description="This is the Game werebot",
#     intents=discord.Intents.all()
# )
# bot.run(TOKEN)
