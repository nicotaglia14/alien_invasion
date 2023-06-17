import pygame
from pygame.sprite import Sprite


# A class to manage the lives of the player
class Life(Sprite):
    def __init__(self, image_type):
        # Initialize the life
        super().__init__()

        # load the ship images and get their rect
        if image_type == "dynamic":
            self.image = pygame.image.load('images/dynamic_life.png')
        elif image_type == "static":
            self.image = pygame.image.load('images/static_life.png')
        else:
            # Default to dynamic image if image_type is not recognized
            self.image = pygame.image.load('images/dynamic_life.png')

        self.rect = self.image.get_rect()




