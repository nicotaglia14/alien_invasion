import random


class Power:
    def __init__(self, ai_game):
        self.settings = ai_game.settings
        self.power_active = False

        self.rand_power = 0

    def get_powers(self):
        if not self.power_active:
            self.settings.save_dynamic_settings()

        self.power_active = True
        self.rand_power = random.randint(1, 4)

        if self.rand_power == 1:
            self.super_speed()
        elif self.rand_power == 2:
            self.slow_motion()
        elif self.rand_power == 3:
            self.super_bullets()
        elif self.rand_power == 4:
            self.big_bullet()

    def super_speed(self):
        self.settings.ship_speed *= 3

    def slow_motion(self):
        self.settings.alien_speed /= 2
        self.settings.alien_bullet_speed /= 2

    def big_bullet(self):
        self.settings.bullet_width = 100

    def super_bullets(self):
        self.settings.bullet_speed *= 3
        self.settings.bullet_color = (0, 255, 0)
