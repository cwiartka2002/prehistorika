import pygame



from settings import *
screen = pygame.display.set_mode((screen_width, screen_height))
class Button():
    def __init__(self, x, y, image):
        self.width = image.get_width()
        self.height = image.get_height()
        self.image = pygame.transform.scale(image, (200, 150))
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.clicked = False

    def draw(self):
        action = False
        pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(pos) and pygame.mouse.get_pressed()[0] and not self.clicked:
            print("cover")
            self.clicked = True
            action = True
        if not pygame.mouse.get_pressed()[0]:
            self.clicked = False
        screen.blit(self.image, (self.rect.x, self.rect.y))
        return action