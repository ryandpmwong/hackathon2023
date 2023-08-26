import asyncio

import discord
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


class MakeButtons(commands.Cog):
    def __init__(self, bot):
        self.players_joined = 0
        self.button_message = None
        self.bot = bot
        self.players_joined_message = None
        self.num_players = None
        self.num_werewolves = None
        self.button_start = None
        self.button_join = None
        self.button_cancel = None
        self.view = View()

    # async def create_start_prompt(self):
    #     return

    async def makebuttons(self, interaction: discord.Interaction):
        """
        Makes buttons for voting.
        """
        pass

    @app_commands.command(name='helopme')
    @app_commands.describe(
        arg1='number of players',
        arg2='number of werewolves'
    )
    async def helopme(self, interaction, arg1: str | None = None, arg2: str | None = None):
        """Runs on /test_play [num players] [num werewolf]"""
        ctx = await self.bot.get_context(interaction)
        self.num_players = arg1
        self.num_werewolves = arg2
        if arg1 is None:
            ctx.send("arg1 cannot be empty")
            return
        if arg1.lower() in ["h", "help"]:
            await ctx.send("Usage: /test_play [total number of players] [number of werewolves]")
            return

        self.button_join = Button(label="Join Game", style=discord.ButtonStyle.blurple)
        print(self.button_join)
        self.button_start = Button(label="Start Game", style=discord.ButtonStyle.green, disabled=True)
        self.button_cancel = Button(label="Warning: I'm broken, Cancel", style=discord.ButtonStyle.red)


        # num of player conditions
        if arg2 is not None:
            if self.valid_player_numbers(int(arg1), int(arg2)):
                self.players_joined = 0

                self.button_join.callback = lambda inter: self.button_join_callback(inter)
                self.button_start.callback = lambda inter: self.button_start_callback(inter)
                self.button_cancel.callback = lambda inter: self.button_boring_callback(inter)

                self.view.add_item(self.button_join)
                self.view.add_item(self.button_start)
                self.view.add_item(self.button_cancel)

                if ctx.author.nick is not None:
                    start_message = await ctx.send(
                        f"{ctx.author.nick} ({ctx.author}) has started a {self.num_werewolves} werewolf game! 🐺")
                else:
                    start_message = await ctx.send(f"{ctx.author} has started a {self.num_werewolves} werewolf game! 🐺")

                self.players_joined_message = await ctx.send(f"{self.players_joined}/{self.num_players} players joined")
                self.button_message = await ctx.send(view=self.view)

            else:
                await ctx.send("Too many werewolves. Please enter a lower amount of werewolves.")

    # function to manage player number check

    async def button_join_callback(self, interaction):
        """Prints username/nicknames and a message"""
        nickname = interaction.user.nick
        username = interaction.user
        if nickname is None:
            await interaction.response.send_message(f"{username} has clicked a button! Blasphemous!")
        else:
            await interaction.response.send_message(f"{nickname} ({username}) has clicked a button! Blasphemous!")
        self.players_joined += 1
        await self.players_joined_message.edit(content=f"{self.players_joined}/{self.num_players} players joined")
        print(self.players_joined, self.num_players)
        if int(self.players_joined) == int(self.num_players):
            print('Yes')

            self.button_start.disabled = False
            print(self.button_join)
            self.button_join.label("I don't know what's going on")
            self.button_join.disabled = True
            self.reset_view()

    async def button_start_callback(self, interaction):
        await interaction.response.send_message(f"Sleep is great for you")
        message = await interaction.original_response()
        self.reset()
        await message.edit(content="There is no sleep in Ba Sing Se")

    async def button_boring_callback(self, interaction):
        await interaction.response.send_message("Oh. You clicked the other button.")


    def valid_player_numbers(self, total, werewolves):
        good = total - werewolves
        if werewolves >= good:
            return False
        else:
            return True

    def reset(self):
        self.button_start = None
        self.button_join = None
        self.button_message = None
        self.num_players = None
        self.num_werewolves = None
        self.players_joined = 0
        self.players_joined_message = None
        self.view.clear_items()

    def reset_view(self):
        self.view.clear_items()
        self.view.add_item(self.button_join)
        self.view.add_item(self.button_start)
        self.view.add_item(self.button_cancel)



async def setup(the_bot):
    await the_bot.add_cog(MakeButtons(the_bot))
