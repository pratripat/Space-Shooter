from data.scripts.globals import *
from data.scripts.background import Background

background = Background()
font = pygame.font.SysFont('comicsans', 50)

def collision(obj1, obj2):
    #Return pixel perfect collision between two images
    x_off = obj2.x - obj1.x
    y_off = obj2.y - obj1.y

    return obj1.mask.overlap(obj2.mask, (x_off, y_off)) != None

def render_background():
    #Renders the background
    background.update()
    background.show()

    #Rendering the coins
    label = font.render(str(player_stats['coins']), 1, white)
    screen.blit(label, (width-label.get_width()-20, 20))

    screen.blit(COIN_IMAGE, (width-label.get_width()-COIN_IMAGE.get_width()-30, 20))

def load_animations(path, frames):
    #Loads the animation frames
    animation_frames = []

    for i in range(len(frames)):
        for n in range(frames[i]):
            image = pygame.image.load(f'data/animations/{path}/{i}.png')
            animation_frames.append(image)

    return animation_frames

def save_scores(cost):
    #Saves the progress of the game in two .txt files
    stats_file = open('data/scores/stats.txt', 'w')
    costs_file = open('data/scores/costs.txt', 'w')

    stats_file.write(str(player_stats['timer']) + '\n')
    stats_file.write(str(player_stats['health']) + '\n')
    stats_file.write(str(player_stats['damage_amount']) + '\n')
    stats_file.write(str(player_stats['coins']) + '\n')

    costs_file.write(str(costs['timer']) + '\n')
    costs_file.write(str(costs['health']) + '\n')
    costs_file.write(str(costs['damage_amount']) + '\n')

    stats_file.close()
    costs_file.close()
