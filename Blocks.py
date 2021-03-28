import pygame
from pygame.locals import Rect

class Block(pygame.sprite.Sprite):
    def __init__(self, x, y, wall=False):
        super().__init__()
        self.x = x
        self.y = y
        self.width = 40
        self.height= 40
        # self.surf = pygame.Surface((self.width, self.height))
        # self.surf.fill(BLACK)
        self.rect = Rect(self.x, self.y, self.width, self.height)
        if wall:
            self.img = pygame.image.load("sprites/Stein/stein.png")
        # print("RECT: ", self.rect)
        # self.rect.move_ip(200, 200)
    def draw(self, surface):
        surface.blit(self.img, self.rect)

class Sblock(Block):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.speedplus = 1
        self.img = pygame.image.load("sprites/Box/Box_speed.png")
        self.width = 40
        self.height = 40

class Bblock(Block):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.img = pygame.image.load("sprites/Box/Box_bomb.png")
        self.width = 40
        self.height = 40