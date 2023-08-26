import discord


class test_threads:

    def __init__(self, channel, author):
        self.all_players_thread = None
        self.werewolves_thread = None
        self.dead_thread = None
        self.channel = channel
        self.author = author

    async def create_game_threads(self):
        """When command is triggered
        Store number of running games"""
        game_id = "Game 1: "
        message = "Welcome to Werewolf!"

        # create public thread for all players
        self.all_players_thread = await self.channel.create_thread(name=game_id + "Village Talk",
                                                                      type=discord.ChannelType.private_thread)
        # create werewolf thread
        self.werewolves_thread = await self.channel.create_thread(name=game_id + "Werewolf Chat",
                                                                     type=discord.ChannelType.private_thread)
        # need player list to populate thread
        '''for wolf in werewolves:
            werewolves_thread.add_user(wolf)'''
        # create dead chat
        self.dead_thread = await self.channel.create_thread(name=game_id + "Ghost Chat",
                                                               type=discord.ChannelType.private_thread)

        # testing, adding myself
        discord_handle = self.author
        await self.all_players_thread.add_user(discord_handle)
        await self.werewolves_thread.add_user(discord_handle)

    async def delete_game_threads(self, channel_id):
        """Deletes game threads, or attempts to hahahahahahahahahahahahahah"""
        await self.all_players_thread.delete()
        await self.werewolves_thread.delete()
        await self.dead_thread.delete()
