from button import MakeButtons
import asyncio

import discord
from discord.ui import Button, View
from discord.ext import commands
import discord.ext
from dotenv import load_dotenv
import os
from bot import WereWolfBot
from discord import app_commands
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

    @app_commands.command(name='newgame')
    @app_commands.describe(
        num_players='number of players',
        num_werewolves='number of werewolves'
    )
    async def newgame(self, interaction: discord.Interaction, num_players: str|None, num_werewolves: str|None):
        context = await self.bot.get_context(interaction)
        await context.send("Hi")
        self.view = MakeButtons(int(num_players), int(num_werewolves))
        await context.send("Hiii")
        self.button_message = await context.send(view=self.view)


async def setup(bot):
    await bot.add_cog(StartGame(bot))
