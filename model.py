import math
class GameModel:
    """
    Initializes a new game of Werewolf with appropriate number of players

    To do:
    Add more mode selection: e.g. able to choose additional role like valentine, cupid...

    Also, what should happen if not enough people sign up?
    """

    def __init__(self, num_players: int, game_mode='text'):
        self.num_players = num_players
        self.game_mode = game_mode
        villager_num = math.ceil(num_players / 3.5)
        werewolf_num = num_players - villager_num
        self.roles = {'villager' : villager_num, 'werewolf' : werewolf_num})
        self.players = generate_players(num_players)

    def generate_players(self, amount):
        for i in range(0,amount):
            



class Player:
    """
    Initialize an instance of a player.
    Subclasses: Werewolf, Village, Witch, Hunter....
    Incomplete. Need to add more functionality
    """
    def __init__(self, username):
        self.username = username
        self.alive = True
        pass

    def get_username(self):
        return self.username

    def get_side(self):
        return None  # might modify later: eg. by default return good

    def is_alive(self):
        return self.alive


class Werewolf(Player):
    def __init__(self, username):
        super().__init__(username)

    def get_side(self):
        return 'Werewolf'


class Villager(Player):
    def __init__(self, username):
        super().__init__(username)

    def get_side(self):
        return 'Villager'


class Witch(Player):
    """
    Witch owns a poison and a cure medicine.
    They can choose to save the people being killed or poison others at night
    """
    def __init__(self, username):
        super().__init__(username)
        self.potions = ['poison', 'medicine']

    def get_side(self):
        return 'Good'

