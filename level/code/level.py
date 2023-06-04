import pygame
from support import *
from settings import *
from Tile import *
class Level:
    def __init__(self, level_data, surface):
        self.worold_shift = -4
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
                        sprite = StaticTile(tile_size, x, y, tile_surface)

                    if type == 'drabina':
                            drabina_tile_list = import_cut_graphics('C:/Users/kacpe/OneDrive/Desktop/Prehistorika_by_kacper/graphics/teren/ladder/28x128/2.png',28,65)
                            drabina_surface = drabina_tile_list[int(val)]
                            sprite = StaticTile(tile_size, x, y, drabina_surface)

                    if type == 'zdrowie':
                        zdrowie_tile_list = import_cut_graphics('C:/Users/kacpe/OneDrive/Desktop/Prehistorika_by_kacper/graphics/teren/boxx.png',50,50)
                        zdrowie_surface = zdrowie_tile_list[int(val)]
                        sprite = Zdrowie(tile_size, x, y, zdrowie_surface)

                    if type == 'enemy':
                        sprite = Enemy(tile_size, x, y)


                    if type == 'kolizja':
                        sprite = tile(tile_size,x, y)

                    if type == 'statek':
                        statek_tile_list = import_cut_graphics('C:/Users/kacpe/OneDrive/Desktop/Prehistorika_by_kacper/graphics/teren/Ship/ship13.png', 64, 64)
                        statek_surface = statek_tile_list[int(val)]
                        sprite = Statek(tile_size, x, y, statek_surface)
                    sprite_group.add(sprite)
        return sprite_group
    def setup_player(self,layout):
        for index, row in enumerate(layout):
            for col_index, val in enumerate(row):
                if val != '-1':
                    print("tutaj")

    def colision(self):
        for enemy in self.enemy_sprites.sprites():
            if pygame.sprite.spritecollide(enemy, self.kolizja_sprites, False):
                enemy.direction()



    def run(self):
        self.terrain_sprites.draw(self.display_surface)
        self.terrain_sprites.update(self.worold_shift)
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
