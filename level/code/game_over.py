import pygame
from Menu import *
class GameOverScreen:
    def __init__(self, screen):
        self.screen = screen
        self.font = pygame.font.Font('C:/Users/kacpe/OneDrive/Desktop/Prehistorika_by_kacper/graphics/text/for_text.ttf', 100)
        self.color = (255, 0, 255)  # Fioletowy kolor
        self.points_font = pygame.font.Font('C:/Users/kacpe/OneDrive/Desktop/Prehistorika_by_kacper/graphics/text/for_text.ttf', 36)

    def display_game_over(self, text, points):
        self.screen.fill((0, 0, 0))
        game_over_text = self.font.render(text, True, self.color)
        game_over_rect = game_over_text.get_rect(center=self.screen.get_rect().center)
        self.screen.blit(game_over_text, game_over_rect)

        points_text = self.points_font.render("Points: " + str(points), True, pygame.color.THECOLORS['white'])
        points_rect = points_text.get_rect(center=(game_over_rect.centerx, game_over_rect.bottom + 50))
        self.screen.blit(points_text, points_rect)

        pygame.display.flip()