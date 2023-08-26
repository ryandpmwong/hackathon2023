# bot.py
import os

import discord
from discord import app_commands
from discord.ext import commands
from dotenv import load_dotenv
from discord import ChannelType
import responses
import model

# Define all our constants here (and only constants!)


load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')

client = discord.Client(intents=discord.Intents.default())  # can this go into run_werebot function?


class WereWolfBot(discord.Client):
    pass
    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #
    # async def on_ready(self):
    #     for guild in client.guilds:
    #         if guild.name == GUILD:
    #             break
    #
    #     print(
    #         f'{client.user} is connected to the following guild:\n'
    #         f'{guild.name}(id: {guild.id})'
    #     )
    #
    #     print("Guild members:")
    #     for member in guild.members:
    #         print(f"- {member.name}\n")


class Round():
    def __init__(self, players):
        self.attacked = None
        self.protected = None
        self.players = players

    def construct_werewolf_options(self) -> list:
        options = []
        for player in self.players:
            if player.is_alive() and self.players[player] != 'werewolf':
                options.append(discord.SelectOption(label=player.username, description='Vote to kill ' + player.username))
        return options

    async def werewolf_select(self, idk, options):
        select = Select(placeholder="Vote for a player to kill", options=options)
        view = View()
        view.add_item(select)

        async def werewolf_callback(interaction):
            await interaction.response.send_message(f"Werewolf chose: {select_values[0]}")
            
        await idk.send("Vote for a player to kill", view=view)

    def run_night(self):
        werewolf_options = construct_werewolf_options()
        # type "Start of night [night_number]:" in the werewolf channel
        # put the werewolf select in the werewolf channel
        # do stuff depending on what the werewolves voted for

    def run_day(self):
        pass


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


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content == 'hello':
        await message.channel.send('Hi~')


client.run(TOKEN)  # I think this should also go inside run_werebot


def run_werebot():

    pass

async def create_game_threads(channel_id):
    # when command is trigerred
    # store number of running games
    game_id = "game1"
    message = "Welcome to Werewolf!"
    channel = client.get_channel(int(channel_id))
    # create public thread for all players
    all_players_thread = await channel.create_thread(name = game_id+" everyone", type=ChannelType.private_thread)
    # create werewolf thread
    werewolves_thread = await channel.create_thread(name = game_id+" werewolves", type=ChannelType.private_thread)
    # need player list to populate thread
    '''for wolf in werewolves:
        werewolves_thread.add_user(wolf)'''
    # create dead chat
    dead_thread = await channel.create_thread(name = game_id+" dead", type=ChannelType.private_thread)

def kill_player(user):
    user.timeout()

async def main():
    pass


if __name__ == '__main__':
    main()
