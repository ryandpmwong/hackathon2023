import discord
import model
import asyncio


"""
Inform me on discord when modifying this file OR DDIIIIIE
(because I have lost all progress due to merge)
"""


class WerewolfGame:
    ID = 0
    GAMES = {}

    def __init__(self, channel, admin: discord.User):
        self.channel = channel
        self.admin = admin  # implement later
        self.player_list = []
        self.ID = WerewolfGame.ID
        WerewolfGame.ID += 1
        self.threads = {'villager': None, 'werewolf': None,
                        'ghost': None}

    async def create_game_threads(self):
        """When command is triggered
        Store number of running games"""
        game_id = f"Game {self.ID}: "
        message = "Welcome to Werewolf!"
        print(message) #tr
        self.threads['villager'] = await self.channel.create_thread(name=game_id + "Village Talk",
                                                              type=discord.ChannelType.private_thread)
        # create werewolf thread
        self.threads['werewolf'] = await self.channel.create_thread(name=game_id + "Werewolf Chat",
                                                              type=discord.ChannelType.private_thread)
        # need player list to populate thread
        '''for wolf in werewolves:
            werewolves_thread.add_user(wolf)'''
        # create dead chat
        self.threads['ghost'] = await self.channel.create_thread(name=game_id + "Ghost Chat",
                                                           type=discord.ChannelType.private_thread)

    async def allocate_role(self, user, thread: discord.Thread):
        self.player_list.append(model.Player(user))
        await thread.add_user(user)

    async def deallocate_role(self, user, thread:discord.Thread):
        await thread.remove_user(user)

    async def delete(self):
        async for thread in asyncio.gather(a for a in self.threads.values()): # need to be modified
            await thread.delete()

        self.__del__()

    def __del__(self):
        del self

    def get_threads(self):
        pass
