import asyncio

import discord
from discord
from discord.ext import commands
import bot
import game_a


# This code is now functional


class Play(commands.Cog):
    """
    """
    def __init__(self, the_bot: bot.WereWolfBot):
        # Allows bot to be used for functions
        self.bot = the_bot

    # 
    @discord.slash_command(name="clear_threads", description="Exterminates threads")
    async def clear_threads(self, interaction: discord.Interaction):
        """Deletes threads
        """
        context = await self.bot.get_context(interaction)
        await context.send("Deleting threads")
        for thread in interaction.channel.threads:
            if 'Game' in thread.name:
                await thread.delete()
        await context.respond("All game threads from this channel are deleted.")

    @app_commands.command(name='play_game')
    @app_commands.describe(
        num_werewolves='number of werewolves'
    )

    async def play_game(self, interaction: discord.Interaction, num_werewolves: str = None):
        users = []
        context = await self.bot.get_context(interaction)
        await context.send("Starting a new werewolf game")
        for name in interaction.channel.members:
            if name.bot is False and name.status != discord.Status.offline:
                users.append(name)
        new_game = game_a.WerewolfGame(interaction.channel, users, int(num_werewolves))
        await new_game.create_game_threads()
        for user in users:
            await new_game.join_game(user)
        await new_game.select_werewolves()
        while await new_game.is_game_over() is False:
            print('game over: ', await new_game.is_game_over())
            print(list(user.name for user, alive in new_game.alive.items() if alive), 'is alive.')
            if new_game.is_day:
                await new_game.day()
            else:
                await new_game.night()
            new_game.is_day = not new_game.is_day
        await interaction.channel.send(f"Game{new_game.ID} is over. {await new_game.is_game_over()} had won.")
        await new_game.delete()

    @discord.slash_command(name="check_status")
    async def check_status(self, interaction: discord.Interaction):
        a = await self.bot.get_context(interaction)
        await a.send("Checking member status...")
        for member in interaction.channel.members:
            status = member.status
            await interaction.channel.send(f'{member} is {status}')


async def setup(bot: bot.WereWolfBot):
    await bot.add_cog(Play(bot))
