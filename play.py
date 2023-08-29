import asyncio

import discord
from discord import app_commands
from discord.ext import commands
import bot
import game

# This code is for testing purposes and is not functional.

class Play(commands.Cog):
    def __init__(self, the_bot: bot.WereWolfBot):
        self.bot = the_bot

    @app_commands.command(name="clear_threads")
    async def clear_threads(self, interaction: discord.Interaction):
        for thread in interaction.channel.threads:
            if 'Game' in thread.name:
                await thread.delete()
        await interaction.channel.send("All game threads from this channel are deleted.")

    @app_commands.command(name='make_threads')
    async def make_threads(self, interaction: discord.Interaction):
        users = []
        for name in interaction.guild.members:
            if name.bot is False:
                users.append(name)
        new_game = game.WerewolfGame(interaction.channel, users)
        print('made new game')
        # Creates new threads
        # so if we did something like    threads = await new_game.create_game_threads()
        # then the variable "threads" can be passed back to GameModel???
        await new_game.create_game_threads()
        print("hello")
        await new_game.generate_players(users)
        print('seems to work up to here')
        await interaction.channel.send(await new_game.run_game())

    @app_commands.command(name="check_status")
    async def check_status(self, interaction: discord.Interaction):
        for member in interaction.channel.members:
            if member.status == discord.Status.online:
                a = await self.bot.get_context(interaction)
                await a.send(f"{member.name} is online")



async def setup(bot: bot.WereWolfBot):
    await bot.add_cog(Play(bot))
