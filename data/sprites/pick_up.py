from data.scripts.globals import *
from data.scripts.functions import *

class Pickup:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.scroll = 1

    def show(self):
        #Rendering the image
        screen.blit(self.image, (self.x, self.y))

    def update(self):
        #Moving the pickup downwards
        self.y += self.scroll

    def is_offscreen(self):
        #Returns if the pickup's image is offscreen
        return self.y > height

class Health_Boost(Pickup):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.image = HEALTH_BOOST_IMAGE
        self.mask = pygame.mask.from_surface(self.image)

    def on_interact(self, player, game):
        #Boosts player's health if there is interaction between pickup and player
        if collision(self, player):
            player.boost_health()
            return True

        return False

class Energy_Boost(Pickup):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.image = ENERGY_BOOST_IMAGE
        self.mask = pygame.mask.from_surface(self.image)

    def on_interact(self, player, game):
        #Boosts the timer(feul) if there is an interaction between player and the pickup
        if collision(self, player):
            game.boost_timer()
            return True

        return False
