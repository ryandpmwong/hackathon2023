import random

import discord
from roundmodel_a import Round
import asyncio
from random import sample
import math
from discord.ui import Select, View

"""
Inform me on discord when modifying this file OR DDIIIIIE
(because I have lost all progress due to merge)
"""

WELCOME_MESSAGE = "Welcome to WereWolf!"

# dummy list of players
dummy_players = ["player1", "player2", "player3", "player4"]


async def timer(thread: discord.Thread, seconds):  # bot
    message = await thread.send(f"Time left: {seconds}")
    while seconds >= 0:
        await asyncio.sleep(1)
        await message.edit(content=f"Time left: {seconds}")
        seconds -= 1
    await message.edit(content="Time's up!")
    return True


class WerewolfGame:
    ID = 0
    GAMES = {}

    def __init__(self, channel, users, werewolves_num=None):
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
        self.alive = {}
        for user in self.users:
            self.alive[user] = True
        self.players = {}  # will be a list of users (probably)
        self.ID = WerewolfGame.ID
        WerewolfGame.ID += 1
        self.threads = {}
        self.day = 0
        self.is_day = True
        self.werewolves = []

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

        ghost = await self.channel.create_thread(name=game_id + "Ghost Chat",
                                                 type=discord.ChannelType.private_thread,
                                                 invitable=False)
        self.threads['ghost'] = ghost

        return self.threads

    async def join_game(self, user):
        await self.threads.get('everyone').add_user(user)

    async def select_werewolves(self):
        """
        using random to select the group of werewolf in game, then add them to the thread
        Should only be called once when the game has started.
        :return: None
        """
        if self.werewolf_num <= 0:
            await self.channel.send('not enough wolves')
        self.werewolves = sample(self.users, self.werewolf_num)
        for user in self.werewolves:
            await self.threads['werewolves'].add_user(user)
            await self.threads['werewolves'].send(f'{user.mention} you are a werewolf. Kill the villagers without getting uncovered.')
        return

    async def get_threads(self):
        return self.threads.values()

    async def add_role(self, user, thread: discord.Thread):
        """
        Initialize player object for each user based on the type and allocate them into correct threads
        :param user:
        :param thread:
        :param player_type:
        :return:
        """
        await thread.add_user(user)
        self.players.update((user, None))

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
        new_round = Round(self.players.keys(), self.threads)
        await new_round.run_night()
        while new_round.get_game_result() is None:
            await new_round.run_night()
        print('night')


    async def night(self):
        await self.threads['werewolves'].send("It is night time. Discuss whom you shalt kill. No time to discuss")
        await timer(self.threads['werewolves'], 5)
        result = await self.vote([user for user in self.users if user not in self.werewolves and self.alive[user]],
                                 'werewolves')
        await self.threads['everyone'].send(f"{result} was killed last night. How horrible! Who would've done it?")
        self.threads['ghost'].send(f'@{result} you were killed. This is the ghost space')

    async def day(self):
        # if self.alive[user]
        pass

    async def vote(self, users: list[discord.User], side: str):
        """
        :param side: The side of player
        :param users: A list of users, which will be the options. (They need to be alive)
        :return: A user who is voted out.
        """
        options = [discord.SelectOption(label=user.name, description=user.name) for user in users]
        current_votes = {}
        message = None
        select = Select(placeholder="", options=options)
        time_up = False
        if side == 'werewolves':
            select.placeholder = "Vote for a player to kill"
        else:
            select.placeholder = "Vote to eliminate a player"

        async def callback(interaction: discord.Interaction):
            if not time_up:
                current_votes[interaction.user] = select.values[0]
                await interaction.channel.send(f"{interaction.user} voted for {select.values[0]}")
                await interaction.response.defer()

        select.callback = callback
        view = View().add_item(select)
        print('send view')
        # await self.threads[side].send("Vote for a player to kill")
        await self.threads[side].send("Vote for a player to kill", view=view)
        print('sent')
        time_up = await timer(self.threads[side], 5)
        print(current_votes)
        votes = list(current_votes.values())
        if len(votes) == 0:
            await self.threads[side].send("Nobody was chosen. Round skipped.")
            return None
        else:
            max_vote = 0
            selected = None
            for vote in set(votes):
                times = votes.count(vote)
                await self.threads[side].send(f'{vote} is voted {times} times')
                if times > max_vote:
                    max_vote = times
                    selected = vote
            print(selected)
            return selected


