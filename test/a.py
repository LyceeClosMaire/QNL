import pygame

done = False

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

clock = pygame.time.Clock()
screen = pygame.display.set_mode((700, 500))

class Bomberman():

    def __init__(self):
        self.droite = pygame.image.load("droite.png")
        self.dos = pygame.image.load("dos.png")
        self.face = pygame.image.load("face.png")
        self.gauche = pygame.image.load("gauche.png")
        self.vitesse_x = 0
        self.vitesse_y = 0
        self.pos = [50, 50]
        self.direction = "face"

    def afficher(self):
        if self.direction == "face":
            screen.blit(bomberman.face, self.pos)
        elif self.direction == "dos":
            screen.blit(bomberman.dos, self.pos)
        elif self.direction == "gauche":
            screen.blit(bomberman.gauche, self.pos)
        elif self.direction == "droite":
            screen.blit(bomberman.droite, self.pos)


bomberman = Bomberman()

# -------- Main Program Loop -----------
while not done:
    # --- Main event loop
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                bomberman.direction = "gauche"
                bomberman.vitesse_x = -5
                bomberman.vitesse_y = 0
            elif event.key == pygame.K_RIGHT:
                bomberman.direction = "droite"
                bomberman.vitesse_x = 5
                bomberman.vitesse_y = 0
            elif event.key == pygame.K_UP:
                bomberman.direction = "dos"
                bomberman.vitesse_y = -5
                bomberman.vitesse_x = 0
            elif event.key == pygame.K_DOWN:
                bomberman.direction = "face"
                bomberman.vitesse_y = 5
                bomberman.vitesse_x = 0
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                bomberman.vitesse_x = 0
            elif event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                bomberman.vitesse_y = 0

    # --- Game logic should go here
    print(bomberman.pos)

    # --- Drawing code should go here
    screen.fill(BLACK)

    bomberman.pos[0] += bomberman.vitesse_x
    bomberman.pos[1] += bomberman.vitesse_y
    bomberman.afficher()

    pygame.display.flip()

    clock.tick(60)

pygame.quit()