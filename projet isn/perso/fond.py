# Créé par CLERCL, le 27/03/2017 en Python 3.2

import pygame

done = False

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BG_SPRITES = (33, 57, 148)

x = 128
y = 120
f_montant1 = False
f_montant2 = False
f_montant3 = False
f_montant4 = False
i = 0
j = 0
m = 0

clock = pygame.time.Clock()
screen = pygame.display.set_mode((960, 816))
background = pygame.image.load("fond.png").convert()

class Bloc(pygame.sprite.Sprite):

    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("bloc.png").convert()
        self.rect = self.image.get_rect(topleft=[50, 50])

    def afficher(self):
        screen.blit(self.image, self.rect)

class SpriteSheet(object):

    def __init__(self, file_name, BG):
        self.BG = BG
        self.sprite_sheet = pygame.image.load(file_name).convert()
        self.sprite_sheet.set_colorkey(self.BG)
        self.i = 0
        self.list_images = []

    def get_image(self, x, y, width, height):
        return self.sprite_sheet.subsurface(pygame.Rect(x, y, width, height))

    def get_all_images(self, largeur, hauteur, marge, nbr):
        while self.i < nbr:
            self.list_images.append(self.sprite_sheet.subsurface(pygame.Rect(largeur * self.i + marge * (self.i), 0, largeur, hauteur)))
            self.i += 1
        self.i = 1
        return self.list_images

    def get_all_images_flip(self, largeur, hauteur, marge, nbr):
        while self.i < nbr:
            self.list_images.append(pygame.transform.flip(self.sprite_sheet.subsurface(pygame.Rect(largeur * self.i + marge * (self.i), 0, largeur, hauteur)), True, False))
            self.list_images = list(reversed(self.list_images))
            self.i += 1
        self.i = 1
        return self.list_images

class Bomberman(pygame.sprite.Sprite):

    def __init__(self, touches=[pygame.K_LEFT, pygame.K_RIGHT, pygame.K_UP, pygame.K_DOWN, pygame.K_KP1], sprites="1"):
        super().__init__()
        self.touches = touches
        self.sprites = sprites + "/"
        self.droite = pygame.image.load(self.sprites+"droite.png").convert()
        self.dos = pygame.image.load(self.sprites+"dos.png").convert()
        self.face = pygame.image.load(self.sprites+"face.png").convert()
        self.gauche = pygame.image.load(self.sprites+"gauche.png").convert()
        self.rect = pygame.Rect(0, 0, 64, 64)
        self.droite.set_colorkey(BG_SPRITES)
        self.dos.set_colorkey(BG_SPRITES)
        self.face.set_colorkey(BG_SPRITES)
        self.gauche.set_colorkey(BG_SPRITES)
        self.pos = [64, 56]
        self.vitesse_x = 0
        self.vitesse_y = 0
        self.direction = "face"
        self.moving = False
        self.attacking = False

        #self.face = pygame.transform.scale(self.face, (28, 48))

        self.frame = 0
        self.v_frame = 0
        self.animation_b = []
        self.animation_h = []
        self.animation_d = []
        self.animation_g = []

        sprite_sheet = SpriteSheet(self.sprites+"anim_face.png", BG_SPRITES)
        self.animation_b = sprite_sheet.get_all_images(42, 72, 15, 8)
        sprite_sheet = SpriteSheet(self.sprites+"anim_dos.png", BG_SPRITES)
        self.animation_h = sprite_sheet.get_all_images(42, 72, 15, 8)
        sprite_sheet = SpriteSheet(self.sprites+"anim_droite.png", BG_SPRITES)
        self.animation_d = sprite_sheet.get_all_images(48, 72, 15, 8)
        sprite_sheet = SpriteSheet(self.sprites+"anim_gauche.png", BG_SPRITES)
        self.animation_g = sprite_sheet.get_all_images(48, 72, 15, 8)

        """image = sprite_sheet.get_image(0, 0, 14, 24)
        self.animation_b.append(image)
        image = sprite_sheet.get_image(23, 0, 14, 24)
        self.animation_b.append(image)
        image = sprite_sheet.get_image(46, 0, 14, 24)
        self.animation_b.append(image)
        image = sprite_sheet.get_image(70, 0, 14, 24)
        self.animation_b.append(image)
        image = sprite_sheet.get_image(90, 0, 14, 24)
        self.animation_b.append(image)
        image = sprite_sheet.get_image(110, 0, 14, 24)
        self.animation_b.append(image)"""

    def afficher(self):
        if self.direction == "face" and self.vitesse_y != 0:
            if self.frame >= len(self.animation_b):
                self.frame = 0
            screen.blit(self.animation_b[self.frame], [self.pos[0]+11, self.pos[1]-8])
            self.v_frame += 1
            if self.v_frame > 3:
                self.frame += 1
                self.v_frame = 0
        elif self.direction == "face" and self.vitesse_y == 0:
            screen.blit(self.face, [self.pos[0]+11, self.pos[1]-8])
        elif self.direction == "dos" and self.vitesse_y != 0:
            if self.frame >= len(self.animation_h):
                self.frame = 0
            screen.blit(self.animation_h[self.frame], [self.pos[0]+11, self.pos[1]-8])
            self.v_frame += 1
            if self.v_frame > 3:
                self.frame += 1
                self.v_frame = 0
        elif self.direction == "dos"and self.vitesse_y == 0:
            screen.blit(self.dos, [self.pos[0]+11, self.pos[1]-8])
        elif self.direction == "gauche" and self.vitesse_x != 0:
            if self.frame >= len(self.animation_g):
                self.frame = 0
            screen.blit(self.animation_g[self.frame], [self.pos[0]+11, self.pos[1]-8])
            self.v_frame += 1
            if self.v_frame > 3:
                self.frame += 1
                self.v_frame = 0
        elif self.direction == "gauche" and self.vitesse_x ==0:
            screen.blit(self.gauche, [self.pos[0]+11, self.pos[1]-8])
        elif self.direction == "droite" and self.vitesse_x !=0:
            if self.frame >= len(self.animation_d):
                self.frame = 0
            screen.blit(self.animation_d[self.frame], [self.pos[0]+11, self.pos[1]-8])
            self.v_frame += 1
            if self.v_frame > 3:
                self.frame += 1
                self.v_frame = 0
        elif self.direction == "droite" and self.vitesse_x == 0:
            screen.blit(self.droite, [self.pos[0]+11, self.pos[1]-8])

    def mouvement(self):
        self.pos[0] += self.vitesse_x
        self.pos[1] += self.vitesse_y
        self.rect.topleft = [self.pos[0], self.pos[1]]

