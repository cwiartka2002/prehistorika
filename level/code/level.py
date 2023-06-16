import pygame
from support import *
from settings import *
from Tile import *
from player import *
from drabina import *
import os

from inforamacje import *

class Level:
    def __init__(self, level_data, surface):
        self.worold_shift = 0
        self.display_surface = surface

        player_layout = import_csv_layout(level_data['player'])
        self.player = pygame.sprite.GroupSingle()
        self.setup_player(player_layout)

        ship_layout = import_csv_layout(level_data['statek'])
        self.statek_sprites = self.create_tile_group(ship_layout, 'statek')


        terrain_layout = import_csv_layout(level_data['terrain'])
        self.terrain_sprites = self.create_tile_group(terrain_layout,'terrain')

        drabina_layout = import_csv_layout(level_data['drabina'])
        self.drabina_sprites = self.create_tile_group(drabina_layout, 'drabina')

        zdrowie_layout = import_csv_layout(level_data['zdrowie'])
        self.zdrowie_sprites = self.create_tile_group(zdrowie_layout,'zdrowie')

        enemy = import_csv_layout(level_data['enemy'])
        self.enemy_sprites = self.create_tile_group(enemy, 'enemy')

        kolizja = import_csv_layout(level_data['kolizja'])
        self.kolizja_sprites = self.create_tile_group(kolizja, 'kolizja')

        za_drabina = import_csv_layout(level_data['za_drabina'])
        self.za_drabina_sprites = self.create_tile_group(za_drabina, 'za_drabina')

        self.flag_cam_move = False


        self.pd = 0

        self.poinnts = 0

        self.lifes = 3
        self.interface = UI(pygame.display.set_mode((screen_width, screen_height)))

        self.enemy_flag = False
    def create_tile_group(self, layout, type):
        sprite_group = pygame.sprite.Group()
        for index, row in enumerate(layout):
            for col_index, val in enumerate(row):
                if val != '-1':
                    x = col_index * tile_size
                    y = index * tile_size
                    if type == 'terrain':
                        terrain_tile_list = import_cut_graphics('C:/Users/kacpe/OneDrive/Desktop/Prehistorika_by_kacper/graphics/teren/[64x64] Rocky Grass.png',tile_size,tile_size)
                        tile_surface = terrain_tile_list[int(val)]
                        sprite = StaticTile(tile_size,tile_size, x, y, tile_surface)

                    if type == 'drabina':
                            drabina_surface = pygame.image.load('C:/Users/kacpe/OneDrive/Desktop/Prehistorika_by_kacper/graphics/teren/ladder/28x128/2.png')

                            sprite = StaticTile(28,64, x, y, drabina_surface)


                    if type == 'zdrowie':
                        zdrowie_tile_list = import_cut_graphics('C:/Users/kacpe/OneDrive/Desktop/Prehistorika_by_kacper/graphics/teren/boxx.png',50,50)
                        zdrowie_surface = zdrowie_tile_list[int(val)]
                        sprite = Zdrowie(tile_size, tile_size, x, y, zdrowie_surface)

                    if type == 'za_drabina':
                        za_drabina_surface = import_cut_graphics('C:/Users/kacpe/OneDrive/Desktop/Prehistorika_by_kacper/graphics/teren/[64x64] Rocky Grass.png',tile_size, tile_size)
                        za_drabina_surface = za_drabina_surface[int(val)]
                        sprite = StaticTile(tile_size, tile_size,x,y,za_drabina_surface)

                    if type == 'enemy':
                        sprite = Enemy(tile_size,tile_size, x, y)

                    if type == 'kolizja':
                        sprite = tile(tile_size,tile_size, x, y)

                    if type == 'statek':
                        statek_tile_list = import_cut_graphics('C:/Users/kacpe/OneDrive/Desktop/Prehistorika_by_kacper/graphics/teren/Ship/ship13.png', 64, 64)
                        statek_surface = statek_tile_list[int(val)]
                        sprite = Statek(tile_size, tile_size, x, y, statek_surface)
                    sprite_group.add(sprite)

        return sprite_group
    def setup_player(self,layout):
        for index, row in enumerate(layout):
            for col_index, val in enumerate(row):
                x = col_index * tile_size
                y = index * tile_size
                if val != '-1':
                    sprite = Player((x,y))
                    self.player.add(sprite)

    def colision(self):
        for enemy in self.enemy_sprites.sprites():
            if pygame.sprite.spritecollide(enemy, self.kolizja_sprites, False):
                enemy.direction()


    def horizontal_movment_collision(self):
        player = self.player.sprite
        player.rect.x += player.direction.x * player.speed
        obiekty_kolizja = self.terrain_sprites.sprites()  + self.statek_sprites.sprites()+ self.zdrowie_sprites.sprites()
        for sprite in obiekty_kolizja :
            if sprite.rect.colliderect(player.rect):
                if player.direction.x < 0:
                    player.rect.left = sprite.rect.right
                    player.on_left = True
                    self.current_x = player.rect.left
                elif player.direction.x > 0:
                    player.rect.right = sprite.rect.left
                    player.on_right = True
                    self.current_x = player.rect.right
            if player.on_left and (player.rect.left < self.current_x or player.direction.x >= 0):
                player.on_left = False
            if player.on_right and (player.rect.right > self.current_x or player.direction.x <= 0):
                player.on_right = False

    def climb_ladder(self):
        player = self.player.sprite
        ladder_collision = pygame.sprite.spritecollide(player, self.drabina_sprites, False)
        if ladder_collision:
            player.na_drabinie = True
            player.jump_flag = True
            player.climb()

    def vertical_movment_collision(self):

        player = self.player.sprite
        player.apply_gravity()
        obiekty_kolizja = self.terrain_sprites.sprites()  + self.statek_sprites.sprites() + self.zdrowie_sprites.sprites()

        for sprite in obiekty_kolizja:
            if sprite.rect.colliderect(player.rect):
                if player.direction.y > 0:
                    player.rect.bottom = sprite.rect.top
                    player.jump_flag = False
                    player.direction.y = 0
                    player.on_ground = True
                elif player.direction.y < 0:
                    player.rect.top = sprite.rect.bottom
                    player.direction.y = 0
                    player.on_ceiling = True
                if player.on_ground and player.direction.y < 0 or player.direction.y > 1:
                    player.on_ground = False
                if player.on_ceiling and player.direction.y > 0:
                    player.on_ceiling = False

    def enemy_colision(self):
        player = self.player.sprite
        colision = pygame.sprite.spritecollide(self.player.sprite, self.enemy_sprites, False)
        if colision and not self.enemy_flag:
            for enemy in colision:
                if not enemy.moving_left and player.facting_right:
                    enemy.direction()
                self.interface.update_health(1)
                player.hitted()
            self.enemy_flag = True
        elif not colision:
            self.enemy_flag = False



    def cam_move(self):
        player = self.player.sprite
        if player.rect.x < 0 :
            self.shift_world(screen_width//2)
        elif player.rect.x > screen_width:
            self.shift_world(-screen_width//2)

    def shift_world(self, shift_x):
        self.worold_shift += shift_x
        for sprite in self.terrain_sprites.sprites():
            sprite.rect.x += shift_x
        for sprite in self.statek_sprites.sprites():
            sprite.rect.x += shift_x
        for sprite in self.zdrowie_sprites.sprites():
            sprite.rect.x += shift_x
        for sprite in self.enemy_sprites.sprites():
            sprite.rect.x += shift_x
        for sprite in self.kolizja_sprites.sprites():
            sprite.rect.x += shift_x
        for sprite in self.za_drabina_sprites.sprites():
            sprite.rect.x += shift_x
        for sprite in self.drabina_sprites.sprites():
            sprite.rect.x += shift_x
        self.player.sprite.rect.x += shift_x *2

    def run(self):
        self.climb_ladder()

        self.terrain_sprites.draw(self.display_surface)

        self.za_drabina_sprites.draw(self.display_surface)

        self.drabina_sprites.draw(self.display_surface)

        self.zdrowie_sprites.draw(self.display_surface)

        self.enemy_sprites.draw(self.display_surface)
        self.enemy_sprites.update(self.worold_shift)
        self.colision()
        self.cam_move()
        self.enemy_colision()
        self.statek_sprites.draw(self.display_surface)

        self.player.update()
        self.player.draw(self.display_surface)
        self.horizontal_movment_collision()
        self.vertical_movment_collision()
        self.text_points = Text(self.poinnts, pygame.color.THECOLORS['lightblue'],  1100, 50, font_size=76)
        self.text_points.draw(self.display_surface)
        self.interface.show_health()


