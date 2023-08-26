import discord
from discord import app_commands
from discord.ext import commands
import bot

class Play(commands.Cog):
    def __init__(self, bot:commands.Bot):
        self.bot = bot

    @app_commands.command(name="play2")
    async def play_game(self, interaction: discord.Interaction):
        print("testing 123")

async def setup(bot: bot.WereWolfBot):
    await bot.add_cog(Play(bot))

