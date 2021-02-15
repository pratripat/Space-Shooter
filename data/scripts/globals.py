import pygame

#Initializing pygame
pygame.init()

#Initializing the screen and its dimensions
width = height = 700
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption('Space Shooting Game')

#Initializing the clock and the fps
clock = pygame.time.Clock()

fps = 60

#The global laser velocity
laser_vel = 5

#Loading the progress of the game
def load_files(path):
    return open(f'data/scores/{path}.txt').read().split('\n')

stats_file = load_files('stats')
costs_file = load_files('costs')

#PLAYER STATS
player_stats = {
    'timer': int(stats_file[0]),
    'health': int(stats_file[1]),
    'damage_amount': int(stats_file[2]),
    'coins': int(stats_file[3])
}

costs = {
    'timer': int(costs_file[0]),
    'health': int(costs_file[1]),
    'damage_amount': int(costs_file[2])
}

#COLORS
black = (0,0,0)
red = (255,0,0)
green = (0,255,0)
white = (255,255,255)
purple = (128,0,255)

#IMAGES
BACKGROUND = pygame.transform.scale(pygame.image.load('data/images/background.png'), (width, height))

LASER_IMAGE = pygame.image.load('data/images/laser_image.png')

HEALTH_BOOST_IMAGE = pygame.transform.scale2x(pygame.image.load('data/images/health_boost_image.png'))
ENERGY_BOOST_IMAGE = pygame.image.load('data/images/energy_boost_image.png')

COIN_IMAGE = pygame.image.load('data/images/coin_image.png')

LIGHT_EFFECT = pygame.transform.scale(pygame.image.load('data/images/light_effect.png'), (20, 640))
