import pygame, sys
from pygame.locals import *
import random

pygame.init()
pygame.font.init()
pygame.mixer.init()

myfont = pygame.font.SysFont("Arial", 30)
FPS = 60
FramePerSec = pygame.time.Clock()
SCREEN_WIDTH = 656
SCREEN_HEIGHT = 487
BLUE  = (0, 0, 255)
RED   = (255, 0, 0)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

Background = pygame.image.load("sprites/Background/Playingfield.png")
DISPLAYSURF = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
DISPLAYSURF.blit(Background, (0, 0))
# DISPLAYSURF.fill(WHITE)
pygame.display.set_caption("Bomberman")
# pygame.display.flip()
# pygame.mixer.music.load("sounds/oents.mp3")
# pygame.mixer.music.play(-1)
bombexplosion = pygame.mixer.Sound("sounds/Explode1.wav")
noleftright = set([(x, y) for x in range(0, 13, 2) for y in range(1, 10, 2)])
noupdown = set([(x, y) for x in range(1, 12, 2) for y in range(0, 11, 2)])
print("noleftright:", noleftright)
def determineSide(rect1, rect2):  # position of rect1 relative to rect2
    a=20
    if 0 < rect1.bottom - rect2.top < a:
        return "top"
    if 0 < rect1.right - rect2.left < a:
        return "left"
    if -a < rect1.left - rect2.right < 0:
        return "right"
    else:
        return "bottom"

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.surf = pygame.Surface((40,40))
        self.imagesize = (40, 40)
        self.images = {"left": pygame.transform.scale(pygame.image.load("sprites/Player1/Player1_left.png"), self.imagesize),
                       "right": pygame.transform.scale(pygame.image.load("sprites/Player1/Player1_right.png"), self.imagesize),
                       "bleft": pygame.transform.scale(pygame.image.load("sprites/Player_back/left.png"), self.imagesize),
                       "bright": pygame.transform.scale(pygame.image.load("sprites/Player_back/right.png"), self.imagesize)}
        self.vertdir = 0
        self.bombs = 1
        self.range = 2
        self.speed = 4
        self.image = pygame.transform.scale(self.images["left"], self.imagesize)

        # self.surf.fill(BLACK)
        self.rect = pygame.Rect(120, 30, self.surf.get_width(), self.surf.get_height())
        self.direction = (0, 0)
        self.space_held = False
    def get_square(self):
        x = (self.rect.centerx - 110) // 40
        y = (self.rect.centery - 20) // 40
        return x, y
    def update(self):
        x, y = self.get_square()
        # print(x, y)
        n = self.rect.collidelist([block.rect for block in blocks] + [block.rect for block in iceblocks] + [bomb.rect for bomb in bombs if not bomb.transparent])
        collision = True
        pressed_keys = pygame.key.get_pressed()
        # print(pressed_keys)
        if pressed_keys[K_SPACE]:
            if self.space_held == False:
                if self.bombs > 0:
                    bombs.append(Bomb(x, y))
                    self.bombs -= 1
                    self.space_held = True
        else: self.space_held = False
        print("n:",n)
        if n != -1:  # collision with block


            col_direction = determineSide(self.rect, (blocks+iceblocks+bombs)[n].rect)

            if col_direction == "top" or col_direction == "bottom":
                self.rect.left = 110+40*x
                self.rect.top = 20+40*y

            elif col_direction == "left" or col_direction == "right":
                self.rect.left = 110+40*x
                self.rect.top = 20+40*y
                    # = self.rect.update(110+40*x, 20+40*y, 35, 35)
            # print(col_direction)
            elif pressed_keys[K_UP]:
                if 20 < self.rect.top and col_direction != "bottom" and (x, y) not in noupdown:
                    self.move(0, -self.speed)

            elif pressed_keys[K_DOWN]:
                if self.rect.bottom < 460 and col_direction != "top" and (x, y) not in noupdown:
                    self.move(0,self.speed)

            elif pressed_keys[K_LEFT]:
                if 110 < self.rect.left  and col_direction != "right" and (x, y) not in noleftright:
                    self.move(-self.speed, 0)

            elif pressed_keys[K_RIGHT]:
                if self.rect.right < 630 and col_direction != "left" and (x, y) not in noleftright:
                    self.move(self.speed, 0)

            # if self.rect.colliderect(E1.rect):
            #     # print("COLLIDE")
            #     self.surf.fill(BLUE)
        else:
            # pressed_keys = pygame.key.get_pressed()

            if self.rect.top > 20 and (x, y) not in noupdown:
                if pressed_keys[K_UP]:
                    self.move(0, -self.speed)

            if self.rect.bottom < 460 and (x, y) not in noupdown:
                if pressed_keys[K_DOWN]:
                    self.move(0,self.speed)

            if 110 < self.rect.left and (x, y) not in noleftright:
                if pressed_keys[K_LEFT]:
                    self.move(-self.speed, 0)

            if self.rect.right < 630 and (x, y) not in noleftright:
                if pressed_keys[K_RIGHT]:
                    self.move(self.speed, 0)
        p = self.rect.collidelist([sblock.rect for sblock in speedblocks])
        if p != -1:  # collision with sblock
            b = speedblocks.pop(p)
            self.speed += b.speedplus
        q = self.rect.collidelist([bblock.rect for bblock in bombblocks])
        if q != -1:
            bombblocks.pop(q)
            self.bombs += 1

    def move(self, a, b):
        # print(self.vertdir)
        if a == 0:  # Vertial movement
            if abs(self.vertdir) > 20:
                if self.vertdir >= 0:
                    self.image = self.images["right"]
                    self.vertdir = -1
                else:
                    self.image = self.images["left"]
                    self.vertdir = 0
            else:
                self.vertdir = self.vertdir + 1 if self.vertdir >= 0 else self.vertdir - 1
                # self.vertdir -= 1 if self.vertdir < 0 else self.vertdir

        self.rect.move_ip(a, b)

    def draw(self, surface):
        surface.blit(self.image, self.rect)

