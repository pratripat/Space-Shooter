from data.scripts.globals import *
from data.scripts.functions import *
from data.scripts.button import Button

class How_To_Play_Menu:
    def __init__(self):
        self.closed = False

        self.generate_text()
        self.generate_buttons()

    def generate_text(self):
        #Setting the lines that will be shown
        self.lines = []

        self.lines.append('"W" to move up')
        self.lines.append('"A" to move left')
        self.lines.append('"S" to move down')
        self.lines.append('"D" to move right')
        self.lines.append('Space to shoot')
        self.lines.append('Collect energies to boost the feul!')
        self.lines.append('Collect health to boost health!')
        self.lines.append('Kill the enemies to get coins to upgrade!')

    def generate_buttons(self):
        #The close button
        self.button = Button({'x':width//2, 'y':height//2+250, 'w':100, 'h':50}, {'color':white, 'hover_color':green, 'font_color':black, 'alpha':128}, {'text':'Back', 'font':'comicsans', 'font_size':30})

    def update(self):
        #Rendering the lines
        self.render_text()

        #Updating the buttons
        self.button.update()
        self.button.show()

    def render_text(self):
        for i, line in enumerate(self.lines):
            label = font.render(line, 1, white)
            screen.blit(label, (width//2-label.get_width()//2, label.get_height()*i+50+(20*i)))

    def close(self):
        self.closed = True

    def event_loop(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                #Saving the progress of the game
                save_scores(costs)
                pygame.quit()
                quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                #If the close button is clicked, closing this menu and going to the main menu
                self.button.on_click(self.close)

    def main_loop(self):
        #Setting the closed boolean at the start of this menu to false
        self.closed = False

        while not self.closed:
            clock.tick(fps)

            render_background()
            self.event_loop()
            self.update()

            pygame.display.update()
