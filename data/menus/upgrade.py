from data.scripts.globals import *
from data.scripts.functions import *
from data.scripts.button import Button

import math

class Upgrade_Menu:
    def __init__(self):
        self.player_animation = load_animations('player_animations', [fps//10, fps//10, fps//10, fps//10])
        self.animation_counter = 0
        self.text = []
        self.generate_buttons()

    def generate_buttons(self):
        #Generating all the buttons
        self.buttons = []

        self.timer_button = Button({'x':width//2, 'y':height//2+200, 'w':150, 'h':50}, {'color':white, 'hover_color':green, 'font_color':black, 'alpha':128}, {'text':f'Timer({costs["timer"]})', 'font':'comicsans', 'font_size':30})
        self.health_button = Button({'x':width//2-180, 'y':height//2+200, 'w':150, 'h':50}, {'color':white, 'hover_color':green, 'font_color':black, 'alpha':128}, {'text':f'Health({costs["health"]})', 'font':'comicsans', 'font_size':30})
        self.damage_button = Button({'x':width//2+180, 'y':height//2+200, 'w':150, 'h':50}, {'color':white, 'hover_color':green, 'font_color':black, 'alpha':128}, {'text':f'Damage({costs["damage_amount"]})', 'font':'comicsans', 'font_size':30})
        self.close_button = Button({'x':width//2, 'y':height//2+270, 'w':150, 'h':50}, {'color':white, 'hover_color':green, 'font_color':black, 'alpha':128}, {'text':'Back', 'font':'comicsans', 'font_size':30})

        self.buttons.append(self.timer_button)
        self.buttons.append(self.health_button)
        self.buttons.append(self.damage_button)
        self.buttons.append(self.close_button)

    def update(self):
        #Rendering the player animation
        screen.blit(self.get_player_image(), (width//2-self.get_player_image().get_width()//2, height//2-self.get_player_image().get_height()//2))

        #Rendering the text if there is any
        self.render_text()

        #Updating all the buttons
        for button in self.buttons:
            button.update()
            button.show()

        #Updating animation frames
        self.animation_counter += 1
        if self.animation_counter >= len(self.player_animation):
            self.animation_counter = 0

    def improve_stat(self, stat):
        #If player has enough amount of coins, the player gets the upgrade and the coins are reduced according to the cost
        if player_stats['coins'] >= costs[stat]:
            player_stats[stat] += 10
            player_stats['coins'] -= costs[stat]

            #Increasing the cost
            costs[stat] += int(costs[stat]*2/3)

            #Setting the text to 'Improved stat(according to what button or what upgrade is chosen)'
            self.text = [f'Improved {stat}', 255]
        #Else the text is set to the amount of coins needed still
        else:
            self.text = [f'You need more {costs[stat]-player_stats["coins"]} coins...', 255]

    def close(self):
        self.closed = True

    def render_text(self):
        #Rendering the text if there is any
        if len(self.text) > 0:
            label = font.render(self.text[0], 1, purple)
            surface = pygame.Surface(label.get_size())
            surface.blit(label, (0,0))
            surface.set_colorkey(black)
            surface.set_alpha(self.text[1])
            screen.blit(surface, (width//2-label.get_width()//2, 200-label.get_height()//2))

            self.text[1] -= 1

            #If the alpha value of the text is 0, it is removed
            if self.text[1] <= 0:
                self.text.clear()

    def event_loop(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                #Saving the progress in the game
                save_scores(costs)
                pygame.quit()
                quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                #Updating the buttons
                self.timer_button.on_click(self.improve_stat, 'timer')
                self.health_button.on_click(self.improve_stat, 'health')
                self.damage_button.on_click(self.improve_stat, 'damage_amount')

                #If the buttons are clicked, then the buttons text is updated to the new cost
                self.timer_button.update_text(f'Timer({costs["timer"]})')
                self.health_button.update_text(f'Health({costs["health"]})')
                self.damage_button.update_text(f'Damage({costs["damage_amount"]})')

                #Closing the menu if close button is clicked
                self.close_button.on_click(self.close)

    def main_loop(self):
        #Setting the closed boolean false and clearing the text
        self.closed = False
        self.text = []

        while not self.closed:
            clock.tick(fps)

            render_background()
            self.event_loop()
            self.update()

            pygame.display.update()

    def get_player_image(self):
        #Getting the current image from animation frame
        image = pygame.transform.scale2x(self.player_animation[self.animation_counter])
        return pygame.transform.scale2x(image)
