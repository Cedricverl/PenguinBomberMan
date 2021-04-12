import pygame, sys
from pygame.locals import *
import random
from config import *
pygame.init()
pygame.mixer.init()
from playingField import PlayingField
from Blocks import *
# pygame.display.flip()
# pygame.mixer.music.load("sounds/oents.mp3")
# pygame.mixer.music.play(-1)

bombexplosion = pygame.mixer.Sound("sounds/Explode1.wav")

blockpositions = [(1+2*x, 1+2*y) for x in range(6) for y in range(5)]
ice_entries = [(x, y) for x in range(13) for y in range(11) if (x, y) not in blockpositions + [(0, 0), (1, 0), (2, 0), (0, 1), (0, 2), (10, 10), (11, 10), (12, 10), (12, 9), (12, 8)]]
# noleftright = set([(x, y) for x in range(0, 13, 2) for y in range(1, 10, 2)])
# noupdown = set([(x, y) for x in range(1, 11, 2) for y in range(1, 9, 2)])
# print("noleftright:", noleftright)


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
        self.speed = 5
        self.img = pygame.transform.scale(self.images["left"], self.imagesize)

        # self.surf.fill(BLACK)
        self.rect = pygame.Rect(120, 30, self.surf.get_width(), self.surf.get_height())
        self.direction = (0, 0)
        self.space_held = False

    def get_square(self):
        x = (self.rect.centerx - 110) // 40
        y = (self.rect.centery - 20) // 40
        return x, y

    def is_centeredx(self):
        # print((self.rect.centerx-110)%40, (self.rect.centery-20)%40)
        return (self.rect.centerx-110)%40==20

    def is_centeredy(self):
        return (self.rect.centery-20)%40==20

    def update(self):
        x, y = self.get_square()
        # print(x, y)
        n = self.rect.collidelist([block.rect for block in playingField.getAllBlocks()])
        pressed_keys = pygame.key.get_pressed()
        # print(pressed_keys)
        if pressed_keys[K_SPACE]:
            if self.space_held == False:
                if self.bombs > 0:
                    print("Bomb dropped at ", x, y)
                    playingField.bombs.append(Bomb(x, y, self.range))
                    self.bombs -= 1
                    self.space_held = True
        else: self.space_held = False
        # print("n:",n)
        # print(self.is_centeredx())
        # print("rect:", self.rect)
        # print(x, y)
        if n != -1:  # collision with block

            # print("COLLISIOSN")
            col_direction = determineSide(self.rect, (playingField.getAllBlocks())[n].rect)

            if col_direction == "top" or col_direction == "bottom":
                self.rect.left = 110+40*x
                self.rect.top = 20+40*y

            elif col_direction == "left" or col_direction == "right":
                self.rect.left = 110+40*x
                self.rect.top = 20+40*y

            elif pressed_keys[K_UP]:
                if 20 < self.rect.top and col_direction != "bottom" and playingField.canMove((x, y), "up") or not self.is_centeredy():
                    self.move(0, -self.speed)

            elif pressed_keys[K_DOWN]:
                if self.rect.bottom < 460 and col_direction != "top" and playingField.canMove((x, y), "down") or not self.is_centeredy():
                    self.move(0,self.speed)

            elif pressed_keys[K_LEFT]:
                if 110 < self.rect.left  and col_direction != "right" and playingField.canMove((x, y), "left") or not self.is_centeredx():
                    self.move(-self.speed, 0)

            elif pressed_keys[K_RIGHT]:
                if self.rect.right < 629 and col_direction != "left" and playingField.canMove((x, y), "right") or not self.is_centeredx():
                    self.move(self.speed, 0)

        else:
            if self.rect.top > 20 and playingField.canMove((x, y), "up") or not self.is_centeredy():
                if pressed_keys[K_UP]:
                    self.move(0, -self.speed)

            if self.rect.bottom < 460 and playingField.canMove((x, y), "down") or not self.is_centeredy():
                if pressed_keys[K_DOWN]:
                    self.move(0,self.speed)

            if 110 < self.rect.left and playingField.canMove((x, y), "left") or not self.is_centeredx():
                if pressed_keys[K_LEFT]:
                    self.move(-self.speed, 0)

            if self.rect.right < 630 and playingField.canMove((x, y), "right") or not self.is_centeredx():
                # print("cando?")
                if pressed_keys[K_RIGHT]:
                    self.move(self.speed, 0)
        p = self.rect.collidelist(playingField.specialblocks)
        if p != -1:  # collision with sblock
            b = playingField.specialblocks.pop(p)
            b.handle(self)

    def move(self, a, b):
        if a == 0:  # Vertial movement
            if abs(self.vertdir) > 20:
                if self.vertdir >= 0:
                    self.img = self.images["right"]
                    self.vertdir = -1
                else:
                    self.img = self.images["left"]
                    self.vertdir = 0
            else:
                self.vertdir = self.vertdir + 1 if self.vertdir >= 0 else self.vertdir - 1
        self.rect.move_ip(a, b)

    def draw(self, surface):
        surface.blit(self.img, self.rect)


class onscreendisplay():
    def draw(self, surface):
        textsurface = myfont.render("bombs: "+str(P1.bombs), False, (0, 0, 0))
        surface.blit(textsurface, (30, 20))


