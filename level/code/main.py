import pygame, sys
from settings import *
from level import *
from game_data import *

pygame.init() #przygotowuje moduł pygame do użycia
screen = pygame.display.set_mode((screen_width, screen_height))
clock = pygame.time.Clock() #pomaga w odświerzaniu
level = Level(level_0, screen)
while True:
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
                break

        screen.fill('black')
        level.run()
        pygame.display.update()
        clock.tick(60)
