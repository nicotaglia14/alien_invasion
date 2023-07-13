import pygame
from pygame.sprite import Sprite
from game_stats import GameStats


# class to represent the alien
class Alien(Sprite):

    def __init__(self, ai_game, alien_type):
        # initialize the alien and set starting position
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings
        self.scoreboard = ai_game.sb
        self.stats = GameStats(self)
        self.level = self.stats.level

        # load the alien image and set its rect attribute
        if alien_type == "yellow":
            self.image = pygame.image.load('images/alien2.png')
        elif alien_type == "blue":
            self.image = pygame.image.load('images/alien.png')
        elif alien_type == "random":
            self.image = pygame.image.load('images/alien1.png')
        else:
            # Default to dynamic image if image_type is not recognized
            self.image = pygame.image.load('images/alien2.png')

        self.rect = self.image.get_rect()

        # start each new alien near the top left of the screen
        self.rect.x = self.rect.width
        self.rect.y = self.rect.height

        # store the alien's exact horizontal position
        self.x = float(self.rect.x)

    def check_edges(self):
        # returns true if the alien is at the edge of the screen
        screen_rect = self.screen.get_rect()
        if self.rect.right >= screen_rect.right or self.rect.left <= 0:
            return True

    def update(self):
        # move the alien to the right
        self.x += (self.settings.alien_speed * self.settings.fleet_direction)
        self.rect.x = self.x