class Slash(pygame.sprite.Sprite):

    def __init__(self):
        super().__init__()
        self.animation = []
        sprite_sheet = SpriteSheet("slash.png", [64, 128, 0])
        self.animation = sprite_sheet.get_all_images(64, 64, 0, 3)
        self.rect = pygame.Rect(128, 128, 64, 64)
        self.frame = 0
        self.v_frame = 0

    def afficher(self):
        if self.frame >= len(self.animation):
            self.frame = 0
        screen.blit(self.animation[self.frame], self.rect)
        self.v_frame += 1
        if self.v_frame > 2:
            self.frame += 1
            self.v_frame = 0

joueur1 = Bomberman()
slash = Slash()
#joueur2 = Bomberman([pygame.K_a, pygame.K_d, pygame.K_w, pygame.K_s], "2")

blocs = []
k = 0
while k <= 29:
    blocs.append(Bloc())
    k += 1

list_bloc = pygame.sprite.Group()

for bloc in blocs:
    list_bloc.add(bloc)

#collide = pygame.sprite.collide_rect_ratio(0.2)

while not done:
    # --- Main event loop
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True

    touches = pygame.key.get_pressed()

    joueur1.vitesse_x = 0
    joueur1.vitesse_y = 0

    #joueur2.vitesse_x = 0

    if not joueur1.moving and not joueur1.attacking:
        if touches[joueur1.touches[0]] and joueur1.direction == "gauche" and not f_montant1:
            joueur1.moving = True
        if touches[joueur1.touches[0]] and not pygame.sprite.spritecollide(joueur1, list_bloc, False):
            joueur1.direction = "gauche"
            f_montant1 = True
        if not touches[joueur1.touches[0]]:
            f_montant1 = False

        if touches[joueur1.touches[1]] and joueur1.direction == "droite" and not f_montant2:
            joueur1.moving = True
        if touches[joueur1.touches[1]] and not pygame.sprite.spritecollide(joueur1, list_bloc, False):
            joueur1.direction = "droite"
            f_montant2 = True
        if not touches[joueur1.touches[1]]:
            f_montant2 = False

        if touches[joueur1.touches[2]] and joueur1.direction == "dos" and not f_montant3:
            joueur1.moving = True
        if touches[joueur1.touches[2]] and not pygame.sprite.spritecollide(joueur1, list_bloc, False):
            joueur1.direction = "dos"
            f_montant3 = True
        if not touches[joueur1.touches[2]]:
            f_montant3 = False

        if touches[joueur1.touches[3]] and joueur1.direction == "face" and f_montant4 == False:
            joueur1.moving = True
        if touches[joueur1.touches[3]] and not pygame.sprite.spritecollide(joueur1, list_bloc, False):
            joueur1.direction = "face"
            f_montant4 = True
        if not touches[joueur1.touches[3]]:
            f_montant4 = False

        if touches[joueur1.touches[4]]:
            joueur1.attacking = True

    """if touches[joueur2.touches[0]] and not pygame.sprite.spritecollide(joueur2, list_bloc, False):
        joueur2.direction = "gauche"
        joueur2.vitesse_x = -1
        joueur2.vitesse_y = 0
    elif touches[joueur2.touches[1]] and not pygame.sprite.spritecollide(joueur2, list_bloc, False):
        joueur2.direction = "droite"
        joueur2.vitesse_x = 1
        joueur2.vitesse_y = 0
    elif touches[joueur2.touches[2]] and not pygame.sprite.spritecollide(joueur2, list_bloc, False):
        joueur2.direction = "dos"
        joueur2.vitesse_y = -1
        joueur2.vitesse_x = 0
    elif touches[joueur2.touches[3]] and not pygame.sprite.spritecollide(joueur2, list_bloc, False):
        joueur2.direction = "face"
        joueur2.vitesse_y = 1
        joueur2.vitesse_x = 0"""

    # --- Game logic

    u = 0
    for t in range(5):
        while i <= 5:
            blocs[u].rect.topleft = [x + (128*i), y + (128 * t)]
            i += 1
            u += 1
        i = 0

    if joueur1.moving:
        if joueur1.direction == "droite" and j < 17:
            joueur1.vitesse_x = 4
            j += 1
        if j >= 17:
            j = 0
            joueur1.moving = False
            joueur1.vitesse_x = 0

        if joueur1.direction == "gauche" and j < 17:
            joueur1.vitesse_x = -4
            j += 1
        if j >= 17:
            j = 0
            joueur1.moving = False
            joueur1.vitesse_x = 0

        if joueur1.direction == "face" and j < 17:
            joueur1.vitesse_y = 4
            j += 1
        if j >= 17:
            j = 0
            joueur1.moving = False
            joueur1.vitesse_y = 0

        if joueur1.direction == "dos" and j < 17:
            joueur1.vitesse_y = -4
            j += 1
        if j >= 17:
            j = 0
            joueur1.moving = False
            joueur1.vitesse_y = 0

    clock.tick(60)

    # --- Drawing code
    screen.fill(BLACK)

    screen.blit(background, (0, 0))

    for bloc in blocs:
        bloc.afficher()

    joueur1.mouvement()
    joueur1.afficher()
    print(joueur1.rect)

    if joueur1.attacking:
        if joueur1.direction == "droite":
            slash.rect = (joueur1.pos[0]+64, joueur1.pos[1])
        if joueur1.direction == "gauche":
            slash.rect = (joueur1.pos[0]-64, joueur1.pos[1])
        if joueur1.direction == "dos":
            slash.rect = (joueur1.pos[0], joueur1.pos[1]-64)
        if joueur1.direction == "face":
            slash.rect = (joueur1.pos[0], joueur1.pos[1]+64)

        if m < 9:
            slash.afficher()
            m += 1
        else:
            m = 0
            joueur1.attacking = False

    #print(joueur1.attacking)
    #print(m)

    #joueur2.mouvement()
    #joueur2.afficher()
    pygame.display.flip()

    clock.tick(60)

pygame.quit()
