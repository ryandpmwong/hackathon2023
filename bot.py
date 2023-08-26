import os

import discord
from discord import app_commands
from discord.ext import commands
from dotenv import load_dotenv

import model

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
class WereWolfBot(commands.Bot):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    async def on_ready(self):
        print("Ready")

    async def on_message(self, message):
        if message.author == self.user:
            return

        if message.content == "Hi":
            await message.channel.send("Hello~")
        print(message)
        if message.channel.name == 'testing':
            await message.channel.send(f"{message.author} has send a message: {message.content}")

    async def on_message_edit(self, before, after):
        if before.channel.name != 'testing':
            return
        await before.channel.send(
            f"{before.author} edited a message\n"
            f"before message: {before.content}\n"
            f"after message: {after.content}"
        )




#
# bot = WereWolfBot(
#     command_prefix='/',
#     description="This is the Game werebot",
#     intents=discord.Intents.all()
# )
# bot.run(TOKEN)

