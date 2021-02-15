from data.scripts.globals import *
from data.scripts.functions import *
from data.scripts.button import Button

from data.sprites.ship import Player, Enemy

import random

class Game:
    def __init__(self):
        self.player = Player(width//2, height-300)
        self.close_button = Button({'x':60, 'y':30, 'w':100, 'h':50}, {'color':white, 'hover_color':green, 'font_color':black, 'alpha':128}, {'text':'Close', 'font':'comicsans', 'font_size':30})

    def generate_new_enemies(self):
        #Going to the next level if all the enemies have been killed
        self.level += 1
        self.wave_length += 5
        self.enemies = [Enemy(random.randrange(50, width-100), -(i+1)*random.randrange(200,250)) for i in range(self.wave_length)]

    def update(self):
        if len(self.enemies) == 0:
            self.generate_new_enemies()

        if self.player.is_dead():
            #Setting game over if the player is dead
            self.game_over = True
            self.game_over_state = 'You Died...'

        for enemy in self.enemies[:]:
            enemy.update_lasers(self.player)
            enemy.move()
            enemy.show()

            if random.randrange(0, fps*3) == 1:
                enemy.shoot()

            if collision(enemy, self.player):
                #If there is a collision between enemy and player, player gets damaged and enemy dies
                self.player.damage()
                enemy.health = 0

            if enemy.is_offscreen():
                #Removing the enemy if it has gone offscreen
                self.enemies.remove(enemy)

            elif enemy.is_dead():
                #If enemy has no health left it is removed
                self.enemies.remove(enemy)

                #Player coins are increased
                player_stats['coins'] += 5

                #Random chance of drops
                drop = enemy.drop()
                if drop:
                    self.pickups.append(drop)

        for pickup in self.pickups[:]:
            pickup.update()
            pickup.show()

            if pickup.on_interact(self.player, self):
                #If the player and pickup are colliding, it is removed
                self.pickups.remove(pickup)
            elif pickup.is_offscreen():
                #If the pickup is offscreen, it is removed
                self.pickups.remove(pickup)

        #Updating the player
        self.player.update_lasers(self.enemies)
        self.player.move()
        self.player.edges()
        self.player.show()

        #Decreasing timer(feul) per second according to the frame rate
        self.timer -= 1/fps

        #If times up, the game is over
        if self.timer <= 0:
            self.game_over = True
            self.game_over_state = 'Out of feul...'

        #Rendering the timer bar
        self.render_timer()

        #Updating the button to close the game
        self.close_button.update()
        self.close_button.show()

    def render_timer(self):
        #Determining the color according to the timer left
        color = ((self.start_timer-self.timer)/self.start_timer*255, self.timer/self.start_timer*255,0)
        h = height-80

        surface = pygame.Surface((20, h))
        surface.set_colorkey(black)
        #Drawing a rect according to the time left
        pygame.draw.rect(surface, color, (0, h, 20, -self.timer*(h)/self.start_timer))
        #Rendering light effect with special flags
        surface.blit(LIGHT_EFFECT, (0,0), special_flags=pygame.BLEND_MULT)
        #Setting alpha value
        surface.set_alpha(128)

        #Finally rendering the surface on the screen surface
        screen.blit(surface, (30, 70))

    def boost_timer(self):
        #Boosting the timer if the player interacts with the pickup
        self.timer += 10

        #Limiting the timer to some value
        if self.timer > self.start_timer:
            self.timer = self.start_timer

    def event_loop(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                #Saving the scores
                save_scores(costs)
                pygame.quit()
                quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                #Closing the game and entering the menu if close button is clicked
                self.close_button.on_click(self.close_game)

    def close_game(self):
        #Closing the game
        self.game_over = True
        self.game_over_state = 'Closing...'

    def restart(self):
        #Setting the level back to 0
        self.level = 0
        self.wave_length = 0

        #Refresing the timer and setting player health to max
        self.start_timer = self.timer = player_stats['timer']
        self.player.max_health = self.player.health = player_stats['health']

        #Setting game to not over
        self.game_over = False

        #Filtering the enemies and pickups
        self.enemies = []
        self.pickups = []

        #Setting the player position back to the center
        self.player.set_pos(width//2, height//2)

    def main_loop(self):
        #Restarting the game everytime this function is run
        self.restart()

        while not self.game_over:
            clock.tick(fps)

            render_background()

            self.event_loop()
            self.update()

            pygame.display.update()

        #If game is over, rendering the reason for the game over
        self.render_you_died_screen()

    def render_you_died_screen(self):
        label = font.render(self.game_over_state, 1, purple)
        surface = pygame.Surface(label.get_size())
        #Rendering the label on the surface
        surface.blit(label, (0,0))
        surface.set_colorkey(black)
        surface.set_alpha(128)
        #Rendering the surface on the screen surface
        screen.blit(surface, (width//2-label.get_width()//2, height//2-label.get_height()//2))
        pygame.display.update()
        pygame.time.wait(1000)
