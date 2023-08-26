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
    async def play_game(self, ctx, arg1: str | None = None, arg2: str | None = None):
        """Runs on /test_play [num players] [num werewolf]"""
        self.num_players = arg1
        self.num_werewolves = arg2
        print('play game')
        ctx.reply("fsghfkjsdafgsudfhsk")
        if arg1 is None:
            ctx.send("arg1 cannot be empty")
            return
        if arg1.lower() in ["h", "help"]:
            await ctx.send("Usage: /test_play [total number of players] [number of werewolves]")
            print('help')
            return
        print('outside first if')

        print('cooking up some butt0ns')
        self.button_join = Button(label="Join Game", style=discord.ButtonStyle.blurple)
        print('button join config done')
        self.button_start = Button(label="Start Game", style=discord.ButtonStyle.green, disabled=True)
        print('button_start_initialized')
        button_cancel = Button(label="Warning: I'm broken, Cancel", style=discord.ButtonStyle.red)
        print('button cancel initialized')

        print('set up callback')

        # num of player conditions
        if arg2 is not None:
            print('arg2 is not None')
            if self.valid_player_numbers(int(arg1), int(arg2)):
                players_joined = 0

                # await ctx.send(str(ctx.author)+" wants to start a game with "+arg1+" players and "+arg2+" werewolves.")

                self.button_join.callback = lambda interaction: self.button_join_callback(interaction)
                self.button_start.callback = lambda interaction: self.button_start_callback(interaction)
                button_cancel.callback = lambda interaction: self.button_boring_callback(interaction)

                view = View()
                view.add_item(self.button_join)
                view.add_item(self.button_start)
                view.add_item(button_cancel)
                # view.remove_item(button)

                if ctx.author.nick is not None:
                    start_message = await ctx.send(
                        f"{ctx.author.nick} ({ctx.author}) has started a {self.num_werewolves} werewolf game! 🐺")
                else:
                    start_message = await ctx.send(f"{ctx.author} has started a {self.num_werewolves} werewolf game! 🐺")

                self.players_joined_message = await ctx.send(f"{self.players_joined}/{self.num_players} players joined")
                self.button_message = await ctx.send(view=view)

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
        self.players_joined_message.edit(content=f"{self.players_joined}/{self.num_players} players joined")
        if self.players_joined == self.num_players:
            self.button_start.disabled = False
            self.button_join.disabled = True

    async def button_start_callback(self, interaction):
        await interaction.response.send_message(f"Sleep is great for you")
        message = await interaction.original_response()
        # print(message)
        # await interaction.edit_original_response("New or old message first method?")
        await message.edit(content="There is no sleep in Ba Sing Se")

    async def button_boring_callback(self, interaction):
        await interaction.response.send_message("Oh. You clicked the other button.")

    def valid_player_numbers(self, total, werewolves):
        good = total - werewolves
        if werewolves >= good:
            return False
        else:
            return True


async def setup(the_bot):
    await the_bot.add_cog(MakeButtons(the_bot))
