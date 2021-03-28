import pygame
from main import *

class Bomb():
    def __init__(self, x, y):
        self.width = 40
        self.height = 40
        self.surf = pygame.Surface((self.width, self.height))
        self.surf.fill(RED)
        self.rect = Rect(x, y, self.width, self.height)
        self.img = pygame.image.load("sprites/Bomb_red/bomb.png")
        self.start_ticks = pygame.time.get_ticks()

    def draw(self, surface):
        if (pygame.time.get_ticks() - self.start_ticks)/1000 < 3:
            surface.blit(self.img, self.rect)
        else:
            bombexplosion.play()
            bombs.remove(self)