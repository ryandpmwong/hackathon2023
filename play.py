import asyncio

import discord
from discord import app_commands
from discord.ext import commands
import bot
import game_a


# This code is now functional


class Play(commands.Cog):
    def __init__(self, the_bot: bot.WereWolfBot):
        self.bot = the_bot

    @app_commands.command(name="clear_threads", description="Clears all threads in current channel.")
    async def clear_threads(self, interaction: discord.Interaction):
        context = await self.bot.get_context(interaction)
        await context.send("Deleting threads")
        for thread in interaction.channel.threads:
            if 'Game' in thread.name:
                await thread.delete()
        await context.send("All game threads from this channel are deleted.")

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

    @app_commands.command(name="check_status", description="Returns all server members and online status.")
    async def check_status(self, interaction: discord.Interaction):
        a = await self.bot.get_context(interaction)
        await a.send("Checking member status...")
        for member in interaction.channel.members:
            status = member.status
            await interaction.channel.send(f'{member} is {status}')

    @app_commands.command(name="help", description="Show help about the bot")
    async def help(self, interaction: discord.Interaction):
        """displays a list of available commands to the user"""
        await interaction.channel.send("Here is a list of commands use can use. Type /[command] help for more info."
                    "\n/start_game \n/clear_threads \nOthers I'm not bothered to write up")
        
    @app_commands.command(name="skip", description="Non-functional")
    async def skip(self, interaction: discord.Interaction):
        """adds to skip counter, if 75% of players have used /skip then discussion session ends immediately"""
        pass

    @app_commands.command(name="game_help", description="Non-functional.")
    async def game_help(self, interaction: discord.Interaction):
        "presents the rules of the game"
        # await ctx.send("")
        pass

    @app_commands.command(name="create_roles", description="Might give you a role.")
    async def create_roles(self, interaction: discord.Interaction):
        guild = interaction.user.guild
        user = interaction.user
        #guild = self.client.get_guild(GuildID) # GET GUILD SOMEHOWWW
        await guild.create_role(name="Alive", permissions=discord.Permissions(permissions=0x0000004000000000)) # Permission Send messages in threads
        await interaction.channel.send("Alive role created!")
        role = discord.utils.get(interaction.guild.roles, name="Alive")
        await user.add_roles(role)
        await interaction.channel.send(f"Alive role given to {user}!")

    @app_commands.command()
    async def delete_roles(self, interaction: discord.Interaction):
        user = interaction.user
        guild = interaction.user.guild
        # OR role = discord.utils.get(ctx.guild.roles, name="Alive") ?
        role = discord.utils.get(guild.roles, name="Alive")
        #await client.add_roles(user, role)
        await user.remove_roles(role)
        await interaction.channel.send(f"Alive role taken from {user}!")
        await role.delete()
        await interaction.channel.send(f"Alive role taken from guild(?)")


async def setup(bot: bot.WereWolfBot):
    await bot.add_cog(Play(bot))
