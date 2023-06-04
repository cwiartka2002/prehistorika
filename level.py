from level.code.player import *
from level.code.drabina import *
class Level:
    def __init__(self, level_data, surface):
        self.display_surface = surface
        self.setup_level(level_data)
        self.world_shift = 0
        self.current_x = 0

    def setup_level(self,layout):
        self.tiles = pygame.sprite.Group()
        self.player = pygame.sprite.GroupSingle()
        self.drabina= pygame.sprite.Group()
        for row_number,row in enumerate(layout): # zwraca rząd i numer rzędu
            for col_number,cell in enumerate(row):
                x = col_number * tile_size
                y = row_number * tile_size
                if cell == 'X':
                    tile =  Tile((x,y), tile_size)
                    self.tiles.add(tile)
                if cell == 'P':
                    player_sprite = Player((x, y))
                    self.player.add(player_sprite)
                if cell == 'D':
                    drabina =  Drabina((x, y), ladder_size)
                    self.drabina.add(drabina)

    def scroll_x(self):
        player = self.player.sprite
        player_x = player.rect.centerx
        direction_x = player.direction.x
        if player_x < 200 and direction_x < 0:
            self.world_shift = 9
            player.speed = 0
        elif player_x >= 1000 and direction_x > 0:
            self.world_shift = -9
            player.speed = 0
        else:
            self.world_shift = 0
            player.speed = 8

    def horizontal_movment_collision(self):
        player = self.player.sprite
        player.rect.x += player.direction.x * player.speed


        for sprite in self.tiles.sprites():
            if sprite.rect.colliderect(player.rect):
                if player.direction.x <0:
                    player.rect.left = sprite.rect.right
                    player.on_left = True
                    self.current_x = player.rect.left
                elif player.direction.x >0:
                    player.rect.right = sprite.rect.left
                    player.on_right = True
                    self.current_x = player.rect.right
            if player.on_left and (player.rect.left < self.current_x or player.direction.x >= 0):
                player.on_left = False
            if player.on_right and (player.rect.right > self.current_x or player.direction.x <= 0):
                player.on_right = False

    def climb_ladder(self):
        player = self.player.sprite

        ladder_collision = pygame.sprite.spritecollide(player, self.drabina, False)
        if ladder_collision:
            player.climb()


    def vertical_movment_collision(self):

        player = self.player.sprite
        player.apply_gravity()

        for sprite in self.tiles.sprites():
            if sprite.rect.colliderect(player.rect):
                if player.direction.y >0:
                    player.rect.bottom = sprite.rect.top
                    player.jump_flag = False
                    player.direction.y = 0
                    player.on_ground = True
                elif player.direction.y <0:
                    player.rect.top = sprite.rect.bottom
                    player.direction.y = 0
                    player.on_ceiling = True
                if player.on_ground and player.direction.y < 0 or player.direction.y > 1:

                    player.on_ground = False
                if player.on_ceiling and player.direction.y > 0:

                    player.on_ceiling = False





    def run(self):
        self.climb_ladder()
        self.tiles.update(self.world_shift)
        self.drabina.update(self.world_shift)
        self.tiles.draw(self.display_surface)
        self.drabina.draw(self.display_surface)
        self.player.update()
        self.horizontal_movment_collision()
        self.vertical_movment_collision()
        self.climb_ladder()
        self.player.draw(self.display_surface)
        self.scroll_x()
