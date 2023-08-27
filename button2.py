import asyncio
from typing import Any

import discord
from discord import Interaction
from discord._types import ClientT
from discord.ui import Button, View
from discord.ext import commands
import discord.ext
from dotenv import load_dotenv
import os
from bot import WereWolfBot
from discord import app_commands

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

intents = discord.Intents.all()
client = discord.Client(intents=intents)
tree = discord.app_commands.CommandTree(client)


# bot = commands.Bot(command_prefix="/", intents=discord.Intents.all())
# bot = WereWolfBot(command_prefix='/', intents=discord.Intents.all())



class MakeButtons(View):
    def __init__(self, num_players, num_werewolves, bot: WereWolfBot):
        super().__init__()
        self.bot = bot
        self.players_joined = 0
        self.message = None
        self.num_players = num_players
        self.num_werewolves = num_werewolves
        self.button_start = None
        self.button_join = None
        self.button_cancel = None

    # async def create_start_prompt(self):
    #     return

        @discord.ui.button(label="Join Game", style=discord.ButtonStyle.blurple)
        async def join_game(interaction, button: Button):
            await interaction.response.send_message(f"{bot.get_user(interaction)} just join")
            self.players_joined += 1
            if self.num_players == self.players_joined:
                button.disabled = True
            user = bot.get_user(interaction)
            return user

        # @discord.ui.button(label="Start Game", style=discord.ButtonStyle.green, disabled=True)
        # async def start_game(interaction, button):
        #     await interaction.response.send_message.(f"{bot.get_user(interaction)} clicked start")
        #
        #
        # @discord.ui.button(label="Terminate", style=discord.ButtonStyle.danger)
        # async def terminate(interaction, button):
        #     await
        #

