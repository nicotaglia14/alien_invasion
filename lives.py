import pygame
from pygame.sprite import Sprite


# A class to manage the lives of the player
class Life(Sprite):
    def __init__(self, ai_game):
        # Initialize the life
        super().__init__()

        # load the ship image and get its rect
        self.image = pygame.image.load('images/life.png')
        self.rect = self.image.get_rect()






