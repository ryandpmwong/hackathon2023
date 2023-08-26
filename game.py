import discord
import model
import asyncio


class WerewolfGame:
    ID = 0
    GAMES = {}

    def __init__(self, channel, admin: discord.User):
        self.channel = channel
        self.admin = admin  # implement later
        self.player_list = []
        self.ID = WerewolfGame.ID
        WerewolfGame.ID += 1
        self.threads = {'village': None, 'werewolf': None,
                        'ghost': None}  # contain tread in the order: [village_thread, werewolf_thread, ghost_thread. Use for del
        asyncio.run(self.create_game_threads())

    async def create_game_threads(self):
        """When command is triggered
        Store number of running games"""
        game_id = "Game 1: "
        message = "Welcome to Werewolf!"

        # create public thread for all players
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

    def get_threads(self):
        return self.threads

    async def allocate_role(self, user, thread: discord.Thread):
        self.player_list.append(model.Player(user))
        await thread.add_user(user)

    async def delete(self):
        for thread in asyncio.gather(a for a in self.threads.values()):
            await thread.delete()

        self.__del__()

    def __del__(self):
        del self
