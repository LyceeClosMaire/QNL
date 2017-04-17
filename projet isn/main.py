import pygame
import math

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
rect_x = 50
rect_y= 50
rect_x_change = 0
rect_y_change = 0

done = False
screen = pygame.display.set_mode((700, 500), pygame.DOUBLEBUF)

clock = pygame.time.Clock()

# -------- Main Program Loop -----------
while not done:
    # --- Main event loop
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                rect_x_change = -5
                rect_y_change = 0
            elif event.key == pygame.K_RIGHT:
                rect_x_change = 5
                rect_y_change = 0
            elif event.key == pygame.K_UP:
                rect_y_change = -5
                rect_x_change = 0
            elif event.key == pygame.K_DOWN:
                rect_y_change = 5
                rect_x_change = 0
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT:
                rect_x_change = 0
            elif event.key == pygame.K_RIGHT:
                rect_x_change = 0
            elif event.key == pygame.K_UP:
                rect_y_change = 0
            elif event.key == pygame.K_DOWN:
                rect_y_change = 0

    # --- Game logic should go here

    # --- Drawing code should go here
    screen.fill(BLACK)

    rect_x += rect_x_change
    rect_y += rect_y_change

    pygame.draw.rect(screen, WHITE, [rect_x, rect_y, 50, 50])

    """if rect_y > 450 or rect_y < 0:
        rect_y_change *= -1
    if rect_x > 650 or rect_x < 0:
        rect_x_change *= -1"""

    pygame.display.flip()

    clock.tick(60)

pygame.quit()
