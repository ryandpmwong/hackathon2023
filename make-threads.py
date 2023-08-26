async def create_game_threads(channel_id):
    # when command is trigerred
    # store number of running games
    game_id = "game1"
    message = "Welcome to Werewolf!"
    channel = client.get_channel(int(channel_id))
    # create public thread for all players
    all_players_thread = await channel.create_thread(name = game_id+"-everyone", type=ChannelType.private_thread)
    # create werewolf thread
    werewolves_thread = await channel.create_thread(name = game_id+"-werewolves", type=ChannelType.private_thread)
    # need player list to populate thread
    '''for wolf in werewolves:
        werewolves_thread.add_user(wolf)'''
    # create dead chat
    dead_thread = await channel.create_thread(name = game_id+" dead", type=ChannelType.private_thread)

async def delete_game_threads(channel_id):
    pass

class test_threads:
    def __init__(self, channel_id):
        self.all_players_thread = None
        pass