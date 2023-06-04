import pygame
from settings import *
from support import import_folder
class tile(pygame.sprite.Sprite):
    def __init__(self,size,size1,px,py):
        super().__init__()
        self.image = pygame.Surface((size,size1))
        self.rect = self.image.get_rect(topleft = (px, py))

    def update(self, shift):
        self.rect.x += shift
class StaticTile(tile):
    def __init__(self, size,size1,x,y,surface):
        super().__init__(size,size1,x,y)
        self.image = surface




class Zdrowie(StaticTile):
    def __init__(self, size,size1, x, y, surface):
        super().__init__(size,size1, x, y,surface)
        offset = y +size
        self.rect = self.image.get_rect(bottomleft = (x,offset))

class Animated(tile):
    def __init__(self,siez,size1,x,y,path):
        super().__init__(siez,size1,x,y)
        self.frames = import_folder(path)
        self.frame_index = 0
        self.image = self.frames[self.frame_index]
    def animate(self):
        self.frame_index += 0.15
        if self.frame_index > 4:
            self.frame_index = 0
        self.image = self.frames[int(self.frame_index)]

    def update(self,shift):
        self.animate()
        self.rect.x += shift
class Enemy(Animated):
    def __init__(self,size,size1,x,y):
        super().__init__(size,size1,x,y,'C:/Users/kacpe/OneDrive/Desktop/Prehistorika_by_kacper/graphics/enemy/Monsters_Creatures_Fantasy/Skeleton/walk')
        self.speed = -2
    def move(self):
        self.rect.x += self.speed
    def reverse(self):
        if self.speed < 0:
            self.image = pygame.transform.flip(self.image,True,False)
    def direction(self):
        self.speed *= -1

    def update(self,shift):
        self.animate()
        self.move()
        self.reverse()
        self.rect.x += shift

class Statek(tile):
    def __init__(self,size,size1,px,py,surface):
        super().__init__(size,size1,px,py)
        self.image = surface
        self.speed = -3
    def move(self):
        pass

    def update(self,shift):

        self.rect.x += shift





