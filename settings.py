# A class to store all the settings for Alien Invasion

class Settings:
    def __init__(self):

        # initialize dynamic settings
        self.initialize_dynamic_settings()

        # Screen settings
        self.screen_width = 1200
        self.screen_height = 800
        self.bg_color = (0, 0, 0)

        # ship settings
        self.ship_limit = 3

        # bullet settings
        self.bullet_width = 3
        self.bullet_height = 15
        self.bullet_color = (255, 255, 255)
        self.bullets_allowed = 3

        # alien bullet settings
        self.alien_bullet_width = 3
        self.alien_bullet_height = 18
        self.alien_bullet_color = (255, 152, 0)

        # alien settings
        self.fleet_drop_speed = 10

        # how quickly the game speeds up
        self.speedup_scale = 1.2

        # how quickly the alien point values increase
        self.score_scale = 1.5

        # initialize the memory settings
        self.mem_ship_speed = self.ship_speed
        self.mem_bullet_speed = self.bullet_speed
        self.mem_alien_speed = self.alien_speed

    def initialize_dynamic_settings(self):
        # initialize settings that change throughout the game
        self.ship_speed = 2
        self.bullet_speed = 3.0
        self.alien_speed = 1.5
        self.alien_bullet_speed = 1.0

        # fleet_direction of 1 represents right; -1 represents left
        self.fleet_direction = 1

        # scoring
        self.alien_points = 50

        # difference between shots
        self.shot_gap = 3

    def save_dynamic_settings(self):
        self.mem_ship_speed = self.ship_speed
        self.mem_bullet_speed = self.bullet_speed
        self.mem_alien_speed = self.alien_speed

    def reset_dynamic_settings(self):
        self.ship_speed = self.mem_ship_speed
        self.bullet_speed = self.mem_bullet_speed
        self.alien_speed = self.mem_alien_speed

    def increase_speed(self):
        # increase speed settings and alien point values
        self.ship_speed *= self.speedup_scale
        self.bullet_speed *= self.speedup_scale
        self.alien_speed *= self.speedup_scale
        self.alien_bullet_speed *= self.speedup_scale
        self.shot_gap /= self.speedup_scale

    def increase_points(self):
        self.alien_points = int(self.alien_points * self.score_scale)
