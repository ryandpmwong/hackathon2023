import os

import asyncio
import discord
from discord import app_commands
from discord.ext import commands
from discord.ui import Button, View
from dotenv import load_dotenv
from makeThreads import test_threads
import promptView

import model
import game

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')


class WereWolfBot(commands.Bot):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.game_dict = {}

    async def on_ready(self):
        print(f"{self.user} is ready and on the roll")

    async def on_message(self, message):
        if message.author.bot:
            return

        if message.content == "Make me some threads":
            new_game = game.WerewolfGame(message.channel, message.author)
            await new_game.create_game_threads()
            await new_game.allocate_role(message.author, new_game.threads['villager'])
            await new_game.allocate_role(message.author, new_game.threads['werewolf'])
            await new_game.allocate_role(message.author, new_game.threads['ghost'])
            # add function to ask for player usernames later.
            self.game_dict[new_game.ID] = new_game

        elif message.content == "Delete Werewolf threads":
            pass

        if message.content == "Hi":
            await message.channel.send("Hello~")

        if message.content == "Give me buttons":
            return

        # if message.channel.name == 'testing' and not message.author.bot:
        #     await message.channel.send(f"{message.author} has send a message: {message.content}")

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
