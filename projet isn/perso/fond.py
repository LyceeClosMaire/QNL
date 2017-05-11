import pygame

done = False

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BG_SPRITES = (33, 57, 148)

x = 128
y = 120
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
        self.rect = self.image.get_rect(topleft=[0, 0])

    def afficher(self):
        screen.blit(self.image, self.rect)



class Blocdestru(pygame.sprite.Sprite):

    def __init__(self):
        super().__init__()
        self.image_solide = pygame.image.load("bloc_destructible.png").convert()
        self.image_casse = pygame.image.load("bloc_casse.png").convert()
        self.rect = self.image_solide.get_rect(topleft=[0, 0])
        self.etat = "solide"


    def afficher(self):
        if self.etat == "solide":
            screen.blit(self.image_solide, self.rect)

        elif self.etat == "casse":
            screen.blit(self.image_casse, self.rect)





class SpriteSheet(object):

    def __init__(self, file_name, bg):
        self.bg = bg
        self.sprite_sheet = pygame.image.load(file_name).convert()
        self.sprite_sheet.set_colorkey(self.bg)
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

    def __init__(self, touches=[pygame.K_LEFT, pygame.K_RIGHT, pygame.K_UP, pygame.K_DOWN, pygame.K_KP1], sprites="1", slash=None):
        super().__init__()
        self.i =0
        self.j = 0
        self.last_direction = "face"
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
        self.slash = slash

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
        elif self.direction == "gauche" and self.vitesse_x == 0:
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

    def move(self):
        if self.direction == "droite" and self.j < 17:
            self.vitesse_x = 4
            self.j += 1
        if self.j >= 17:
            self.j = 0
            self.moving = False
            self.vitesse_x = 0

        if self.direction == "gauche" and self.j < 17:
            self.vitesse_x = -4
            self.j += 1
        if self.j >= 17:
            self.j = 0
            self.moving = False
            self.vitesse_x = 0

        if self.direction == "face" and self.j < 17:
            self.vitesse_y = 4
            self.j += 1
        if self.j >= 17:
            self.j = 0
            self.moving = False
            self.vitesse_y = 0

        if self.direction == "dos" and self.j < 17:
            self.vitesse_y = -4
            self.j += 1
        if self.j >= 17:
            self.j = 0
            self.moving = False
            self.vitesse_y = 0

        self.pos[0] += self.vitesse_x
        self.pos[1] += self.vitesse_y
        self.rect.topleft = [self.pos[0], self.pos[1]]

    def attack(self):
        if self.direction == "droite":
            self.slash.rect.topleft = (self.pos[0]+64, self.pos[1])
        if self.direction == "gauche":
            self.slash.rect.topleft = (self.pos[0]-64, self.pos[1])
        if self.direction == "dos":
            self.slash.rect.topleft = (self.pos[0], self.pos[1]-64)
        if self.direction == "face":
            self.slash.rect.topleft = (self.pos[0], self.pos[1]+64)

    def update(self, pressed_keys=None):
        if pressed_keys[self.touches[0]]:
            if self.direction == "gauche" and self.direction == self.last_direction:
                self.moving = True
            else:
                self.direction = "gauche"
        if pressed_keys[self.touches[1]]:
            if self.direction == "droite" and self.direction == self.last_direction:
                self.moving = True
            else:
                self.direction = "droite"
        if pressed_keys[self.touches[2]]:
            if self.direction == "dos" and self.direction == self.last_direction:
                self.moving = True
            else:
                self.direction = "dos"
        if pressed_keys[self.touches[3]]:
            if self.direction == "face" and self.direction == self.last_direction:
                self.moving = True
            else:
                self.direction = "face"
        if pressed_keys[self.touches[4]]:
            self.attacking = True

        if self.direction == "gauche" and not pressed_keys[self.touches[0]]:
            self.last_direction = "gauche"
        if self.direction == "droite" and not pressed_keys[self.touches[1]]:
            self.last_direction = "droite"
        if self.direction == "dos" and not pressed_keys[self.touches[2]]:
            self.last_direction = "dos"
        if self.direction == "face" and not pressed_keys[self.touches[3]]:
            self.last_direction = "face"

    def afficher_slash(self):
        if self.i < 9:
            self.slash.afficher()
            self.i += 1
        else:
            self.i = 0
            self.slash.rect.topleft = (-128, -128)
            self.attacking = False


class Slash(pygame.sprite.Sprite):

    def __init__(self):
        super().__init__()
        self.animation = []
        sprite_sheet = SpriteSheet("slash.png", [64, 128, 0])
        self.animation = sprite_sheet.get_all_images(64, 64, 0, 3)
        self.rect = pygame.Rect(128, 128, 64, 64)
        self.frame = 0
        self.v_frame = 0
        self.in_cd = False
        self.cd = 0

    def afficher(self):
        if self.frame >= len(self.animation):
            self.frame = 0
        screen.blit(self.animation[self.frame], self.rect)
        self.v_frame += 1
        if self.v_frame > 2:
            self.frame += 1
            self.v_frame = 0

slash1 = Slash()
slash1.rect.topleft = (-128, -128)
joueur1 = Bomberman(slash=slash1)

slash2 = Slash()
slash2.rect.topleft = (1088, -128)
joueur2 = Bomberman([pygame.K_a, pygame.K_d, pygame.K_w, pygame.K_s, pygame.K_t], "2", slash2)

