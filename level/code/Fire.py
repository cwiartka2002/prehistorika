import pygame
class Fire(pygame.sprite.Sprite):
    def __init__(self, px, py, direction):
        super().__init__()
        self.image = pygame.image.load('C:/Users/kacpe/OneDrive/Desktop/Prehistorika_by_kacper/graphics/enemy/Monsters_Creatures_Fantasy/Flying_eye/attack/fire.png')
        self.rect = self.image.get_rect()
        self.rect.center = px, py
        self.direction = direction
        if self.direction.x < 0:
            self.image = pygame.transform.flip(self.image,True,False)

    def update(self):
        self.rect.x += self.direction.x
        self.rect.y += self.direction.y

    def draw(self, surface):
        surface.blit(self.image, self.rect)