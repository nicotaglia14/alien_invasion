import pygame.font
import pygame
from pygame.sprite import Sprite


# A class to manage the ship
class Ship(Sprite):
    def __init__(self, ai_game):
        # Initialize the ship and set its starting position.
        super().__init__()

        self.ai_game = ai_game
        self.screen = ai_game.screen
        self.settings = ai_game.settings
        self.screen_rect = ai_game.screen.get_rect()
        self.sb = ai_game.sb

        # load the ship image and get its rect
        self.image = pygame.image.load('images/ship.png')
        self.rect = self.image.get_rect()

        # start new ship at the bottom center of the screen
        self.rect.midbottom = self.screen_rect.midbottom

        # store a decimal value for the ship's horizontal position
        self.x = float(self.rect.x)
        self.y = float(self.rect.y)

        # movement flag
        self.moving_right = False
        self.moving_left = False
        self.moving_up = False
        self.moving_down = False

        self.font = pygame.font.SysFont('', 48)

    def update(self):
        # updates the ships (x and y) position based on the movement flag
        if self.moving_right and self.rect.right < self.screen_rect.right:
            self.x += self.settings.ship_speed
        elif self.moving_left and self.rect.left > 0:
            self.x -= self.settings.ship_speed
        elif self.moving_up and self.rect.top > 0:
            self.y -= self.settings.ship_speed
        elif self.moving_down and self.rect.bottom < self.screen_rect.bottom:
            self.y += self.settings.ship_speed

        # update rectangle object from self.x
        self.rect.x = self.x
        self.rect.y = self.y

    def blitme(self):
        # prints the ship image
        self.screen.blit(self.image, self.rect)

    def center_ship(self):
        # center the ship on the screen
        self.rect.midbottom = self.screen_rect.midbottom
        self.x = float(self.rect.x)