class onscreendisplay():
    def draw(self, surface):
        textsurface = myfont.render("bombs: "+str(P1.bombs), False, (0, 0, 0))
        surface.blit(textsurface, (30, 20))

class Block(pygame.sprite.Sprite):
    def __init__(self, x, y, wall=False):
        super().__init__()
        self.x = 110+x*40
        self.y = 20+y*40
        self.width = 40
        self.height = 40
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

class Bblock(Block):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.img = pygame.image.load("sprites/Box/Box_bomb.png")

class Iblock(Block):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.img = pygame.image.load("sprites/Box/Box_ice.png")



class Bomb():
    def __init__(self, x, y):
        self.width = 40
        self.height = 40
        self.x = 110+x*40
        self.y = 20+y*40
        self.surf = pygame.Surface((self.width, self.height))
        self.surf.fill(RED)
        self.rect = Rect(self.x, self.y, self.width, self.height)
        self.img = pygame.image.load("sprites/Bomb_red/bomb.png")
        self.start_ticks = pygame.time.get_ticks()
        self.transparent = True

    def draw(self, surface):
        if (pygame.time.get_ticks() - self.start_ticks)/1000 >= 0.5:
            self.transparent = False
        if (pygame.time.get_ticks() - self.start_ticks)/1000 < 3:
            surface.blit(self.img, self.rect)
        else:
            bombexplosion.play()
            bombs.remove(self)
            P1.bombs += 1

blocks = [Block(1+2*x, 1+2*y, True) for x in range(6) for y in range(5)]
# blocks = [Block(152, 60, True), Block(230, 60, True), Block(308, 60, True), Block(386, 60, True), Block(464, 60, True), Block(542, 60, True),
#           Block(152, 138, True), Block(230, 138, True), Block(308, 138, True), Block(386, 138, True), Block(464, 138, True), Block(542, 138, True),
#           Block(152, 216, True), Block(230, 216, True), Block(308, 216, True), Block(386, 216, True), Block(464, 216, True), Block(542, 216, True),
#           Block(152, 294, True), Block(230, 294, True), Block(308, 294, True), Block(386, 294, True), Block(464, 294, True), Block(542, 294, True),
#           Block(152, 372, True), Block(230, 372, True), Block(308, 372, True), Block(386, 372, True), Block(464, 372, True), Block(542, 372, True)]
speedblocks = [Sblock(2, 3)]
bombblocks = [Bblock(1, 4)]
iceblocks = [Iblock(2, 1), Iblock(4, 4)]
bombs = []
P1 = Player()
# E1 = Enemy()
osd = onscreendisplay()

while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
    P1.update()


    DISPLAYSURF.blit(Background, (0,0))
    P1.draw(DISPLAYSURF)
    osd.draw(DISPLAYSURF)
    [block.draw(DISPLAYSURF) for block in blocks]
    [sblock.draw(DISPLAYSURF) for sblock in speedblocks]
    [bblock.draw(DISPLAYSURF) for bblock in bombblocks]
    [bomb.draw(DISPLAYSURF) for bomb in bombs]
    [iblock.draw(DISPLAYSURF) for iblock in iceblocks]


    pygame.display.update()
    FramePerSec.tick(FPS)
