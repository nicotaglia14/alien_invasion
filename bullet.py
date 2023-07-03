import pygame


class Bullet(pygame.sprite.Sprite):
    def __init__(self, ai_game, position, bullet_type):
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings
        self.bullet_type = bullet_type

        if self.bullet_type == 'alien':
            self.color = self.settings.alien_bullet_color
            self.rect = pygame.Rect(0, 0, self.settings.alien_bullet_width, self.settings.alien_bullet_height)
        else:
            self.color = self.settings.bullet_color
            self.rect = pygame.Rect(0, 0, self.settings.bullet_width, self.settings.bullet_height)

        self.rect.midbottom = position
        self.y = float(self.rect.y)

    def update(self):
        if self.bullet_type == 'alien':
            self.y += self.settings.alien_bullet_speed
        else:
            self.y -= self.settings.bullet_speed

        self.rect.y = self.y

    def draw_bullet(self):
        pygame.draw.rect(self.screen, self.color, self.rect)

    def fire(self):
        # Set the bullet in motion
        self.speed = self.settings.alien_bullet_speed