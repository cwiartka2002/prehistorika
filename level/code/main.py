import pygame
import sys
from settings import *
from level import *
from game_data import *
from Menu import *


pygame.init()
screen = pygame.display.set_mode((screen_width, screen_height))
clock = pygame.time.Clock()
start_image = pygame.image.load("C:/Users/kacpe/OneDrive/Desktop/Prehistorika_by_kacper/graphics/przyciski/buttons text pack/play.png")
exit_image = pygame.image.load("C:/Users/kacpe/OneDrive/Desktop/Prehistorika_by_kacper/graphics/przyciski/buttons text pack/list.png")



start_button = Button(150, 250, start_image)
exit_button = Button(900, 250, exit_image)
level = Level(level_0, screen)

game_started = False

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
            break

    screen.fill('black')

    if not game_started:
        if start_button.draw():
            game_started = True
        elif exit_button.draw():
            sys.exit()

    else:
        level.run()



    pygame.display.update()
    clock.tick(60)