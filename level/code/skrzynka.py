import pygame
class Skrzynka(pygame.sprite.Sprite):

        def __init__(self, pos):
            super().__init__()
            self.rect = self.image.get_rect(topleft=pos)
            self.path = 'C:/Users/kacpe/OneDrive/Desktop/Prehistorika_by_kacper/graphics/teren/box'
            self.obecna = 1
            self.box = pygame.image.load(self.path + str(self.obecna) + '.png')

        def update(self, x_shift):
            self.rect.x += x_shift
        def niszczenie(self):
            self.obecna += 1
