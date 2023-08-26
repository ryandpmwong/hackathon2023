import collections.abc

import discord
import model
from discordbottest import Round
import asyncio
from collections import abc
from random import sample
import math

"""
Inform me on discord when modifying this file OR DDIIIIIE
(because I have lost all progress due to merge)
"""

WELCOME_MESSAGE = "Welcome to WereWolf!"


class WerewolfGame:
    ID = 0
    GAMES = {}

    def __init__(self, channel, users):
        """
        :param channel: the channel the game belongs in
        :param players: list of users
        """
        self.villager_num = 0
        self.werewolf_num = 0
        self.channel = channel
        # self.players = self.generate_players(users)

        self.players = []  # will be a list of player objects (probably)
        self.ID = WerewolfGame.ID
        WerewolfGame.ID += 1
        self.threads = {}
        self.day = 0
        self.is_day = True
        self.round = Round(self.players)


    async def create_game_threads(self):
        """
        Create game threads for werewolf, ghost and villagers
        Should allocate players here
        initially no one will be in ghost channel
        Should run at most 1 time (for each game instance created)
        It is run in bot.py because we cannot run async in __init__
        """
        game_id = f"Game {self.ID}: "
        # create villager thread
        villagers = await self.channel.create_thread(name=game_id + "Village Talk",
                                                     type=discord.ChannelType.private_thread,
                                                     invitable=False)
        self.threads[villagers] = []
        werewolf = await self.channel.create_thread(name=game_id + "Werewolf Chat",
                                                    type=discord.ChannelType.private_thread,
                                                    invitable=False)
        self.threads[werewolf] = []
        """
        """

        ghost = await self.channel.create_thread(name=game_id + "Ghost Chat",
                                                 type=discord.ChannelType.private_thread,
                                                 invitable=False)
        self.threads[ghost] = []

    def generate_players(self, users: list[discord.User]):
        """
        generate players and allocate them into correct threads
        :param users: discord.User, users who have joined the game.
        :return: None
        """

        self.werewolf_num = len(users) - math.ceil(len(users) / 3.5)
        werewolves = sample(users, self.villager_num)
        for wolf in werewolves:
            await self.allocate_role(wolf, self.threads[1], 'werewolf')
        for user in users:
            if user not in werewolves:
                await self.allocate_role(user, self.threads[0], 'villager')


    async def get_threads(self):
        return self.threads.values()

    async def allocate_role(self, user, thread: discord.Thread, player_type: str):
        """
        Initialize player object for each user based on the type and allocate them into correct threads
        :param user:
        :param thread:
        :param player_type:
        :return:
        """
        if player_type == 'villager':
            self.threads[thread].append(model.Villager(user))
        elif player_type == 'werewolf':
            self.threads[thread].append(model.Werewolf(user))
        await thread.add_user(user)

    async def deallocate_role(self, user, thread: discord.Thread):
        await thread.remove_user(user)

    async def delete(self):
        for thread in self.threads.values():  # need to be modified
            await thread.delete()

        self.__del__()

    def __del__(self):
        del self

    def refresh_status(self):
        if self.is_day:
            pass

    def werewolf_round(self):
        for user in self.threads[1]:
            await self.allocate_role(user, list(self.threads.keys())[1])
        # vote

    def is_game_over(self) -> bool or str:
        pass

