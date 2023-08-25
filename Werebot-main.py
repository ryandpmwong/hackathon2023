# bot.py
import os

import discord
from dotenv import load_dotenv
import responses
import model

# Define all our constants here (and only constants!)


load_dotenv()  # I think this is better to be put inside main - suggestion by Amy
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')

client = discord.Client(intents=discord.Intents.default())  # can this go into run_werebot function?

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


async def main():
    pass


if __name__ == '__main__':
    main()
