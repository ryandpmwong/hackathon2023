import asyncio
import logging
import os
from dotenv import load_dotenv
import random

import discord

from bot import WereWolfBot

load_dotenv()
TOKEN = os.environ.get('DISCORD_TOKEN')



description = "I am an amazing bot, YES."


async def main():
    intents = discord.Intents.all()
    client = discord.Client(intents=intents)

    activities = [
        discord.Game(name="with my food"),
        discord.Activity(type=discord.ActivityType.listening, name="the screams of my victims"),
        discord.Activity(type=discord.ActivityType.watching, name="yet another execution"),
        discord.Activity(type=discord.ActivityType.watching, name="the wrong people die"),
        discord.Game(name="Werewolf, I wish.")
    ]

    bot = WereWolfBot(
        command_prefix="/",
        description=description,
        intents=intents,
        activity=activities[random.randint(0, len(activities)-1)]
    )
    cogs = [
        'startgame',
        'play',
        'button'
    ]

    for cog in cogs:
        await bot.load_extension(f'{cog}')

    await bot.start(TOKEN)


asyncio.run(main())
