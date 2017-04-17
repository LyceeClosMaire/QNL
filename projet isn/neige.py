import pygame
import math
import random
import time

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
rect_x = 50
rect_y = 50
rect_x_change = 5
rect_y_change = 5
snow_list = []
i = 0

done = False
screen = pygame.display.set_mode((700, 500))
clock = pygame.time.Clock()

class Flocon():

    def __init__(self):
        self.pos = [50, 50]

    def afficher(self):
        pygame.draw.circle(screen, WHITE, self.pos, 10)


flocon = Flocon()

# -------- Main Program Loop -----------
while not done:
    # --- Main event loop
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        elif event.type == pygame.KEYDOWN:
            print("L'utilisateur a appuye sur une touche")

    # --- Game logic should go here

    flocon.pos[0] = 250 + int(round(math.cos(i)*50, 2))
    flocon.pos[1] = i*5
    i += 1
    # --- Drawing code should go here
    screen.fill(BLACK)

    flocon.afficher()

    pygame.display.flip()

    clock.tick(60)

pygame.quit()