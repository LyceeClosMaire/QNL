import pygame
from pygame.locals import *
import time

pygame.init()

a = True
i = 50
screen = pygame.display.set_mode((1920, 1080), FULLSCREEN)

bomberman = pygame.image.load("bbm.png")
rotated = pygame.transform.rotate(bomberman, 45)
screen.blit(rotated, (50,100))
background = pygame.image.load("espace.jpg")
clock = pygame.time.Clock()
son = pygame.mixer.Sound("shst.wav")
son.play(loops=-1)
FRAMES_PER_SECOND = 60
deltat = clock.tick(FRAMES_PER_SECOND)


while a:
    screen.fill((0,0,0))
    screen.blit(background, (-i,0))
    i += 1
    screen.blit(rotated, (50, 100))
    rotated = pygame.transform.rotate(bomberman, i)
    #background = pygame.transform.rotate(background, -i)
    pygame.display.flip()

    for event in pygame.event.get():
        if event.type == QUIT or (event.type == KEYUP and event.key == K_ESCAPE):
            a = False
pygame.quit()