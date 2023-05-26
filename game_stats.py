class GameStats:
    # track statistics for Alien invasion

    def __init__(self, ai_game):
        # initialize statistics.
        self.settings = ai_game.settings
        self.reset_stats()

    def reset_stats(self):
        # initialize statistics that can change during the game
        self.ships_left = self.settings.ship_limit