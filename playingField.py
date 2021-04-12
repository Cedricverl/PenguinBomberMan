import random
from Blocks import *
class PlayingField:
    def __init__(self, blocks, ice):
        self.blocks = blocks
        self.ice = ice
        self.bombs = []
        self.specialblocks = []  # sblocks(speedblock), bblock(bombblocks)

    def isOccupied(self, pos):
        return pos in self.getAllPos() or not self.isInside(pos)

    def isInside(self, pos):
        return 0 <= pos[0] < 14 and 0<=pos[1]<12

    def getAll(self):
        return self.blocks + self.ice + self.bombs + self.specialblocks

    def getAllBlocks(self):
        return self.blocks + self.ice + [bomb for bomb in self.bombs if not bomb.transparent]

    def getAllPos(self):
        return [a.pos for a in self.blocks + self.ice + [bomb for bomb in self.bombs if not bomb.transparent]]

    def canMove(self, pos, dir):
        if dir == "down":
            if (pos[0],pos[1]+1) in self.getAllPos():
                print(1)
                return False
        if dir == "up":
            if (pos[0],pos[1]-1) in self.getAllPos():
                print(2)
                return False
        if dir == "right":
            if (pos[0]+1,pos[1]) in self.getAllPos():
                print(3)
                # print("CANNOT MOVE")
                return False
        if dir == "left":
            if (pos[0]-1,pos[1]) in self.getAllPos():
                print(4)
                return False
        return True

    def getSpecialBlocks(self):
        return self.specialblocks

    def isIce(self, pos):
        return pos in [ice.pos for ice in self.ice]

    def removeIce(self, pos):
        self.ice = list(filter(lambda x: x.pos != pos, self.ice))
        self.specialblocks += [random.choice([Sblock(pos[0], pos[1]), Bblock(pos[0], pos[1]), Rblock(pos[0], pos[1])])] if random.random() < 0.5 else self.specialblocks

    def removeBomb(self, bomb):
        self.bombs.remove(bomb)

    def draw(self, surface):
        for entity in self.getAll():
            entity.draw(surface)
        # surface.blit()