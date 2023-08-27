import asyncio
import logging
import os
from dotenv import load_dotenv

import discord

from bot import WereWolfBot

load_dotenv()
load_dotenv()
TOKEN = os.environ.get('DISCORD_TOKEN')

description = "I am an amazing bot, YES."


async def main():
    intents = discord.Intents.all()
    client = discord.Client(intents=intents)

    bot = WereWolfBot(
        command_prefix="/",
        description=description,
        intents=intents
    )
    cogs = [
        'startgame',
        'play'
    ]

    for cog in cogs:
        await bot.load_extension(f'{cog}')

    await bot.start(TOKEN)


asyncio.run(main())