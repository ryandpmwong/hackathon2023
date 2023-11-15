import asyncio
from typing import Optional

import discord
from discord import app_commands
from discord.ui import Button, View
from discord.ext import commands
import discord.ext

from dotenv import load_dotenv
import os

from bot import WereWolfBot
import model
import game_a


load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

intents = discord.Intents.all()
client = discord.Client(intents=intents)
tree = discord.app_commands.CommandTree(client)


# bot = commands.Bot(command_prefix="/", intents=discord.Intents.all())
# bot = WereWolfBot(command_prefix='/', intents=discord.Intents.all())

class JoinView(View):
    def __init__(self, callbacks, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.button_join = Button(
            label="Join Game", 
            style=discord.ButtonStyle.blurple
        )
        self.button_start = Button(
            label="Start Game", 
            style=discord.ButtonStyle.green, 
            disabled=True
        )
        self.button_cancel = Button(
            label="Warning: I'm broken, Cancel", 
            style=discord.ButtonStyle.red
        )

        self.button_join.callback = callbacks["button_join"]
        self.button_start.callback = callbacks["button_start"]
        self.button_cancel.callback = callbacks["button_cancel"]

        self.add_item(self.button_join)
        self.add_item(self.button_start)
        self.add_item(self.button_cancel)

    def enable_start(self):
        self.button_join.disabled = True
        # self.button_join.label("I don't know what's going on")
        self.button_start.disabled = False
        self.reset_view()

    def disable_start(self):
        self.button_start.disabled = True
        self.reset_view()

    def reset_view(self):
        # Needs to edit message view created in or no changes will be made
        self.clear_items()
        self.add_item(self.button_join)
        self.add_item(self.button_start)
        self.add_item(self.button_cancel)



class MakeButtons(commands.Cog):
    def __init__(self, bot):
        self.players_joined = 0
        self.bot = bot

        # Message where JoinView/messages are created
        self.button_message = None

        # Used to keep track of 'x started a game!' message
        self.game_info = None
        # Using a dict? Don't know what we need to pass tbh
        self.players = []

        self.num_players = None
        self.num_werewolves = None

        self.game_started = False

        # self.button_start = None
        # self.button_join = None
        # self.button_cancel = None
        # self.view = View()

    # async def create_start_prompt(self):
    #     return

    async def makebuttons(self, interaction: discord.Interaction):
        """
        Makes buttons for voting.
        """
        pass


    @app_commands.command(name='start_game', description="Attempts game start initiation. Must specify werewolves else nothing.")
    @app_commands.describe(
        num_players='number of players',
        num_werewolves='number of werewolves'
    )
    async def start_game(self, interaction, num_players: str, num_werewolves: int | None = None):
        """Creates game start view
        Runs on /start_game [num players] [num werewolf]"""
        ctx = await self.bot.get_context(interaction)
        self.num_players = num_players
        self.num_werewolves = num_werewolves

        if num_players is None:
            ctx.send("num_players cannot be empty")
            return
        
        if num_players.lower() in ["h", "help"]:
            await ctx.send("Usage: /test_play [total number of players] [number of werewolves]")
            return

        # num of player conditions
        # No werewolf auto-sets yet
        if num_werewolves is not None:
            if self.valid_player_numbers(int(num_players), int(num_werewolves)):
                self.players = []

                callbacks = {
                    "button_join": lambda inter: self.button_join_callback(inter),
                    "button_start": lambda inter: self.button_start_callback(inter),
                    "button_cancel": lambda inter: self.button_boring_callback(inter) 
                }

                self.join_view = JoinView(callbacks)
                
                name = name_display(ctx.author.display_name, ctx.author)
                self.game_info = (f"{name} has started a {self.num_werewolves} werewolf game! 🐺\n")

                self.button_message = await ctx.send(
                    content=self.game_info+
                    f"{len(self.players)}/{self.num_players} players joined", 
                    view=self.join_view
                )

            else:
                await ctx.send("Too many werewolves. Please enter a lower amount of werewolves.")

    async def button_join_callback(self, interaction):
        """"""
        # name = name_display(interaction.user.display_name, interaction.user)
        # await interaction.response.send_message(f"{name} has clicked a button! Blasphemous!")
        if interaction.user in self.players:
            await interaction.response.send_message("You've already joined this game.\n*You can't leave, either*.", 
                                                    ephemeral=True)
        else:
            self.players_joined += 1

            self.players.append(interaction.user)
            await self.display_join_info()

            print(f"{len(self.players)}/{self.num_players}")

            if len(self.players) == int(self.num_players):
                print('Enough players!')
                # Disables buttons
                self.join_view.enable_start()
                # Edits button message to update view
                await self.button_message.edit(view=self.join_view)
            await interaction.response.defer()


    async def button_start_callback(self, interaction):
        if len(self.players) != int(self.num_players):
            # Kind of unnecessary due to button disabling.
            await interaction.response.send_message("There aren't enough people, dummy.")

        else:
            self.join_view.disable_start()
            # Edits button message to update view
            await self.button_message.edit(view=self.join_view)

            await interaction.response.send_message(f"Sleep is great for you")
            message = await interaction.original_response()
            # self.reset()
            await message.edit(content="There is no sleep in Ba Sing Se")
            self.game_started = True
            await self.play_game(interaction)


    async def button_boring_callback(self, interaction):
        await interaction.response.send_message("You're meaann (T_T")


    async def display_join_info(self):
        message = self.game_info+f"{len(self.players)}/{self.num_players} players joined\n\n**Joined**: "
        # Too lazy to get better way to find last value
        for i, user in enumerate(self.players):
            message += str(user.display_name)
            if not i+1 == len(self.players):
                message += ", "
        await self.button_message.edit(content=message)
        
    
    async def play_game(self, interaction: discord.Interaction):

        await interaction.channel.send("Starting a new werewolf game~")
        # for name in interaction.channel.members:
        #     if name.bot is False and name.status != discord.Status.offline:
        #         users.append(name)

        # Roping in a bot for debug purposes
        extra_member = interaction.guild.get_member(941350914772574238)
        self.players.append(extra_member)
        extra_member = interaction.guild.get_member(1144545026316177492)
        self.players.append(extra_member)

        new_game = game_a.WerewolfGame(interaction.channel, 
                                       self.players, 
                                       self.num_werewolves)
        await new_game.create_game_threads()

        for user in self.players:
            await new_game.join_game(user)

        await new_game.select_werewolves()

        while await new_game.is_game_over() is False:
            print('Game over: ', await new_game.is_game_over())
            print(list(user.name for user, alive in new_game.alive.items() if alive), 'is alive.')

            if new_game.is_day:
                await new_game.day()

            else:
                await new_game.night()

            new_game.is_day = not new_game.is_day

        await interaction.channel.send(f"Game {new_game.ID} is over. The {await new_game.is_game_over()} have woneth.")
        await new_game.delete()

    # function to manage player number check
    def valid_player_numbers(self, total, werewolves):
        good = total - werewolves
        return True
        # Commented out for test purposes
        # if werewolves >= good:
        #     return False
        # else:
        #     return True


    def has_game_started(self):
        return self.game_started

def name_display(display_name, username):
    """Indicates display name if user has set one
    """
    if display_name:
        return f"**{display_name}** ({username})"
    else:
        return f"**{username}**"

async def setup(the_bot):
    await the_bot.add_cog(MakeButtons(the_bot))
