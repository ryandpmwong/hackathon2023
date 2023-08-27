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
CLEAR_THREADS = "Clear all threads"
GREETINGS = "hi hello good evening good morning good night greeting welcome"




load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')


class WereWolfBot(commands.Bot):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.game_dict = {}

    async def on_ready(self):
        print(f"{self.user} is ready and on the roll")
        await self.tree.sync()
        print('Synced tree')

    async def on_message(self, message):
        if message.author.bot:
            return

        if message.channel.name == 'testing' and not message.author.bot:
            await message.channel.send(f"{message.author} has send a message: {message.content}")
            await self.handle_responses(message)




    async def handle_responses(self, message):
        print(message.content)
        if message.content == MAKE_THREADS:
            #replace message.author with list of players
            new_game = game.WerewolfGame(message.channel, message.author)
            # so if we did something like    threads = await new_game.create_game_threads()
            # then the variable "threads" can be passed back to GameModel???
            await new_game.create_game_threads()
        elif message.content == CLEAR_THREADS:
            for thread in message.channel.threads:
                await thread.delete()
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
