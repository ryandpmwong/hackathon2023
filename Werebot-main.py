# bot.py
import os

import discord
from discord import app_commands
from discord.ext import commands
from dotenv import load_dotenv
import responses
import model

# Define all our constants here (and only constants!)


load_dotenv()  # I think this is better to be put inside main - suggestion by Amy
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')

client = discord.Client(intents=discord.Intents.default())  # can this go into run_werebot function?


class WereWolfGame(commands.Cog):
    def __init__(self, bot, players: list, game_mode='text'):
        self.bot = bot
        self.player = players
        self.game_model = model.GameModel(len(players), game_mode)

    @app_commands.command()  #apparently this will enable to show us command in discord
    @app_commands.describe(
        number_of_people="The number of people in the game",
        game_mode="Game mode, can be voice or text"
    )
    async def werewolfgame(self, interation: discord.Interaction, number_of_people: int = 5, game_mode: str = 'text'):
        """
        Starts a game of werewolf
        :param interation:
        :param number_of_people:
        :param game_mode:
        :return:
        """


"""
It is best to separate computational functions (with regular def) from async functions, then let the async functions
call the regular functions.
regular function goes below:
"""






"""
Async functions:
"""


@client.event  # probably put in run_werebot?
async def on_ready():
    for guild in client.guilds:
        if guild.name == GUILD:
            break

    print(
        f'{client.user} is connected to the following guild:\n'
        f'{guild.name}(id: {guild.id})'
    )

    print("Guild members:")
    for member in guild.members:
        print(f"- {member.name}\n")
    # print()
    # members = '\n - '.join([member.name for member in guild.members])
    # print(f'Guild Members:\n - {members}')


client.run(TOKEN)  # I think this should also go inside run_werebot


def run_werebot():

    pass

def create_game_threads():
    # when command is trigerred
    # store number of running games
    game_id = "game1"
    message = "Welcome to Werewolf!"
    # create public thread for all players
    all_players_thread = await discord.create_thread(game_id+" everyone", message=message, reason="New Game")
    # create private thread
    werewolves_thread = await discord.create_thread(game_id+" werewolves", message=None, reason="New Game")
    # need player list to populate thread
    '''for wolf in werewolves:
        werewolves_thread.add_user(wolf)'''

async def main():
    pass


if __name__ == '__main__':
    main()
