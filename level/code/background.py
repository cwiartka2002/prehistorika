import pygame
from settings import *
class Sky:
    def __init__(self):
        self.top = pygame.image.load("C:/Users/kacpe/OneDrive/Desktop/Prehistorika_by_kacper/graphics/background/Battleground1.png").convert()
        self.top = pygame.transform.scale(self.top,(screen_width,screen_height))
    def draw(self, surface):
        surface.blit(self.top,(0,0))