blocs = []
blocs_destru = []

k = 0
while k < 30:
    blocs.append(Bloc())
    k += 1

k = 0
while k < 71:
    blocs_destru.append(Blocdestru())
    k += 1

u = 0
for t in range(5):
    while i < 6:
        blocs[u].rect.topleft = [x + (128*i), y + (128 * t)]
        i += 1
        u += 1
    i = 0

u = 0
x = 128
y = 56
for t in range(6):
    while i < 6:
        blocs_destru[u].rect.topleft = [x + (128*i), y + (128 * t)]
        i += 1
        u += 1
    i = 0

x = 64
y = 120
for t in range(5):
    while i < 7:
        blocs_destru[u].rect.topleft = [x + (128*i), y + (128 * t)]
        i += 1
        u += 1
        print(u, i)
    i = 0

list_bloc = pygame.sprite.Group()
list_blocdestru = pygame.sprite.Group()

for bloc in blocs:
    list_bloc.add(bloc)

for bloc in blocs_destru:
    list_blocdestru.add(bloc)

while not done:
    # --- Main event loop
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True

    joueur1.vitesse_x = 0
    joueur1.vitesse_y = 0

    joueur2.vitesse_x = 0
    joueur2.vitesse_y = 0

    # --- Game logic

    touches = pygame.key.get_pressed()

    if not joueur1.moving and not joueur1.attacking:
        joueur1.update(touches)

    if not joueur2.moving and not joueur2.attacking:
        joueur2.update(touches)

    if joueur1.moving:
        joueur1.move()

    if joueur2.moving:
        joueur2.move()

    if joueur1.attacking and not joueur1.moving and not joueur1.slash.in_cd:
        joueur1.attack()
        joueur1.slash.in_cd = True

    if joueur2.attacking and not joueur2.moving:
        joueur2.attack()

    if joueur1.slash.in_cd:
        if joueur1.slash.cd < 30:
            joueur1.slash.cd += 1
        else:
            joueur1.slash.cd = 0
            joueur1.slash.in_cd = False

    if joueur2.slash.in_cd:
        if joueur2.slash.cd < 30:
            joueur2.slash.cd += 1
        else:
            joueur2.slash.cd = 0
            joueur2.slash.in_cd = False


    if pygame.sprite.spritecollide(joueur1, list_bloc, False):
        if joueur1.direction == "droite":
            joueur1.pos[0] -= joueur1.vitesse_x
        elif joueur1.direction == "gauche":
            joueur1.pos[0] -= joueur1.vitesse_x
        elif joueur1.direction == "dos":
            joueur1.pos[1] -= joueur1.vitesse_y
        elif joueur1.direction == "face":
            joueur1.pos[1] -= joueur1.vitesse_y

    collision = pygame.sprite.spritecollide(joueur1.slash, list_blocdestru, False)
    print(collision)

    if len(collision) > 0:
            if collision[0].etat == "solide":
                if joueur1.direction == "droite":
                    joueur1.pos[0] -= joueur1.vitesse_x
                elif joueur1.direction == "gauche":
                    joueur1.pos[0] -= joueur1.vitesse_x
                elif joueur1.direction == "dos":
                    joueur1.pos[1] -= joueur1.vitesse_y
                elif joueur1.direction == "face":
                    joueur1.pos[1] -= joueur1.vitesse_y
            elif collision[0].etat == "casse":
                print()

    if pygame.sprite.spritecollide(joueur2, list_bloc, False):
        if joueur2.direction == "droite":
            joueur2.pos[0] -= joueur2.vitesse_x
        elif joueur2.direction == "gauche":
            joueur2.pos[0] -= joueur2.vitesse_x
        elif joueur2.direction == "dos":
            joueur2.pos[1] -= joueur2.vitesse_y
        elif joueur2.direction == "face":
            joueur2.pos[1] -= joueur2.vitesse_y

    if joueur1.pos[0] < 64:
        joueur1.pos[0] -= joueur1.vitesse_x

    if joueur1.pos[0] > 832:
        joueur1.pos[0] -= joueur1.vitesse_x

    if joueur1.pos[1] < 56:
        joueur1.pos[1] -= joueur1.vitesse_y

    if joueur1.pos[1] > 696:
        joueur1.pos[1] -= joueur1.vitesse_y

    if joueur2.pos[0] < 64:
        joueur2.pos[0] -= joueur2.vitesse_x

    if joueur2.pos[0] > 832:
        joueur2.pos[0] -= joueur2.vitesse_x

    if joueur2.pos[1] < 56:
        joueur2.pos[1] -= joueur2.vitesse_y

    if joueur2.pos[1] > 696:
        joueur2.pos[1] -= joueur2.vitesse_y


    # --- Drawing code
    screen.fill(BLACK)

    screen.blit(background, (0, 0))

    for bloc in blocs:
        bloc.afficher()

    for bloc in blocs_destru:
        bloc.afficher()

    if joueur1.pos[1] < joueur2.pos[1]:
        joueur1.afficher()
        joueur2.afficher()
    elif joueur2.pos[1] < joueur1.pos[1]:
        joueur2.afficher()
        joueur1.afficher()
    else:
        joueur2.afficher()
        joueur1.afficher()

    joueur1.afficher_slash()
    joueur2.afficher_slash()

    pygame.display.flip()

    clock.tick(30)

pygame.quit()
