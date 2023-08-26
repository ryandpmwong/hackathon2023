import discord
from discord import app_commands
from discord.ext import commands
import model


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
bot.run("MTE0NDU1MTU2OTE3MDM3MDU5Mw.Gkdos6.bwWMYA2Sn150-fLMj13b3O-anD8GP3ogLtshns")

