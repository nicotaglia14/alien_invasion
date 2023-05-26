 #A class to store all the settings for Alien Invasion
class Settings:
    def __init__ (self):
        #Screen settings
        self.screen_width = 1100
        self.screen_height = 600
        self.bg_color = (104,34,139)

        #ship settings
        self.ship_speed = 5
        self.ship_limit = 3

        #bullet settings
        self.bullet_speed = 5.0
        self.bullet_width = 3
        self.bullet_height = 15
        self.bullet_color = (0, 0, 0)
        self.bullets_allowed = 3

        #alien settings
        self.alien_speed = 1
        self.fleet_drop_speed = 7

        #fleet_direction of 1 represents right; -1 represents left
        self.fleet_direction = 1