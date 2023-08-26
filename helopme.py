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
        self.bot = bot
        self.players_joined_message = ''
        self.num_players = None
        self.num_werewolves = None

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
        if arg1 is None:
            return
        if arg1.lower() in ["h", "help"]:
            await ctx.send("Usage: /test_play [total number of players] [number of werewolves]")
            print('help')
            return
        print('outside first if')
        nickname = ctx.author.nick
        username = ctx.author

        button_join = Button(label="Join Game", style=discord.ButtonStyle.blurple)
        button_start = Button(label="Start Game", style=discord.ButtonStyle.green, disabled=False)
        button3 = Button(label="Warning: I'm broken, Cancel", style=discord.ButtonStyle.red)

        print('set up callback')

        # num of player conditions
        if arg2 is not None:
            print('arg2 is not None')
            if self.valid_player_numbers(int(arg1), int(arg2)):
                players_joined = 0

                # await ctx.send(str(ctx.author)+" wants to start a game with "+arg1+" players and "+arg2+" werewolves.")

                button_join.callback = lambda interaction: self.button_join_callback(interaction)
                button_start.callback = lambda interaction: self.button_start_callback(interaction)
                button3.callback = lambda interaction: self.button_boring_callback(interaction)

                view = View()
                view.add_item(button_join)
                view.add_item(button_start)
                view.add_item(button3)
                # view.remove_item(button)

                num_players_global_blasphemy = 0
                if nickname is not None:
                    start_message = await ctx.send(f"{nickname} ({username}) has started a {arg2} werewolf game! 🐺")
                else:
                    start_message = await ctx.send(f"{username} has started a {arg2} werewolf game! 🐺")

                players_joined_message = await ctx.send(f"{players_joined}/{arg1} players joined")
                button_message = await ctx.send(view=view)

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
        self.players_joined_message.edit(content=(f"15/{arg1} players joined"))
        # players_joined += 1
        # print(players_joined)
        # message = await interaction.original_response()
        # await message.edit()

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
