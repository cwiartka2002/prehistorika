import csv
import pygame
from os import walk
def import_csv_layout(path):
    terrain_map = []
    with open(path) as map:
        level = csv.reader(map, delimiter=',')
        for row in level:
            terrain_map.append(list(row))
        return terrain_map
def import_cut_graphics(path, tile_size,tile_size1):
    surface = pygame.image.load(path).convert_alpha()
    tile_num_x = surface.get_size()[0] // tile_size
    tile_num_y = surface.get_size()[1] // tile_size1
    cut_tiles = []
    for row in range( tile_num_y):
        for col in range( tile_num_x):
            x = col * tile_size
            y = row * tile_size1
            new_surf = pygame.Surface((tile_size, tile_size1))
            new_surf.blit(surface,(0,0), pygame.Rect(x,y,tile_size, tile_size1))
            cut_tiles.append(new_surf)
    return cut_tiles


def import_folder(path):
        surface_lisr = []
        print(path)
        for _, __, img_file in walk(path):
            for image in img_file:
                full_path = path + '/' + image
                image_surf = pygame.image.load(full_path).convert_alpha()
                surface_lisr.append(image_surf)

        return surface_lisr

