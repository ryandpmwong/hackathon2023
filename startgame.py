import asyncio

import discord
from discord.ui import Button, View
from discord.ext import commands
import discord.ext
from discord import app_commands
from dotenv import load_dotenv
import os

from bot import WereWolfBot
# from button import MakeButtons
from button2 import MakeButtons

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

intents = discord.Intents.all()
client = discord.Client(intents=intents)
tree = discord.app_commands.CommandTree(client)


class StartGame(commands.Cog):
    def __init__(self, bot: WereWolfBot):
        self.button_message = None
        self.bot = bot
        self.view = None
        self.current_game = None

    @app_commands.command(name='new_game', description="I don't work. Use /start_game instead.")
    @app_commands.describe(
        num_players='number of players',
        num_werewolves='number of werewolves'
    )
    async def new_game(self, interaction: discord.Interaction, num_players: str, num_werewolves: str|None):
        context = await self.bot.get_context(interaction)
        await context.send(f"Trying to players {num_players} werewolves {num_werewolves}...")

        # self.view = MakeButtons(int(num_players), int(num_werewolves), self.bot)
        # await context.send("A new game is started")
        # self.button_message = await context.send(view=self.view)

    @app_commands.command(name="dm_me", description="Does this work?")
    @app_commands.describe(
        arg1 = "Something to say"
    )
    async def tester(self, interaction: discord.Interaction, arg1: str):
        user = interaction.user
        await user.send("?????")
        await user.send(arg1)

    
    @app_commands.command(name='sync', description='Sync bot commands maybe')
    async def sync(self, interaction: discord.Interaction):
        print(interaction.user)
        if str(interaction.user) == "insomniac.crow":
            await self.bot.tree.sync()
            await interaction.response.send_message('Command tree synced.')
        else:
            await interaction.response.send_message('You must be insomniac.crow to use this command! Or at least add yourself.')


async def setup(bot):
    await bot.add_cog(StartGame(bot))
