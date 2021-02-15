from data.scripts.globals import *
from data.scripts.functions import *

from data.sprites.laser import Laser
from data.sprites.pick_up import Health_Boost, Energy_Boost

import random

class Ship:
    def __init__(self, x, y, health=player_stats['health']):
        self.x = x
        self.y = y
        self.animation = []
        self.animation_counter = 0
        self.max_health = self.health = health
        self.lasers = []

    def show(self):
        #Renders the image according to the current animation frame
        self.image = self.get_image()
        self.mask = pygame.mask.from_surface(self.image)
        screen.blit(self.image, (self.x, self.y))

        #Rendering the health bar
        self.health_bar()

        #Updating the animation
        self.update_animation_counter()

    def update_lasers(self, obj):
        for laser in self.lasers[:]:
            laser.move()
            laser.show()

            #Removing the laser if it is offscreen
            if laser.is_offscreen():
                self.lasers.remove(laser)
            #Removing the laser if it has collided with the object
            elif laser.collides(obj):
                obj.damage()
                self.lasers.remove(laser)

    def shoot(self):
        #Adding a laser in the lasers list
        laser = Laser(self.x + self.get_width()//2, self.y, laser_vel, pygame.transform.flip(LASER_IMAGE, False, True))
        self.lasers.append(laser)

    def damage(self, amount=10):
        #Reducing health according to the dame amount
        self.health -= amount

    def health_bar(self):
        #Rendering the health bar first on a surface
        surface = pygame.Surface((self.get_width(), 10))
        pygame.draw.rect(surface, red, (0, 0, self.get_width(), 10))
        pygame.draw.rect(surface, green, (0, 0, int(self.health*self.get_width()/self.max_health), 10))

        #Setting alpha of the surface
        surface.set_alpha(128)

        #Finally rendering the surface on the screen surface
        screen.blit(surface, (self.x, self.y-20))

    def update_animation_counter(self):
        #Increasing the animation counter(animation frame)
        self.animation_counter += 1

        #Setting the animation frame back to 0, to let the animation continue from starting
        if self.animation_counter >= len(self.animation):
            self.animation_counter = 0

    def is_dead(self):
        #Returns if the health is lesser than or equal to 0
        return self.health <= 0

    def get_image(self):
        #Getting the image according to the animation frame
        return pygame.transform.scale2x(self.animation[self.animation_counter])

    def get_width(self):
        #Returns the ship's image's width
        return self.get_image().get_width()

    def get_height(self):
        #Returns the ship's image's height
        return self.get_image().get_height()

class Player(Ship):
    def __init__(self, x, y):
        super().__init__(x, y)
        #Loading the player animations
        self.animation = load_animations('player_animations', [fps//10, fps//10, fps//10, fps//10])
        self.mask = pygame.mask.from_surface(self.get_image())

        #Centering the player
        self.x -= self.get_width()//2
        self.y -= self.get_height()//2

        self.vel = 5
        self.COOLDOWN = fps//3
        self.cooldown_counter = 0

    def move(self):
        #Updating shooting cooldown
        self.cooldown()

        #Moving according to key presses
        keys = pygame.key.get_pressed()

        if keys[pygame.K_w]:
            self.y -= self.vel
        if keys[pygame.K_a]:
            self.x -= self.vel
        if keys[pygame.K_s]:
            self.y += self.vel
        if keys[pygame.K_d]:
            self.x += self.vel
        #Shooting if the space key is pressed
        if keys[pygame.K_SPACE]:
            self.shoot()

    def edges(self):
        #Keeping the player in the screen
        if self.x < 0:
            self.x = 0
        if self.y < 0:
            self.y = 0
        if self.x > width - self.get_width():
            self.x = width - self.get_width()
        if self.y > height - self.get_height():
            self.y = height - self.get_height()

    def shoot(self):
        #Shooting if the shooting cooldown is 0
        if self.cooldown_counter == 0:
            laser = Laser(self.x + self.get_width()//2, self.y, -laser_vel, LASER_IMAGE)
            self.lasers.append(laser)
            self.cooldown_counter = 1

    def cooldown(self):
        #Updating cooldown counter
        if self.cooldown_counter >= self.COOLDOWN:
            self.cooldown_counter = 0
        elif self.cooldown_counter > 0:
            self.cooldown_counter += 1

    def update_lasers(self, objs):
        for laser in self.lasers[:]:
            laser.move()
            laser.show()

            #Removing laser if offscreen
            if laser.is_offscreen():
                self.lasers.remove(laser)
            else:
                removed = False
                for obj in objs:
                    #Checking collision with each enemy
                    if laser.collides(obj):
                        #Damaging the enemy
                        obj.damage(player_stats['damage_amount'])

                        #If the laser is not removed yet, the laser is removed
                        if not removed:
                            self.lasers.remove(laser)
                            removed = True

    def health_bar(self):
        #Drawing the health bar
        surface = pygame.Surface((self.get_width(), 10))
        pygame.draw.rect(surface, red, (0, 0, self.get_width(), 10))
        pygame.draw.rect(surface, green, (0, 0, int(self.health*self.get_width()/self.max_health), 10))

        surface.set_alpha(128)

        #Rendering the health bar surface on the screen
        screen.blit(surface, (self.x, self.y+self.get_height()+10))

    def boost_health(self):
        #Increasing the health
        self.health += 10

        #Limiting the health to the max health of the player
        if self.health > self.max_health:
            self.health = self.max_health

    def set_pos(self, x, y):
        #Setting the position of player
        self.x = x - self.get_width()//2
        self.y = y - self.get_height()//2

class Enemy(Ship):
    def __init__(self, x, y):
        super().__init__(x, y, 100)
        #loading the animations of the enemy
        self.animation = load_animations('enemy_animations', [fps//10, fps//10, fps//10, fps//10])
        self.mask = pygame.mask.from_surface(self.get_image())
        self.vel = 2

    def move(self):
        #Moving the enemy downwards(velocity)
        self.y += self.vel

    def is_offscreen(self):
        #Returns if the enemy is offscreen
        return self.y > height

    def drop(self):
        #Random percent chance to drop a health boost of energy(feul) boost
        r = random.uniform(0,1)
        drops = [Health_Boost(self.x+self.get_width()//2, self.y+self.get_height()//2), Energy_Boost(self.x+self.get_width()//2, self.y+self.get_height()//2)]
        if r <= 0.5:
            return random.choice(drops)
