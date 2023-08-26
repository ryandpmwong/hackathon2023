import os

import asyncio
import discord
from discord import app_commands
from discord.ext import commands
from dotenv import load_dotenv
from makeThreads import test_threads

import model

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')


class WereWolfBot(commands.Bot):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.threads = []

    async def on_ready(self):
        print("Ready")

    async def on_message(self, message):
        if message.author == self.user or message.author.bot:
            return

        if message.content == "Make me some threads":
            thread_test = test_threads(message.channel, message.author)
            self.threads.extend(await thread_test.create_game_threads())
            print(self.threads)

        if message.content == "Delete Werewolf threads":
            # thread_test = test_threads(message.channel, message.author)
            for thread in self.threads:
                await thread.delete()
                self.threads.remove(thread)
            # await thread_test.delete_game_threads(message.channel)

        if message.content == "Hi":
            await message.channel.send("Hello~")

        if message.channel.name == 'testing' or message.author.bot:
            await message.channel.send(f"{message.author} has send a message: {message.content}")

    async def on_message_edit(self, before, after):
        if before.channel.name != 'testing' or before.author.bot:
            return
        await before.channel.send(
            f"{before.author} edited a message\n"
            f"before message: {before.content}\n"
            f"after message: {after.content}"
        )


bot = WereWolfBot(
    command_prefix='/',
    description="This is the Game werebot",
    intents=discord.Intents.all()
)
bot.run(TOKEN)
