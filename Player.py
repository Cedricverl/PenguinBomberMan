import pygame
from main import *
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.surf = pygame.Surface((30, 42))

        self.images = {"left": pygame.transform.scale(pygame.image.load("sprites/Player1/Player1_left.png"), self.surf.get_size()),
                       "right": pygame.transform.scale(pygame.image.load("sprites/Player1/Player1_right.png"), self.surf.get_size()),
                       "bleft": pygame.transform.scale(pygame.image.load("sprites/Player_back/left.png"), self.surf.get_size()),
                       "bright": pygame.transform.scale(pygame.image.load("sprites/Player_back/right.png"), self.surf.get_size())}
        self.vertdir = 0
        self.bombs = 0
        self.range = 2
        self.speed = 4
        self.image = pygame.transform.scale(self.images["left"], self.surf.get_size())

        # self.surf.fill(BLACK)
        self.rect = pygame.Rect(120, 30, self.surf.get_width(), self.surf.get_height())
        self.direction = (0, 0)

    def update(self):
        print(self.rect.center)
        n = self.rect.collidelist([block.rect for block in blocks])
        collision = True
        pressed_keys = pygame.key.get_pressed()
        if pressed_keys[K_SPACE]:
            if self.bombs > 0:
                bombs.append(Bomb(self.rect.x, self.rect.y))
                self.bombs -= 1

        if n != -1:  # collision with block

            col_direction = determineSide(self.rect, blocks[n].rect)

            if pressed_keys[K_UP]:
                if 0 < self.rect.top and col_direction != "bottom":
                    self.move(0, -self.speed)

            if pressed_keys[K_DOWN]:
                if self.rect.bottom < SCREEN_HEIGHT and col_direction != "top":
                    self.move(0,self.speed)

            if pressed_keys[K_LEFT]:
                if 110 < self.rect.left  and col_direction != "right":
                    self.move(-self.speed, 0)

            if pressed_keys[K_RIGHT]:
                if self.rect.right < SCREEN_WIDTH - 20 and col_direction != "left":
                    self.move(self.speed, 0)

            # if self.rect.colliderect(E1.rect):
            #     # print("COLLIDE")
            #     self.surf.fill(BLUE)
        else:
            pressed_keys = pygame.key.get_pressed()

            if self.rect.top > 0:
                if pressed_keys[K_UP]:
                    self.move(0, -self.speed)

            if self.rect.bottom < SCREEN_HEIGHT-5:
                if pressed_keys[K_DOWN]:
                    self.move(0,self.speed)

            if 110 < self.rect.left :
                if pressed_keys[K_LEFT]:
                    self.move(-self.speed, 0)

            if self.rect.right < SCREEN_WIDTH-20:
                if pressed_keys[K_RIGHT]:
                    self.move(self.speed, 0)
        p = self.rect.collidelist([sblock.rect for sblock in speedblocks])
        if p != -1:  # collision with sblock
            b = speedblocks.pop(p)
            self.speed += b.speedplus
        q = self.rect.collidelist([bblock.rect for bblock in bombblocks])
        if q != -1:
            print("wdfqsf")
            bombblocks.pop(q)
            self.bombs += 1

    def move(self, a, b):
        print(self.vertdir)
        if a == 0:  # Vertial movement
            print("VERTICLA")
            if abs(self.vertdir) > 20:
                if self.vertdir >= 0:
                    self.image = self.images["right"]
                    self.vertdir = -1
                else:
                    self.image = self.images["left"]
                    self.vertdir = 0
            else:
                print("EHRE")
                self.vertdir = self.vertdir + 1 if self.vertdir >= 0 else self.vertdir - 1
                # self.vertdir -= 1 if self.vertdir < 0 else self.vertdir

        self.rect.move_ip(a, b)

    def draw(self, surface):
        surface.blit(self.image, self.rect)

def determineSide(rect1, rect2):  # position of rect1 relative to rect2
    if 0 < rect1.bottom - rect2.top < 10:
        return "top"
    if 0 < rect1.right - rect2.left < 10:
        return "left"
    if -10 < rect1.left - rect2.right < 0:
        return "right"
    else:
        return "bottom"