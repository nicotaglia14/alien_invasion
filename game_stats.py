# A class to track statistics for Alien invasion
class GameStats:

    def __init__(self, ai_game):
        # initialize statistics.
        self.settings = ai_game.settings
        self.reset_stats()

        # Start Alien Invasion in an active state
        self.game_active = False

        self.repeat_game = False

        # high score should never be reset
        self.high_score = 0

    def reset_stats(self):
        # initialize statistics that can change during the game
        self.ships_left = self.settings.ship_limit
        self.score = 0
        self.level = 1

    def bonus(self):
        # here is where we check what happens when the bonus is needed\
        if self.ships_left < 3:
            self.ships_left += 1
        else:
            self.score += self.settings.alien_points * 10
