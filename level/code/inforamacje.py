import pygame
import sys
class UI:
    def __init__(self,surface):
        self.display_surface = surface
        self.path = 'C:/Users/kacpe/OneDrive/Desktop/Prehistorika_by_kacper/graphics/ui/'
        self.obecna = 1
        self.health_bar = pygame.image.load(self.path + str(self.obecna) + '.png')
    def show_health(self):
        self.display_surface.blit(self.health_bar,(20,10))

    def update_health(self, value):
        try:
            self.obecna += value
            self.health_bar = pygame.image.load(self.path + str(self.obecna)+'.png')
            if self.obecna > 9:
                self.obecna =0
                return True
            return False
        except FileNotFoundError:
            self.obecna == 1

class Text:
    def __init__(self, text, text_colour, px, py, font_type=None, font_size = 74):

        font = pygame.font.Font( 'C:/Users/kacpe/OneDrive/Desktop/Prehistorika_by_kacper/graphics/text/for_text.ttf', font_size)
        self.image = font.render(text, True, text_colour)
        self.rect = self.image.get_rect()
        self.rect.center = px, py

    def draw(self, surface):
        surface.blit(self.image, self.rect)




