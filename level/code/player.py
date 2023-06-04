import pygame
from suport import import_folder
import level
from level import *
class Player(pygame.sprite.Sprite):
    def __init__(self,pos):
        super().__init__()
        self.import_character_assets()
        self.frame_index = 0
        self.animation_speed = 0.1
        self.image = self.animations['idle'][self.frame_index]
        self.rect = self.image.get_rect(topleft = pos)
        self.direction = pygame.math.Vector2(0,0)
        self.speed = 3
        self.gravity = 0.5
        self.jump_speed = -8
        self.jump_flag = False
        self.climbing = False
        self.status = 'idle'
        self.facting_right = True
        self.on_ground = False
        self.on_ceiling = False
        self.on_right = False
        self.on_left = False
        self.attack_flag = False
        self.na_drabinie = False

    def import_character_assets(self):
        character_path = 'C:/Users/kacpe/OneDrive/Desktop/Prehistorika_by_kacper/graphics/character/'
        self.animations = {'idle':[], 'run':[], 'jump':[], 'fall':[], 'attack':[],'hit':[], 'dead':[]}
        for animation in self.animations.keys():
            full_path = character_path + animation
            self.animations[animation] = import_folder(full_path)
    def animete(self):
        animation = self.animations[self.status]
        if self.attack_flag:
            self.frame_index += 0.08
            if int(self.frame_index) >= len(animation):
                self.frame_index = 0
                self.attack_flag = False
                self.status = 'idle'
        self.frame_index += self.animation_speed
        print(self.frame_index)
        if self.frame_index > len(animation):
            self.frame_index = 0
        image = animation[int(self.frame_index)]
        if self.facting_right:
            self.image = image
        else:
            flipped_image = pygame.transform.flip(image,True,False)
            self.image = flipped_image
      

    def get_status(self):
        keys = pygame.key.get_pressed()

        if self.direction.y <0:
            self.status = 'jump'
        elif self.direction.y > 1:
            self.status = 'fall'
        else:
            if self.direction.x != 0:
                self.status = 'run'
            else:
                self.status = 'idle'
        if keys[pygame.K_SPACE]:
            self.status = 'attack'
            self.attack_flag = True
    def get_input(self):
        keys = pygame.key.get_pressed()
        if not self.attack_flag or  self.na_drabinie:
            if keys[pygame.K_RIGHT]:
                self.direction.x = 1
                self.facting_right = True
            elif keys[pygame.K_LEFT]:
                self.direction.x = -1
                self.facting_right = False
            else:
                self.direction.x = 0
            if keys[pygame.K_UP] and self.on_ground:
                self.jump()


    def apply_gravity(self):
        self.direction.y += self.gravity
        self.rect.y += self.direction.y
    def jump(self):
        if not self.jump_flag:
            print("pressed")
            self.direction.y += self.jump_speed
            self.jump_flag = True


    def climb(self):

            keys = pygame.key.get_pressed()

            if keys[pygame.K_UP] and self.na_drabinie:
                self.direction.y -= 1
            elif keys[pygame.K_DOWN] and self.na_drabinie:
                self.direction.y += 1
            else:
                self.direction.y = -1

    def update(self):
        self.get_input()
        self.get_status()
        self.animete()



