from data.scripts.globals import *

class Button:
    def __init__(self, dimension, colors, text):
        #Centering the button
        self.x = dimension['x'] - dimension['w']//2
        self.y = dimension['y'] - dimension['h']//2
        self.w = dimension['w']
        self.h = dimension['h']

        #Setting up the colors
        self.color = colors['color']
        self.hover_color = colors['hover_color']
        self.font_color = colors['font_color']
        self.alpha = colors['alpha']
        self.current_color = self.color

        #Setting up font and fontstyle
        self.text = text['text']
        self.font = pygame.font.SysFont(text['font'], text['font_size'])

        self.surface = pygame.Surface((self.w, self.h))
        self.surface.set_colorkey(black)

    def show(self):
        #Rendering everything first on the surface
        pygame.draw.rect(self.surface, self.current_color, (0, 0, self.w, self.h))
        self.surface.set_alpha(self.alpha)
        screen.blit(self.surface, (self.x, self.y))

        self.render_text()

    def render_text(self):
        #Rendering text directly on the screen
        label = self.font.render(self.text, 1, self.font_color)
        screen.blit(label, (self.x+self.w//2-label.get_width()//2, self.y+self.h//2-label.get_height()//2))

    def update(self):
        self.hover()

    def update_text(self, text):
        self.text = text

    def hover(self):
        self.current_color = self.color

        #If mouse is over the button, changing the button's color to the button's hover color
        if self.is_mouse_over_button():
            self.current_color = self.hover_color

    def is_mouse_over_button(self):
        #Returns if the mouse is over the button
        mx, my = pygame.mouse.get_pos()

        return (
            mx > self.x and mx < self.x + self.w and
            my > self.y and my < self.y + self.h
        )

    def on_click(self, func, args=None):
        #If mouse is over the button
        if self.is_mouse_over_button():
            #If there are some aruments, running the function with aruments
            if args:
                func(args)
            #If there are no arguments to be passed, running the function with no arguments
            else:
                func()
