from __future__ import annotations
from typing import Optional, Union
import collections.abc
from collections import abc

import discord
from discord.ext import commands
from discord.ui import Select, View

import asyncio
import random
from random import sample
import math

import model
from roundmodel import Round

"""
Inform me on discord when modifying this file OR DDIIIIIE
(because I have lost all progress due to merge)
"""

WELCOME_MESSAGE = "Welcome to WereWolf!"

# dummy list of players
dummy_players = ["player1", "player2", "player3", "player4"]


class WerewolfGame:
    ID = 1
    GAMES = {}

    def __init__(self, 
                 channel: Union[abc.GuildChannel, abc.PrivateChannel], 
                 users: list[Union[discord.User, discord.Member]], 
                 werewolves_num=None):
        """
        :param channel: the channel the game belongs in
        :param players: list of users
        """

        if werewolves_num is not None:
            self.werewolf_num = werewolves_num
        else:
            self.werewolf_num = math.ceil(len(users) / 3.5)
        self.villager_num = len(users) - self.werewolf_num
        self.channel = channel
        self.users = users

        self.players = []  # will be a list of player objects (probably)
        self.ID = WerewolfGame.ID
        WerewolfGame.ID += 1
        self.threads = {}
        self.day = 0
        self.is_day = True
        # self.round = Round(self.players)

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
        everyone = await self.channel.create_thread(name=game_id + "Village Talk",
                                                    type=discord.ChannelType.private_thread,
                                                    invitable=False)
        self.threads['everyone'] = everyone
        werewolf = await self.channel.create_thread(name=game_id + "Werewolf Chat",
                                                    type=discord.ChannelType.private_thread,
                                                    invitable=False)
        self.threads['werewolves'] = werewolf
        """
        """

        ghost = await self.channel.create_thread(name=game_id + "Ghost Chat",
                                                 type=discord.ChannelType.private_thread,
                                                 invitable=False)
        self.threads['ghost'] = ghost

        return self.threads

    async def generate_players(self) -> None:
        """
        generate players and allocate them into correct threads
        :param users: discord.User, users who have joined the game.
        :return: None
        """
        werewolves = sample(self.users, self.werewolf_num)
        print(werewolves, ' chosen as Werewolf')
        for user in self.users:
            if user in werewolves:
                await self.allocate_role(user, self.threads['werewolves'], 'werewolves')
                await self.allocate_role(user, self.threads['everyone'], None)
            else:
                await self.allocate_role(user, self.threads['everyone'], 'villager')
        print(self.players, 'from game.py')
        return

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
        if player_type is None:
            self.threads['everyone'].add_role(user)

        if player_type == 'villager':
            self.players.append(model.Villager(user))

        elif player_type == 'werewolf':
            self.players.append(model.Werewolf(user))

        await thread.add_user(user)
        print(self.players)

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

    '''async def werewolf_round(self):
        for user in self.threads[1]:
            await self.allocate_role(user, list(self.threads.keys())[1], 'werewolf')
        # vote'''

    async def run_game(self):
        print('start run game')
        print('players', self.players)
        new_round = Round(self.players, self.threads)
        print('start new round')
        await new_round.run_night()
        while new_round.get_game_result() is None:
            await new_round.run_night()
        print('night')
        # while new_round.get_game_result() is None:
        #     new_round = Round(self.players, self.threads)
        #     await new_round.run_night()
        # return new_round.get_game_result()
