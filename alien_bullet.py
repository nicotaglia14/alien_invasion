import pygame


class AlienBullet(pygame.sprite.Sprite):
    def __init__(self, ai_game, position):
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings
        self.color = self.settings.alien_bullet_color

        self.rect = pygame.Rect(0, 0, self.settings.alien_bullet_width, self.settings.alien_bullet_height)
        self.rect.midbottom = position  # Set the initial position to the provided position

        self.y = float(self.rect.y)

        self.bullet_direction = -1

    def update(self):
        self.y -= self.settings.alien_bullet_speed * self.bullet_direction  # Multiply the speed by the bullet direction
        self.rect.y = self.y

    def draw_bullet(self):
        pygame.draw.rect(self.screen, self.color, self.rect)

    def fire(self):
        # Set the bullet in motion
        self.speed = self.settings.alien_bullet_speed
