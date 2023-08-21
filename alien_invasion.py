import sys
import random
import time
from time import sleep
import pygame
from settings import Settings
from game_stats import GameStats
from ship import Ship
from bullet import Bullet
from alien import Alien
from button import Button
from scoreboard import Scoreboard
from powers import Power


# Overall class to manage game assets and behavior
class ALienInvasion:
    def __init__(self):
        pygame.init()

        self.settings = Settings()
        self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)  # Set the screen size to unknown
        self.settings.screen_width = self.screen.get_rect().width  # Get the screen width and set that for the size
        self.settings.screen_height = self.screen.get_rect().height  # Get the screen height and set that for the size

        pygame.display.set_caption("Alien Invasion")

        # set the image for the background
        self.background_image = pygame.image.load("images/bg.png").convert()
        self.background_image = pygame.transform.scale(self.background_image,
                                                       (self.settings.screen_width, self.settings.screen_height))

        # Create the groups for the game
        self.bullets = pygame.sprite.Group()
        self.alien_bullets = pygame.sprite.Group()
        self.aliens = pygame.sprite.Group()
        self.red_aliens_group = pygame.sprite.Group()

        # create an instance to store game statistics, and create a scoreboard
        self.stats = GameStats(self)
        self.power = Power(self)
        self.sb = Scoreboard(self)
        self.ship = Ship(self)
        self._create_fleet()
        self.alien = Alien(self, "yellow")

        # make the play and quit buttons
        self.play_button = Button(self, "Play", (0, 255, 0), 430)
        self.quit_button = Button(self, "Quit", (255, 0, 0), 490)

        # set a starting time
        self.last_alien_shot_time = 0

    # MAIN FUNCTIONS TO RUN THE GAME
    def run_game(self):
        # Start the main loop for the game
        while True:
            self._check_events()
            self.sb.game_banners()

            if self.stats.game_active:
                self._check_alien_type()
                self._update_aliens()
                self.ship.update()
                self._update_bullets()
                if self.stats.level > 5:
                    self._fire_alien_bullet()

            self._update_screen()

            if (self.stats.level + 1) % 5 == 0:
                self.sb.elapsed_time = 10

    def _check_events(self):
        # Watch for keyboard and mouse events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

            # detect when the user presses the keys
            elif event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)

            # detect when the user stops pressing the keys
            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)

            # start when clicked on play button
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                self._check_buttons(mouse_pos)

    def _check_buttons(self, mouse_pos):
        # start a new game when the player clicks play
        play_button_clicked = self.play_button.rect.collidepoint(mouse_pos)
        if play_button_clicked and not self.stats.game_active:
            # reset the game settings
            self.settings.initialize_dynamic_settings()
            self.stats.reset_stats()
            self.stats.game_active = True
            self.aliens.empty()
            self.red_aliens_group.empty()
            self.bullets.empty()
            self.alien_bullets.empty()
            self.sb.prep_score()
            self.sb.prep_ships()
            self.sb.static_lives()

            # create a new fleet and center the ship
            self._create_fleet()

            self.sb.prep_level()
            self.ship.center_ship()

            # hide the mouse cursor
            pygame.mouse.set_visible(False)

        quit_button_clicked = self.quit_button.rect.collidepoint(mouse_pos)
        if quit_button_clicked:
            sys.exit()

    def _check_keydown_events(self, event):
        # respond to keypress
        if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
            self.ship.moving_right = True
        elif event.key == pygame.K_LEFT or event.key == pygame.K_a:
            self.ship.moving_left = True
        elif event.key == pygame.K_SPACE:
            self._fire_bullet()
        elif event.key == pygame.K_q:
            sys.exit()

    def _check_keyup_events(self, event):
        if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
            self.ship.moving_right = False
        elif event.key == pygame.K_LEFT or event.key == pygame.K_a:
            self.ship.moving_left = False

    # ALIEN-RELATED FUNCTIONS
    def _check_alien_type(self):
        random_alien = random.randint(1, 3)
        if (self.stats.level + 1) % 5 == 0:
            self.alien_type = "blue"
        elif random_alien == 3 and not self.red_aliens_group:
            self.alien_type = "random"
        else:
            self.alien_type = "yellow"

        return self.alien_type

    def _create_alien(self, alien_number, row_number):
        # creates ab alien and places it in the row
        if self.stats.repeat_game:
            alien = Alien(self, "yellow")
        else:
            alien = Alien(self, self._check_alien_type())

        alien_width, alien_height = alien.rect.size
        alien.x = alien_width + 2 * alien_width * alien_number
        alien.rect.x = alien.x
        alien.rect.y = alien_height + 2 * alien.rect.height * row_number
        self.aliens.add(alien)
        if self.alien_type == "random":
            self.red_aliens_group.add(alien)

    def _update_aliens(self):
        # update the positions of every alien in the fleet
        self._check_fleet_edges()
        self.aliens.update()

        # look for alien-ship collisions
        if pygame.sprite.spritecollideany(self.ship, self.aliens):
            self._ship_hit()

        # check for aliens getting to the bottom of the screen
        self._check_aliens_bottom()

    def _create_fleet(self):
        # create an alien and then a fleet
        if self.stats.repeat_game:
            alien = Alien(self, "yellow")
        else:
            alien = Alien(self, self._check_alien_type())

        # reset the time
        self.start_time = time.time()

        alien_width, alien_height = alien.rect.size
        available_space_x = self.settings.screen_width - (2 * alien_width)
        number_aliens_x = available_space_x // (2 * alien_width)

        # determine the number of rows of aliens that fit on the screen
        ship_height = self.ship.rect.height
        available_space_y = (self.settings.screen_height - (2 * alien_height) - ship_height)
        number_rows = available_space_y // (2 * alien_height)

        # create the full fleet of aliens
        for row_number in range(number_rows):
            for alien_number in range(number_aliens_x):
                self._create_alien(alien_number, row_number)

    # ALIEN FLEET MOVING FUNCTIONS
    def _check_fleet_edges(self):
        # respond appropriately if any aliens have reached an edge
        for alien in self.aliens.sprites():
            if alien.check_edges():
                self._change_fleet_direction()
                break

    def _check_aliens_bottom(self):
        # check if any aliens have reached the bottom
        screen_rect = self.screen.get_rect()
        for alien in self.aliens.sprites():
            if alien.rect.bottom >= screen_rect.bottom:
                # treat this the same as if the ship got hit
                self._ship_hit()
                break

    def _change_fleet_direction(self):
        # drop the entire fleet and  change the fleet's direction.
        for alien in self.aliens.sprites():
            alien.rect.y += self.settings.fleet_drop_speed
        self.settings.fleet_direction *= -1

    # BULLET RELATED FUNCTIONS
    def _fire_bullet(self):
        # create a new bullet and add it to the bullets group
        if len(self.bullets) < self.settings.bullets_allowed:
            new_bullet = Bullet(self, self.ship.rect.midtop, 'ship')
            self.bullets.add(new_bullet)

    def _fire_alien_bullet(self):
        current_time = time.time()
        if current_time - self.last_alien_shot_time >= self.settings.shot_gap:
            self.last_alien_shot_time = current_time

            if len(self.alien_bullets) < self.settings.bullets_allowed:
                random_alien = random.choice(self.aliens.sprites())
                alien_bullet = Bullet(self, random_alien.rect.midbottom, 'alien')
                alien_bullet.fire()
                self.alien_bullets.add(alien_bullet)

    def _update_bullets(self):
        # update position of bullets and get rid of old bullets
        self.bullets.update()
        self.alien_bullets.update()

        # get rid of the bullets that have disappeared
        for bullet in self.bullets.copy():
            if bullet.rect.bottom <= 0:
                self.bullets.remove(bullet)

        # get rid of the bullets that have disappeared
        for alien_bullet in self.alien_bullets.copy():
            if alien_bullet.rect.top >= self.settings.screen_height:
                self.alien_bullets.remove(alien_bullet)

        self._check_bullet_alien_collision()
        self._check_alien_bullet_ship_collision()

    # BULLET COLLISIONS FUNCTIONS
    def _check_alien_bullet_ship_collision(self):
        # Check for aliens hitting the ship with bullets
        for alien_bullet in self.alien_bullets:
            if alien_bullet.rect.colliderect(self.ship.rect):
                self._ship_hit()
                break

    def _check_bullet_alien_collision(self):
        # check for any bullets that have hit aliens if so, get rid of the bullet and the alien
        red_aliens_collisions = pygame.sprite.groupcollide(self.bullets, self.red_aliens_group, True, True)

        if self.power.power_active and self.power.rand_power == 3:
            collisions = pygame.sprite.groupcollide(self.bullets, self.aliens, True, False)
        else:
            collisions = pygame.sprite.groupcollide(self.bullets, self.aliens, True, True)

        if red_aliens_collisions:
            self.sb.power_elapsed_time = 4
            self.power_time = time.time()

            self.power.get_powers()

        if collisions:
            for aliens in collisions.values():
                self.stats.score += self.settings.alien_points * len(aliens)
            self.sb.prep_score()
            self.sb.check_high_score()

        # destroy existing bullets and create new fleet
        if not self.aliens:

            # empty the groups
            self.bullets.empty()
            self.alien_bullets.empty()
            self._create_fleet()

            # check if they destroyed the fleet before the bonus was gone
            if self.sb.elapsed_time > 0 and self.stats.level % 5 == 0:
                self.stats.bonus()
                self.sb.prep_ships()
                self.sb.static_lives()

            # increase level
            self.stats.level += 1
            self.sb.prep_level()

            # increase points
            self.settings.increase_points()
            self.settings.increase_speed()

            # update the settings and the memory
            if not self.power.power_active:
                self.settings.save_dynamic_settings()

        self.stats.repeat_game = False

    def _ship_hit(self):
        # respond to the ship being hit by an alien
        # decrement ships left
        if self.stats.ships_left > 0:

            # decrement ships_left, and update scoreboard
            self.stats.ships_left -= 1
            self.sb.prep_ships()
            self.sb.static_lives()

            # pause
            sleep(1)

        else:
            self.stats.game_active = False
            pygame.mouse.set_visible(True)

        # get rid of any remaining aliens and bullets
        self.aliens.empty()
        self.red_aliens_group.empty()
        self.bullets.empty()
        self.alien_bullets.empty()

        self.stats.repeat_game = True

        # create a new fleet and center the ship
        self._create_fleet()
        self.ship.center_ship()

    # SCREEN UPDATING FUNCTION
    def _update_screen(self):
        # update images on the screen, and flip to the new screen.
        # self.screen.fill(self.settings.bg_color)
        self.screen.blit(self.background_image, (0, 0))

        self.ship.blitme()
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()
        for alien_bullet in self.alien_bullets.sprites():
            alien_bullet.draw_bullet()
        self.aliens.draw(self.screen)

        # draw the score information
        self.sb.show_score()

        # draw the play button if the game is inactive
        if not self.stats.game_active:
            self.play_button.draw_button()
            self.quit_button.draw_button()

        # show the counter every 5 levels
        if (self.stats.level % 5) == 0 and self.sb.elapsed_time > 0 and self.stats.game_active:
            self.sb.timer_count()

        # show the timer for the powers
        if self.power.power_active and self.sb.power_elapsed_time > 0 and self.stats.game_active:
            self.sb.power_timer()

        if self.sb.power_elapsed_time <= 0:
            self.power.power_active = False

        pygame.display.flip()


if __name__ == '__main__':
    # Make a game instance, and run the game.
    ai = ALienInvasion()
    ai.run_game()
