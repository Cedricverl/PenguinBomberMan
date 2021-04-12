import pygame
pygame.font.init()

myfont = pygame.font.SysFont("Arial", 30)
FPS = 60
FramePerSec = pygame.time.Clock()
SCREEN_WIDTH = 656
SCREEN_HEIGHT = 487
BLUE = (0, 0, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

Background = pygame.image.load("sprites/Background/Playingfield.png")
DISPLAYSURF = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
DISPLAYSURF.blit(Background, (0, 0))
pygame.display.set_caption("Bomberman")