import pygame
class Tile(pygame.sprite.Sprite): #zapewni funkcje które tóre można wyświetlać na ekranie, manipulować nimi, wykrywać kolizje itp
    def __init__(self,pos,size):
        super().__init__()
        self.image = pygame.Surface((size,size)) #Tworzy nowy obiekt powierzchni (Surface) o określonym rozmiarze (size, size). size jest tutaj zmienną, która wskazuje na wymiar kafelka (np. szerokość i wysokość). Powierzchnia ta będzie służyć jako obrazek, który będzie reprezentował sprite'a.
        self.image.fill('purple')
        self.rect = self.image.get_rect(topleft=pos)
    def update(self,x_shift):
        self.rect.x += x_shift
