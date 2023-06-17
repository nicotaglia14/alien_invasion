# A class to track statistics for Alien invasion
class GameStats:

    def __init__(self, ai_game):
        # initialize statistics.
        self.settings = ai_game.settings
        self.reset_stats()

        # Start Alien Invasion in an active state
        self.game_active = False

        # high score should never be reset
        self.high_score = 0

    def reset_stats(self):
        # initialize statistics that can change during the game
        self.ships_left = self.settings.ship_limit
        self.score = 0
        self.level = 1

