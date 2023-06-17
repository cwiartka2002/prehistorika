import pygame
from support import *
from settings import *
from Tile import *
from player import *
from drabina import *
import os
from game_over import *
from inforamacje import *
class Level:
    def __init__(self, level_data, surface):
        self.world_shift = 0
        self.display_surface = surface
        player_layout = import_csv_layout(level_data['player'])
        self.player = pygame.sprite.GroupSingle()
        self.setup_player(player_layout)
        ship_layout = import_csv_layout(level_data['ship'])
        self.ship_sprites = self.create_tile_group(ship_layout, 'ship')
        terrain_layout = import_csv_layout(level_data['terrain'])
        self.terrain_sprites = self.create_tile_group(terrain_layout, 'terrain')
        ladder_layout = import_csv_layout(level_data['ladder'])
        self.ladder_sprites = self.create_tile_group(ladder_layout, 'ladder')
        enemy_layout = import_csv_layout(level_data['enemy'])
        self.enemy_sprites = self.create_tile_group(enemy_layout, 'enemy')
        crate_layout = import_csv_layout(level_data['crate'])
        self.crate_sprites = self.create_tile_group(crate_layout, 'crate')
        collision_layout = import_csv_layout(level_data['collision'])
        self.collision_sprites = self.create_tile_group(collision_layout, 'collision')
        behind_ladder_layout = import_csv_layout(level_data['behind_ladder'])
        self.behind_ladder_sprites = self.create_tile_group(behind_ladder_layout, 'behind_ladder')
        health_layout = import_csv_layout(level_data['health'])
        self.health_sprites = self.create_tile_group(health_layout, 'health')
        self.flag_cam_move = False
        self.pd = 0
        self.points = 0
        self.lives = 1
        self.interface = UI(pygame.display.set_mode((screen_width, screen_height)))
        self.enemy_flag = False
        self.crate_flag = False
        self.end_game = False
        self.counter = 0
        self.game_over = GameOverScreen(self.display_surface)

    def create_tile_group(self, layout, type):
        sprite_group = pygame.sprite.Group()
        for index, row in enumerate(layout):
            for col_index, val in enumerate(row):
                if val != '-1':
                    x = col_index * tile_size
                    y = index * tile_size
                    if type == 'terrain':
                        terrain_tile_list = import_cut_graphics('graphics/teren/[64x64] Rocky Grass.png', tile_size, tile_size)
                        tile_surface = terrain_tile_list[int(val)]
                        sprite = StaticTile(tile_size, tile_size, x, y, tile_surface)
                    elif type == 'ladder':
                        drabina_surface = pygame.image.load('C:/Users/kacpe/OneDrive/Desktop/Prehistorika_by_kacper/graphics/teren/ladder/28x128/2.png')
                        sprite = StaticTile(28, 64, x, y, drabina_surface)
                    elif type == 'crate':
                        path = 'graphics/teren/box/'
                        sprite = Skrzynka(64, 64, x, y, path)
                    elif type == 'behind_ladder':
                        behind_ladder_surface = import_cut_graphics('graphics/teren/[64x64] Rocky Grass.png', tile_size, tile_size)
                        behind_ladder_surface = behind_ladder_surface[int(val)]
                        sprite = StaticTile(tile_size, tile_size, x, y, behind_ladder_surface)
                    elif type == 'enemy':
                        sprite = Enemy(tile_size, tile_size, x, y)
                    elif type == 'collision':
                        sprite = tile(tile_size, tile_size, x, y)
                    elif type == 'ship':
                        ship_tile_list = import_cut_graphics('graphics/teren/Ship/ship13.png', 64, 64)
                        ship_surface = ship_tile_list[int(val)]
                        sprite = Ship(tile_size, tile_size, x, y, ship_surface)
                    elif type == 'health':
                        health_surface = pygame.image.load('graphics/teren/hearths/2.png')
                        sprite = Health(64, 64, x, y, health_surface)
                    sprite_group.add(sprite)
        return sprite_group

    def setup_player(self, layout):
        for index, row in enumerate(layout):
            for col_index, val in enumerate(row):
                x = col_index * tile_size
                y = index * tile_size
                if val != '-1':
                    sprite = Player((x, y))
                    self.player.add(sprite)

    def collision(self):
        for enemy in self.enemy_sprites.sprites():
            if pygame.sprite.spritecollide(enemy, self.collision_sprites, False):
                enemy.change_direction()

    def horizontal_movement_collision(self):
        player = self.player.sprite
        player.rect.x += player.direction.x * player.speed
        collision_objects = self.terrain_sprites.sprites()
        for sprite in collision_objects:
            if sprite.rect.colliderect(player.rect):
                if player.direction.x < 0:
                    player.rect.left = sprite.rect.right
                    self.current_x = player.rect.left
                elif player.direction.x > 0:
                    player.rect.right = sprite.rect.left
                    self.current_x = player.rect.right

    def climb_ladder(self):
        player = self.player.sprite
        ladder_collision = pygame.sprite.spritecollide(player, self.ladder_sprites, False)
        if ladder_collision:
            player.na_drabinie = True
            player.jump_flag = True
            player.climb()

    def vertical_movement_collision(self):
        player = self.player.sprite
        player.apply_gravity()
        collision_objects = self.terrain_sprites.sprites()
        for sprite in collision_objects:
            if sprite.rect.colliderect(player.rect):
                if player.direction.y > 0:
                    player.rect.bottom = sprite.rect.top
                    player.jump_flag = False
                    player.direction.y = 0
                    player.on_ground = True
                elif player.direction.y < 0:
                    player.rect.top = sprite.rect.bottom
                    player.direction.y = 0

    def crate_collision(self):
        collision = pygame.sprite.spritecollide(self.player.sprite, self.crate_sprites, False)
        if collision and not self.crate_flag:
            for crate in collision:
                if self.player.sprite.status == 'attack':
                    crate.destroy()
                    self.collect_health()
                    self.crate_flag = True
        elif not collision:
            self.crate_flag = False

    def collect_health(self):
        collision = pygame.sprite.spritecollide(self.player.sprite, self.health_sprites, False)
        if collision:
            for health in collision:
                self.interface.update_health(-1)
                health.kill()

    def enemy_collision(self):
        player = self.player.sprite
        collision = pygame.sprite.spritecollide(player, self.enemy_sprites, False)
        if collision and not self.enemy_flag:
            for enemy in collision:
                if player.status == 'attack':
                    enemy.stun()
                    enemy.stun()
                elif enemy.stunned:
                    self.points += 100
                    enemy.kill()
                else:
                    if (not enemy.moving_left and player.facing_right) or (enemy.moving_left and not player.facing_right):
                        enemy.change_direction()
                    if player.facing_right:
                        player.rect.x -= 30
                    else:
                        player.rect.x += 30
                    player.hit()
                    if self.interface.update_health(1):
                        self.lives -= 1
            self.enemy_flag = True
        elif not collision:
            self.enemy_flag = False

    def camera_movement(self):
        player = self.player.sprite
        if 0 <= self.counter < 3:
            if player.rect.x < 0:
                self.shift_world(screen_width // 2)
                self.counter -= 1
            elif player.rect.x > screen_width:
                self.shift_world(-screen_width // 2)
                self.counter += 1
        else:
            self.shift_world(0)

    def shift_world(self, shift_x):
        self.world_shift += shift_x
        objects = self.terrain_sprites.sprites() + self.ship_sprites.sprites() + self.crate_sprites.sprites() + self.enemy_sprites.sprites() + self.collision_sprites.sprites() + self.ladder_sprites.sprites() + self.health_sprites.sprites()
        for sprite in objects:
            sprite.rect.x += shift_x
        self.player.sprite.rect.x += shift_x * 2

    def game_over_check(self):
        if self.lives == 0 or self.player.sprite.rect.y > screen_height + 500 and not self.end_game:
            self.gameover.display_game_over("GAME OVER")

    def move_ship(self):
        player = self.player.sprite
        ship_collision = pygame.sprite.spritecollide(player, self.ship_sprites, False)
        if ship_collision:
            for ship in ship_collision:
                ship.rect.x += 10
                player.gravity = 0
                player.rect.x = ship.rect.x
                if ship.rect.x > 1200 or self.game_over:
                    self.gameover.display_game_over("Gratualcje")

                player.on_ship = True
        else:
            player.gravity = 0.5

    def run(self):
        self.climb_ladder()
        self.ladder_sprites.draw(self.display_surface)
        self.terrain_sprites.draw(self.display_surface)
        self.ship_sprites.draw(self.display_surface)
        self.crate_sprites.draw(self.display_surface)
        self.enemy_sprites.draw(self.display_surface)
        self.enemy_sprites.update(self.world_shift)
        self.collision()
        self.camera_movement()
        self.enemy_collision()
        self.crate_collision()
        self.player.update()
        self.player.draw(self.display_surface)
        self.horizontal_movement_collision()
        self.vertical_movement_collision()
        self.points_text = Text(self.points, pygame.color.THECOLORS['lightblue'], 1100, 50, font_size=76)
        self.lives_text = Text(self.lives, pygame.color.THECOLORS['red'], 500, 50, font_size=76)
        self.points_text.draw(self.display_surface)
        self.lives_text.draw(self.display_surface)
        self.interface.show_health()
        self.move_ship()
        self.game_over_check()

