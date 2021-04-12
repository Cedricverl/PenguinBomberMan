import pygame
from pygame.locals import Rect

class Block(pygame.sprite.Sprite):
    def __init__(self, x, y, wall=False):
        super().__init__()
        self.x = 110+x*40
        self.y = 20+y*40
        self.pos = (x, y)
        self.width = 40
        self.height = 40
        self.rect = Rect(self.x, self.y, self.width, self.height)
        if wall:
            self.img = pygame.image.load("sprites/Stein/stein.png")

    def draw(self, surface):
        surface.blit(self.img, self.rect)


class Sblock(Block):  # Speed block
    def __init__(self, x, y):
        super().__init__(x, y)
        self.speedplus = 1
        self.img = pygame.image.load("sprites/Box/Box_speed.png")

    def handle(self, player):
        player.speed += 1


class Bblock(Block):  # Bomb block
    def __init__(self, x, y):
        super().__init__(x, y)
        self.img = pygame.image.load("sprites/Box/Box_bomb.png")

    def handle(self, player):
        player.bombs += 1


class Iblock(Block):  # Ice block
    def __init__(self, x, y):
        super().__init__(x, y)
        self.img = pygame.image.load("sprites/Box/Box_ice.png")

class Rblock(Block):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.img = pygame.image.load("sprites/Box/Box_blast.png")

    def handle(self, player):
        player.range += 1