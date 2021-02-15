from data.scripts.globals import *
from data.scripts.functions import *

class Laser:
    def __init__(self, x, y, vel, image):
        #Centering the laser only in the x-axis
        self.x = x - image.get_width()//2
        self.y = y
        self.vel = vel
        self.image = image
        self.mask = pygame.mask.from_surface(self.image)

    def show(self):
        #Rendering the image
        screen.blit(self.image, (self.x, self.y))

    def move(self):
        #Moving the laser either up or down
        self.y += self.vel

    def collides(self, obj):
        #Returns for collision between laser's image and other object's image
        return collision(self, obj)

    def is_offscreen(self):
        #Returns if the laser is offscreen
        return (
            self.x > width or
            self.y > height or
            self.x < -self.get_width() or
            self.y < -self.get_height()
        )

    def get_width(self):
        #Returns laser's image's width
        return self.image.get_width()

    def get_height(self):
        #Returns laser's image's height
        return self.image.get_height()
