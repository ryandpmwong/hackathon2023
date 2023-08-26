class test_threads:

    def __init__(self, channel_id):
        self.all_players_thread = None
        self.werewolves_thread = None
        self.dead_thread = None

    async def create_game_threads(self, channel_id, bot):
        """When command is triggered
        Store number of running games"""
        game_id = "game1"
        message = "Welcome to Werewolf!"
        channel = bot.get_channel(int(channel_id))
        # create public thread for all players
        self.all_players_thread = await channel.create_thread(name = game_id+"-everyone", type=bot.ChannelType.private_thread)
        # create werewolf thread
        self.werewolves_thread = await channel.create_thread(name = game_id+"-werewolves", type=bot.ChannelType.private_thread)
        # need player list to populate thread
        '''for wolf in werewolves:
            werewolves_thread.add_user(wolf)'''
        # create dead chat
        self.dead_thread = await channel.create_thread(name = game_id+" dead", type=bot.ChannelType.private_thread)

        # testing, adding myself
        discord_handle = "insomniac.crow"
        self.all_players_thread.add_user(discord_handle)
        self.werewolves_thread.add_user(discord_handle)

    async def delete_game_threads(self, channel_id):
        """Deletes game threads, or attempts to hahahahahahahahahahahahahah"""
        self.all_player_thread.delete()
        self.werewolves_thread.delete()
        self.dead_thread.delete()