# class Block(pygame.sprite.Sprite):
#     def __init__(self, x, y, wall=False):
#         super().__init__()
#         self.x = 110+x*40
#         self.y = 20+y*40
#         self.pos = (x, y)
#         self.width = 40
#         self.height = 40
#         self.rect = Rect(self.x, self.y, self.width, self.height)
#         if wall:
#             self.img = pygame.image.load("sprites/Stein/stein.png")
#
#     def draw(self, surface):
#         surface.blit(self.img, self.rect)


# class Sblock(Block):
#     def __init__(self, x, y):
#         super().__init__(x, y)
#         self.speedplus = 1
#         self.img = pygame.image.load("sprites/Box/Box_speed.png")
#
#
# class Bblock(Block):
#     def __init__(self, x, y):
#         super().__init__(x, y)
#         self.img = pygame.image.load("sprites/Box/Box_bomb.png")
#
#
# class Iblock(Block):
#     def __init__(self, x, y):
#         super().__init__(x, y)
#         self.img = pygame.image.load("sprites/Box/Box_ice.png")



class Bomb():
    def __init__(self, x, y, range):
        self.width = 40
        self.height = 40
        self.range = range
        self.x = 110+x*40
        self.y = 20+y*40
        self.pos = (x, y)
        self.square = (x, y)
        self.surf = pygame.Surface((self.width, self.height))
        self.surf.fill(RED)
        self.rect = Rect(self.x, self.y, self.width, self.height)
        self.img = pygame.image.load("sprites/Bomb_red/bomb.png")
        self.explimg = pygame.transform.scale(pygame.image.load("sprites/BlastsequenceYellow/1.png"), (40, 40))
        self.start_ticks = pygame.time.get_ticks()
        self.transparent = True
        self.exploded = False
        self.exsequencenumb = 1

    def draw(self, surface):
        if self.exploded:
            if 0 < self.exsequencenumb <= 60:
                for pos in self.explosionPos:
                    surface.blit(self.explimg, (110+40*pos[0], 20+40*pos[1], 40, 40))
                self.exsequencenumb += 1

            if self.exsequencenumb <= 20:
                self.img = pygame.transform.scale(pygame.image.load(f"sprites/Explosionsequence/{self.exsequencenumb}.png"), (40, 40))
                surface.blit(self.img, self.rect)
            else:
                playingField.removeBomb(self)
        else:
            if self.transparent and P1.get_square() != self.square:
                self.transparent = False
            if (pygame.time.get_ticks() - self.start_ticks)/1000 < 3:
                surface.blit(self.img, self.rect)
            else:
                self.exploded = True
                self.explosionPos = self.getExplosionPos(playingField)
                self.explosiontime = pygame.time.get_ticks()
                # bombexplosion.play()
                P1.bombs += 1
    # def get_coord(self):
    #     x = (self.rect.centerx - 110) // 40
    #     y = (self.rect.centery - 20) // 40
    #     return x, y
    def getExplosionPos(self, playingField):
        possible_pos = [self.pos]
        for i in range(1, self.range):
            if not playingField.isOccupied((self.pos[0], self.pos[1]+i)):
                possible_pos.append((self.pos[0], self.pos[1]+i))
            else:
                if playingField.isIce((self.pos[0], self.pos[1]+i)):
                    playingField.removeIce((self.pos[0], self.pos[1]+i))
                    possible_pos.append((self.pos[0], self.pos[1]+i))
                break

        for i in range(1, self.range):
            if not playingField.isOccupied((self.pos[0], self.pos[1]-i)):
                possible_pos.append((self.pos[0], self.pos[1]-i))
            else:
                if playingField.isIce((self.pos[0], self.pos[1]-i)):
                    playingField.removeIce((self.pos[0], self.pos[1]-i))
                    possible_pos.append((self.pos[0], self.pos[1]-i))
                break

        for i in range(1, self.range):
            if not playingField.isOccupied((self.pos[0]+i, self.pos[1])):
                possible_pos.append((self.pos[0]+i, self.pos[1]))
            else:
                if playingField.isIce((self.pos[0]+i, self.pos[1])):
                    playingField.removeIce((self.pos[0]+i, self.pos[1]))
                    possible_pos.append((self.pos[0]+i, self.pos[1]))
                break

        for i in range(1, self.range):
            if not playingField.isOccupied((self.pos[0]-i, self.pos[1])):
                possible_pos.append((self.pos[0]-i, self.pos[1]))
            else:
                if playingField.isIce((self.pos[0]-i, self.pos[1])):
                    playingField.removeIce((self.pos[0]-i, self.pos[1]))
                    possible_pos.append((self.pos[0]-i, self.pos[1]))
                break

        return possible_pos


blocks = [Block(1+2*x, 1+2*y, True) for x in range(6) for y in range(5)]
iceblocks = list(map(lambda x: Iblock(x[0], x[1]), list(set([random.choice(ice_entries) for _ in ice_entries]))))

playingField = PlayingField(blocks, iceblocks)
P1 = Player()
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
    playingField.draw(DISPLAYSURF)
    # [block.draw(DISPLAYSURF) for block in blocks]
    # [sblock.draw(DISPLAYSURF) for sblock in speedblocks]
    # [bblock.draw(DISPLAYSURF) for bblock in bombblocks]
    # [bomb.draw(DISPLAYSURF) for bomb in bombs]
    # [iblock.draw(DISPLAYSURF) for iblock in iceblocks]


    pygame.display.update()
    FramePerSec.tick(FPS)
