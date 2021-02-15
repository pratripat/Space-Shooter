from data.scripts.globals import *

class Background:
    def __init__(self):
        self.scroll = 0
        self.image = BACKGROUND

    def show(self):
        #Rendering two images according to scroll to give the effect of flying in space
        screen.blit(self.image, (0,self.scroll-width))
        screen.blit(self.image, (0,self.scroll))

    def update(self):
        #Increasing the scroll
        self.scroll += 1

        #Setting the scroll back to zero to show that space is infinite
        if self.scroll-width == 0:
            self.scroll = 0
