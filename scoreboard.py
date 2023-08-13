import time
import ship
import pygame.font
from pygame.sprite import Group
from lives import Life
import powers


class Scoreboard:
    # a class to report scoring information
    def __init__(self, ai_game):
        # initialize score keeping attributes
        self.ai_game = ai_game
        self.screen = ai_game.screen
        self.screen_rect = self.screen.get_rect()
        self.settings = ai_game.settings
        self.stats = ai_game.stats
        self.ship = ship
        self.power = powers

        # font settings for scoring information
        self.text_color = (255, 255, 255)
        self.bonus_color = (255, 255, 0)
        self.power_color = (0, 255, 0)
        self.font = pygame.font.SysFont('', 48)

        # prepare the initial score images
        self.prep_score()
        self.prep_high_score()
        self.prep_level()
        self.prep_ships()

        self.elapsed_time = 1
        self.power_elapsed_time = 1

    def prep_score(self):
        # turn the score into a rendered image
        rounded_score = round(self.stats.score, -1)
        score_str = "{:,}".format(rounded_score)
        self.score_image = self.font.render(score_str, True, self.text_color, None)

        # display the score at the top right of the screen
        self.score_rect = self.score_image.get_rect()
        self.score_rect.right = self.screen_rect.right - 20
        self.score_rect.top = 20

    def prep_high_score(self):
        # turn the high score into a rendered image
        high_score = round(self.stats.high_score, -1)
        high_score_str = "{:,}".format(high_score)
        self.high_score_image = self.font.render(high_score_str, True, self.text_color, None)

        # display the high_score at the top of the screen
        self.high_score_rect = self.high_score_image.get_rect()
        self.high_score_rect.centerx = self.screen_rect.centerx
        self.high_score_rect.top = self.score_rect.top

    def prep_level(self):
        # turn the level into a rendered image
        self.level_str = "Level {}".format(self.stats.level)
        self.level_image = self.font.render(self.level_str, True, self.text_color, None)

        # position the level below the score
        self.level_rect = self.level_image.get_rect()
        self.level_rect.right = self.score_rect.right
        self.level_rect.top = self.score_rect.bottom + 10

    def prep_ships(self):
        # show how many ships are left
        self.ships = Group()
        for ship_number in range(self.stats.ships_left):
            life = Life("dynamic")
            life.rect.x = 10 + ship_number * life.rect.width
            life.rect.y = 10
            self.ships.add(life)

    def static_lives(self):
        # show the amount of lives that the player has
        self.lives = Group()
        for life_number in range(self.settings.ship_limit):
            life = Life("static")
            life.rect.x = 10 + life_number * life.rect.width
            life.rect.y = 10
            self.ships.add(life)

    def game_banners(self):
        if not self.stats.game_active and self.stats.ships_left == 0:
            self.banners = pygame.image.load('images/game_over.png')
        else:
            self.banners = pygame.image.load('images/alien_invasion.png')

        self.banners_rect = self.banners.get_rect()
        self.banners_rect.centerx = self.screen_rect.centerx
        self.banners_rect.y = 90

    def timer_count(self):
        self.elapsed_time = round(10 - (time.time() - self.ai_game.start_time))
        timer_str = "Bonus: {} seconds".format(self.elapsed_time)
        self.timer_image = self.font.render(timer_str, True, self.bonus_color, None)
        self.timer_rect = self.timer_image.get_rect()
        self.timer_rect.centerx = self.screen_rect.centerx

        """ I AM TRYING TO IMPORT THE CORRECT WAY BUT ITS NOT IMPORTING THE OTHER CLASS"""
        if self.power.power_active:
            self.timer_rect.top = (self.high_score_rect.bottom + 30)
        else:
            self.timer_rect.top = self.high_score_rect.bottom
        self.screen.blit(self.timer_image, self.timer_rect)

    def power_timer(self):
        self.power_elapsed_time = round(4 - (time.time() - self.ai_game.power_time))
        timer_str = "POWER: {} seconds".format(self.power_elapsed_time)
        self.timer_image = self.font.render(timer_str, True, self.power_color, None)
        self.timer_rect = self.timer_image.get_rect()
        self.timer_rect.centerx = self.screen_rect.centerx
        self.timer_rect.top = self.high_score_rect.bottom
        self.screen.blit(self.timer_image, self.timer_rect)

        if self.power_elapsed_time <= 0:
            self.settings.reset_dynamic_settings()
            self.ship.super_power = False

    def show_score(self):
        # draw scores, level, and ships to the screen
        self.screen.blit(self.score_image, self.score_rect)
        self.screen.blit(self.high_score_image, self.high_score_rect)
        self.screen.blit(self.level_image, self.level_rect)

        if not self.stats.game_active:
            self.screen.blit(self.banners, self.banners_rect)
        self.ships.draw(self.screen)

    def check_high_score(self):
        # check to see if there's a new high score
        if self.stats.score > self.stats.high_score:
            self.stats.high_score = self.stats.score
            self.prep_high_score()
