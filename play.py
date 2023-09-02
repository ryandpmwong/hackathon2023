import asyncio

import discord
from discord import app_commands
from discord.ext import commands
import bot
import game_a

# This code is for testing purposes and is not functional.

class Play(commands.Cog):
    def __init__(self, the_bot: bot.WereWolfBot):
        self.bot = the_bot

    @app_commands.command(name="clear_threads")
    async def clear_threads(self, interaction: discord.Interaction):
        context = await self.bot.get_context(interaction)
        await context.send("Deleting threads")
        for thread in interaction.channel.threads:
            if 'Game' in thread.name:
                await thread.delete()
        await context.send("All game threads from this channel are deleted.")

    @app_commands.command(name='play_game')
    async def play_game(self, interaction: discord.Interaction):
        users = []
        context = await self.bot.get_context(interaction)
        await context.send("Starting a new werewolf game")
        for name in interaction.channel.members:
            if name.bot is False and name.status == discord.Status.online:
                users.append(name)
        new_game = game_a.WerewolfGame(interaction.channel, users)
        await new_game.create_game_threads()
        for user in users:
            await new_game.join_game(user)
        await new_game.select_werewolves()
        while await new_game.is_game_over() is False:
            if new_game.is_day:
                await new_game.day()
            else:
                await new_game.night()
            new_game.is_day = not new_game.is_day
        await interaction.channel.send(f"Game{new_game.ID} is over. {await new_game.is_game_over()} had won.")
        await new_game.delete()


    @app_commands.command(name="check_status")
    async def check_status(self, interaction: discord.Interaction):
        a = await self.bot.get_context(interaction)
        await a.send("Checking member status...")
        for member in interaction.channel.members:
            status = member.status

            await interaction.channel.send(f'{member} is {status}')



async def setup(bot: bot.WereWolfBot):
    await bot.add_cog(Play(bot))
