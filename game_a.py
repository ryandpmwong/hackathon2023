from __future__ import annotations
from typing import Optional, Union
from collections import abc

import random

import discord
from roundmodel_a import Round
import asyncio
from random import sample
import math
from discord.ui import Select, View

import prompts

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
    ID = 1
    GAMES = {}

    def __init__(self, 
                 channel: Union[abc.GuildChannel, abc.PrivateChannel], 
                 users: list[Union[discord.User, discord.Member]], 
                 werewolves_num: int | None = None):
        """
        :param channel: the channel the game belongs in
        :param players: list of users
        """
        if werewolves_num is not None:
            self.werewolf_num = werewolves_num
        else:
            self.werewolf_num = math.ceil(len(users) / 3.5)

        # Commented out for debug purposes
        # self.villager_num = len(users) - self.werewolf_num

        self.channel = channel
        self.users = users

        self.villager_num = len(self.users) - self.werewolf_num
        self.alive = {}
        for user in self.users:
            self.alive[user] = True
        self.players = {}  # will be a list of users (probably)
        self.ID = WerewolfGame.ID
        WerewolfGame.ID += 1
        self.threads = {}
        self.is_day = False
        self.werewolves = []
        print("Init ended ok")


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


    async def select_werewolves(self) -> None:
        """
        using random to select the group of werewolf in game, then add them to the thread
        Should only be called once when the game has started.
        :return: None
        """
        if self.werewolf_num <= 0:
            await self.channel.send('Not enough werewolves! Please add more.')
        elif 2*self.werewolf_num > self.villager_num:
            # await self.channel.send("Too many wolves :(")
            # await self.delete()
            pass

        await self.threads['everyone'].send("Welcome to the game! The game will start in 15 seconds.")
        self.werewolves = sample(self.users, self.werewolf_num)
        # Sends role message
        for user in self.users:
            print(user)
            print(user.bot)
            if not user.bot:
                if user in self.werewolves:
                    print("User werewolf")
                    await user.send(prompts.werewolf_prompts[
                        random.randint(0, len(prompts.werewolf_prompts)-1)
                        ].replace("{name}", user.mention))
                    
                    if not len(self.werewolves) == 1:
                        await user.send("\nYour other werewolves are "+
                                    str([user.display_name for user in self.werewolves]))
                    print("Messaged")

                else:
                    print("User no werewolf")
                    await user.send(prompts.villager_prompts[
                        random.randint(0, len(prompts.villager_prompts)-1)
                        ].replace("{name}", user.mention))
                    print("Messaged")
        
        # Timer before game start
        await timer(self.threads["everyone"], 15)

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
            await thread.send('All threads should be deleted after 10 seconds.')
        await asyncio.sleep(10)
        for thread in self.threads.values():  # need to be modified
            await thread.delete()
        self.__del__()

    def __del__(self):
        del self


    async def run_game(self):
        new_round = Round(self.players.keys(), self.threads)
        await new_round.run_night()
        while new_round.get_game_result() is None:
            await new_round.run_night()

    async def is_game_over(self):
        villagers = len([user for user in self.users if self.alive[user] and user not in self.werewolves])
        werewolves = len([werewolf for werewolf in self.werewolves if self.alive[werewolf]])
        print("villagers left: ", villagers, "\twerewolves left: ", werewolves)
        if werewolves >= villagers:
            # await self.threads['everyone'].send("AHHH werewolf killed everyone!")
            # await self.channel.send("Game over. Wolves rules.")
            return 'Werewolf'
        elif werewolves == 0:
            # await self.threads['everyone'].send("All werewolves are killed. YAHHHH")
            return 'Villager'
        else:
            return False
        
    async def announce_death(self, user: discord.Member, time_of_day: str) -> None:
        # Replace with prompts to mix up games
        if not user == None:
            if time_of_day == 'night':
                await self.threads['everyone'].send(f"**{user.display_name}** was killed last night. How horrible! Who could've done it...?")
            
            elif time_of_day == 'day':
                await self.threads['everyone'].send(f"It seems that you have chosen to eliminate {user.display_name}. Farewell, {user.display_name}. 🫡")
            
            await self.threads['ghost'].add_user(user)
            await self.threads['ghost'].send(f'{user.mention} you were killed, RIP. This is the ghost space.')

            for a in self.alive:
                if a == user:
                    self.alive[a] = False
                    if time_of_day == 'day':
                        await self.threads['werewolves'].remove_user(a)
                        await self.threads['everyone'].send(f'A wolf is killed. '
                                                            f'{len(list(wolf for wolf in self.werewolves if self.alive[wolf]))}'
                                                            f' wolves left')
        else:
            await self.threads['everyone'].send(f"No-one died. Weird, huh?")

        # elif a.status == discord.Status.offline:
        #     self.alive[a] = False

    async def night(self) -> None:
        await self.threads['everyone'].send("It is now night time, Werewolves discuss and stalk the earth...")
        await self.threads['werewolves'].send("It is night time. Discuss whom you shalt kill.")
        await timer(self.threads['werewolves'], 30)
        result = await self.vote([user for user in self.users if user not in self.werewolves and self.alive[user]],
                                 'werewolves')
        print(result)

        await self.announce_death(result, 'night')

        return

    async def day(self) -> None:
        await self.threads['everyone'].send("It is day time. Discuss who the werewolves may be.")
        votable = [user for user in self.users if self.alive[user]]
        await timer(self.threads['everyone'], 30)
        result = await self.vote(votable,
                                 'everyone')

        await self.announce_death(result)

        return

    async def vote(self, 
                   users: list[discord.User], 
                   side: str) -> None | discord.User:
        """
        :param side: The side of player
        :param users: A list of users, which will be the options. (They need to be alive)
        :return: A user who is voted out.
        """
        options = [discord.SelectOption(
            label=user.display_name, 
            description="Vote to off "+user.name,
            value=str(user.id)) for user in users]
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
                print(select.values[0])
                print(interaction.guild.get_member(int(select.values[0])))
                print((interaction.guild.get_member(int(select.values[0]))).display_name)
                # Makes dictionary with player vote, then converts to user
                current_votes[interaction.user] = int(select.values[0])
                # {select.values[0]: interaction.guild.get_member(int(select.values[0]))}
                print(current_votes)

                await interaction.channel.send(f"{interaction.user.display_name} voted for "+
                                               f"{interaction.guild.get_member(current_votes[interaction.user]).display_name}!")
                await interaction.response.defer()
        
        select.callback = callback
        view = View().add_item(select)
        # await self.threads[side].send("Vote for a player to kill")
        await self.threads[side].send("Vote for a player to kill", view=view)

        time_up = await timer(self.threads[side], 10)

        votes = list(current_votes.values())
        print("votes")
        print(votes)

        if len(votes) == 0:
            await self.threads[side].send("Nobody was chosen. Round skipped.")
            return None
        
        else:
            max_vote = 0
            selected = None

            for vote in set(votes):
                print(vote)
                user_voted = self.channel.guild.get_member(vote)
                print(user_voted)
                times = votes.count(vote)
                await self.threads[side].send(f'{user_voted.display_name} is voted {times} times')

                if times > max_vote:
                    max_vote = times
                    selected = user_voted

            return selected