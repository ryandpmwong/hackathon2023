import math


class GameModel:
    """
    Initializes a new game of Werewolf with appropriate number of players

    To do:
    Add more mode selection: e.g. able to choose additional role like valentine, cupid...

    Also, what should happen if not enough people sign up?
    """

    def __init__(self, num_players: int, game_mode):
        # In class Game of Werebot-main, the game mode is defined to be "text" by default. Perhaps doing game mode in
        # class Game is better, so we can have game model only focus on internal stuff - to be discussed

        self.num_players = num_players
        self.game_mode = game_mode
        self.villager_num = math.ceil(num_players / 3.5)
        self.werewolf_num = num_players - self.villager_num
        self.roles = {'villager': self.villager_num, 'werewolf': self.werewolf_num}
        self.user_list = []  # list of player objects
        # need to generate user list from methods
        self.players = self.generate_players(num_players)
        self.day = 0


    def generate_players(self, user_list):
        for user in self.user_list:
            pass


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

    def get_role(self):
        return "Player"

    def is_alive(self):
        return self.alive

    def kill(self):
        self.alive = False


class Werewolf(Player):
    def __init__(self, username):
        super().__init__(username)

    def get_side(self):
        return 'Bad'

    def get_role(self):
        return "Werewolf"


class Villager(Player):
    def __init__(self, username):
        super().__init__(username)

    def get_side(self):
        return 'Good'

    def get_role(self):
        return "Villager"


class Witch(Player):  # or doctor? Whatever name you guys want
    """
    Witch owns a poison and a cure medicine.
    They can choose to save the people being killed or poison others at night
    """

    def __init__(self, username):
        super().__init__(username)
        self.poison = True
        self.medicine = True

    def get_side(self):
        return 'Good'

    def get_role(self):
        return "Witch"

    def apply_poison(self, other: Player) -> bool:
        """
        :param other: The player to apply poison on
        :return: True if the application is successful, False otherwise
        """
        if self.poison is True and other.is_alive():
            other.kill()
            self.poison = False
            return True
        return False

    def apply_medicine(self, other: Player) -> bool:
        """
        :param other: The player to apply poison on
        :return: True if the application is successful, False otherwise
        """
        if self.medicine is True and other.is_alive():
            other.kill()
            self.medicine = False
            return True
        return False

    def get_potion_status(self):
        return f"poison: {int(self.poison)}, medicine: {int(self.medicine)}"