import pygame
from support import *
from settings import *
from Tile import *
from player import *
from drabina import *
import time
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
        obiekty_kolizja = self.terrain_sprites.sprites()  + self.statek_sprites.sprites()+ self.zdrowie_sprites.sprites() + self.enemy_sprites.sprites()
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
        obiekty_kolizja = self.terrain_sprites.sprites()  + self.statek_sprites.sprites() + self.zdrowie_sprites.sprites() + self.enemy_sprites.sprites()

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

    def attack(self):
        player = self.player.sprite
        enemy_collide = pygame.sprite.spritecollide(player, self.enemy_sprites, False)
        if enemy_collide:

            enemy = enemy_collide[0]
            enemy.hitted()




    def run(self):
        self.climb_ladder()
        self.attack()
        self.terrain_sprites.draw(self.display_surface)
        self.terrain_sprites.update(self.worold_shift)
        self.za_drabina_sprites.draw(self.display_surface)
        self.za_drabina_sprites.update(self.worold_shift)
        self.drabina_sprites.draw(self.display_surface)
        self.drabina_sprites.update(self.worold_shift)
        self.zdrowie_sprites.draw(self.display_surface)
        self.zdrowie_sprites.update(self.worold_shift)
        self.enemy_sprites.draw(self.display_surface)
        self.enemy_sprites.update(self.worold_shift)
        self.colision()
        self.kolizja_sprites.update(self.worold_shift)
        self.statek_sprites.draw(self.display_surface)
        self.statek_sprites.update(self.worold_shift)
        self.player.update()
        self.player.draw(self.display_surface)
        self.horizontal_movment_collision()
        self.vertical_movment_collision()

