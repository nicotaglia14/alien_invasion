import random


class Power:
    def __init__(self, ai_game):
        self.settings = ai_game.settings
        self.power_active = False

    def get_powers(self):
        if not self.power_active:
            self.settings.save_dynamic_settings()

        self.power_active = True
        rand_power = 4

        if rand_power == 1:
            self.super_speed()
        elif rand_power == 2:
            self.slow_motion()
        elif rand_power == 3:
            self.super_bullets()
        elif rand_power == 4:
            self.big_bullet()

    def super_speed(self):
        self.settings.ship_speed *= 2

    def slow_motion(self):
        self.settings.alien_speed /= 2
        self.settings.alien_bullet_speed /= 2

    def big_bullet(self):
        self.settings.bullet_width = 3000

    def super_bullets(self):
        print("super bullets active")
