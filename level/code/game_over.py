import pygame
from Menu import *
class GameOverScreen:
    def __init__(self, screen):
        self.screen = screen
        self.font = pygame.font.Font(None, 100)
        self.color = (255, 0, 255)  # Fioletowy kolor



    def display_game_over(self,text):
        self.screen.fill((0, 0, 0))  # Wypełnienie ekranu czarnym kolorem
        text = self.font.render(text, True, self.color)
        text_rect = text.get_rect(center=self.screen.get_rect().center)
        self.screen.blit(text, text_rect)




        pygame.display.flip()