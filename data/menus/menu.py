from data.scripts.globals import *
from data.scripts.functions import *
from data.scripts.button import Button
from data.scripts.game import Game

from data.menus.upgrade import Upgrade_Menu
from data.menus.how_to_play import How_To_Play_Menu

class Menu:
    def __init__(self):
        self.player_animation = load_animations('player_animations', [fps//10, fps//10, fps//10, fps//10])
        self.animation_counter = 0
        self.game = Game()
        self.upgrade_menu = Upgrade_Menu()
        self.howtoplay = How_To_Play_Menu()

        self.generate_buttons()

    def generate_buttons(self):
        #Generating all the buttons
        self.buttons = []

        self.play_button = Button({'x':width//2, 'y':height//2+200, 'w':130, 'h':50}, {'color':white, 'hover_color':green, 'font_color':black, 'alpha':128}, {'text':'Play', 'font':'comicsans', 'font_size':30})
        self.upgrade_button = Button({'x':width//2-150, 'y':height//2+200, 'w':130, 'h':50}, {'color':white, 'hover_color':green, 'font_color':black, 'alpha':128}, {'text':'Upgrade', 'font':'comicsans', 'font_size':30})
        self.howtoplay_button = Button({'x':width//2+150, 'y':height//2+200, 'w':130, 'h':50}, {'color':white, 'hover_color':green, 'font_color':black, 'alpha':128}, {'text':'How to play', 'font':'comicsans', 'font_size':30})

        self.buttons.append(self.play_button)
        self.buttons.append(self.upgrade_button)
        self.buttons.append(self.howtoplay_button)

    def update(self):
        #Rendering the player animation
        screen.blit(self.get_player_image(), (width//2-self.get_player_image().get_width()//2, height//2-self.get_player_image().get_height()//2))

        #Updating the buttons
        for button in self.buttons:
            button.update()
            button.show()

        #Updating the animation frame for the player
        self.animation_counter += 1
        if self.animation_counter >= len(self.player_animation):
            self.animation_counter = 0

    def event_loop(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                #Saving the progress of the game before quiting
                save_scores(costs)
                pygame.quit()
                quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                #Running the functions if the buttons are clicked
                self.play_button.on_click(self.game.main_loop)
                self.upgrade_button.on_click(self.upgrade_menu.main_loop)
                self.howtoplay_button.on_click(self.howtoplay.main_loop)

    def main_loop(self):
        while True:
            clock.tick(fps)

            render_background()
            self.event_loop()
            self.update()

            pygame.display.update()

    def get_player_image(self):
        #Getting the image from current animation frame
        image = pygame.transform.scale2x(self.player_animation[self.animation_counter])
        return pygame.transform.scale2x(image)
