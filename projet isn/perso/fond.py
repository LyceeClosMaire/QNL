import pygame

# variable qui définie si le jeu doit continure de tourner ou non
done = False

# couleurs en rgb
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BG_SPRITES = (33, 57, 148)

# variables de position et compteurs
x = 128
y = 120
i = 0
j = 0
m = 0

# création de Clock de Display et d'un fond
clock = pygame.time.Clock()
screen = pygame.display.set_mode((960, 816))
background = pygame.image.load("fond.png").convert()


class Bloc(pygame.sprite.Sprite):
    # classe des blocs indestuctibles

    def __init__(self):
        # fonction d'initialisation

        # utilisation de pygame.sprite
        super().__init__()
        # création image
        self.image = pygame.image.load("bloc.png").convert()
        # création Rect
        self.rect = self.image.get_rect(topleft=[0, 0])

    def afficher(self):
        #fonction d'affichage

        # on affiche l'image en fonction du Rect
        screen.blit(self.image, self.rect)


class Blocdestru(pygame.sprite.Sprite):
    # classe des blocs destructibles

    def __init__(self, attention):
        # fonction d'initialisation

        # utilisation de pygame.sprite
        super().__init__()
        # création des images
        self.image_solide = pygame.image.load("bloc_destructible.png").convert()
        self.image_casse = pygame.image.load("bloc_casse.png").convert()
        # création rect
        self.rect = self.image_solide.get_rect(topleft=[0, 0])
        # création d'un timer pour la réaparition du bloc
        self.timer = 0
        # création d'un variable représentant l'état du bloc
        self.etat = "solide"
        # récupération de l'objet Attention
        self.attention = attention


    def afficher(self):
        # fonction d'affichage du bloc

        # si le bloc est solide
        if self.etat == "solide":
            # on affiche l'image de bloc solide en fonction du Rect
            screen.blit(self.image_solide, self.rect)

        # si il est cassé
        elif self.etat == "casse":
            # on affiche l'image de bloc cassé en fonction du Rect
            screen.blit(self.image_casse, self.rect)

    def afficher_attention(self):
        # fonction d'affichage de l'objet attention

        # le Rect de attention est mit au même endroit que celui du bloc
        self.attention.rect.center = self.rect.center
        # et on l'affiche
        self.attention.afficher()


class Attention(pygame.sprite.Sprite):
    #classe du panneau attention

    def __init__(self):
        # fonction d'initialisation

        # utilisation de pygame.sprite
        super().__init__()
        # création d'une image
        self.image = pygame.image.load("attention.png").convert()
        # dont on transforme une certaine couleur en transparent
        self.image.set_colorkey(BG_SPRITES)
        # création d'un Rect
        self.rect = self.image.get_rect(topleft=[0, 0])

    def afficher(self):
        # fonction d'affichage du panneau

        # on affiche l'image en fonction du Rect
        screen.blit(self.image, self.rect)


class SpriteSheet(object):

    def __init__(self, file_name, bg):
        # fonction d'initialisation

        # on récupère la couleur du fond dont on veux se débarrasser
        self.bg = bg
        # création d'une image
        self.sprite_sheet = pygame.image.load(file_name).convert()
        # on enlève la couleur non voulue
        self.sprite_sheet.set_colorkey(self.bg)
        # création d'un compteur
        self.i = 0
        # création d'une liste vide qui contiendra les images d'une animation
        self.list_images = []

    def get_all_images(self, largeur, hauteur, marge, nbr):
        # fonction qui récupère toutes les images d'une animation en fonction de plusieurs paramètres

        # on le fait autant de fois qu'il y a d'images
        while self.i < nbr:
            # on récupère une image qu'on ajoute à la liste
            self.list_images.append(self.sprite_sheet.subsurface(pygame.Rect(largeur * self.i + marge * (self.i), 0, largeur, hauteur)))
            # on incrémente le compteur
            self.i += 1
        # quand on a finis on le remet à 1
        self.i = 1
        # et on renvoie la liste d'images
        return self.list_images

class Bomberman(pygame.sprite.Sprite):

    def __init__(self, touches=[pygame.K_LEFT, pygame.K_RIGHT, pygame.K_UP, pygame.K_DOWN, pygame.K_KP1], sprites="1", slash=None):
        # fonction d'initialisation

        # utilisation de pygame.sprite
        super().__init__()
        # création de compteurs
        self.i =0
        self.j = 0
        # variables de la dernière direction du personnage
        self.last_direction = "face"
        # on récupères les touches enfoncées dans une variable
        self.touches = touches
        # on récupère le chemin du dossier des sprites
        self.sprites = sprites + "/"
        # création des images
        self.droite = pygame.image.load(self.sprites+"droite.png").convert()
        self.dos = pygame.image.load(self.sprites+"dos.png").convert()
        self.face = pygame.image.load(self.sprites+"face.png").convert()
        self.gauche = pygame.image.load(self.sprites+"gauche.png").convert()
        # création d'un Rect
        self.rect = pygame.Rect(0, 0, 64, 64)
        # on enlève la couleur non voulue des images
        self.droite.set_colorkey(BG_SPRITES)
        self.dos.set_colorkey(BG_SPRITES)
        self.face.set_colorkey(BG_SPRITES)
        self.gauche.set_colorkey(BG_SPRITES)
        # variable de position du personnage
        self.pos = [64, 56]
        # variables de vitesse du personnage
        self.vitesse_x = 0
        self.vitesse_y = 0
        # variable de direction du personnage
        self.direction = "face"
        # booléens pour savoir si le personnage est en train de bouger, d'attaquer, de se faire pousser ou est mort
        self.moving = False
        self.attacking = False
        self.dead = False
        self.knockback = False
        # récupération de l'objet Slash associé au joueur
        self.slash = slash
        # booléen pour ne faire reculer l'autre personnage qu'un fois
        self.knockback_f_montant = False

        # création de variables et de listes pour l'animation du personnages
        self.frame = 0
        self.v_frame = 0
        self.animation_b = []
        self.animation_h = []
        self.animation_d = []
        self.animation_g = []

        # on récupère les animations
        sprite_sheet = SpriteSheet(self.sprites+"anim_face.png", BG_SPRITES)
        self.animation_b = sprite_sheet.get_all_images(42, 72, 15, 8)
        sprite_sheet = SpriteSheet(self.sprites+"anim_dos.png", BG_SPRITES)
        self.animation_h = sprite_sheet.get_all_images(42, 72, 15, 8)
        sprite_sheet = SpriteSheet(self.sprites+"anim_droite.png", BG_SPRITES)
        self.animation_d = sprite_sheet.get_all_images(48, 72, 15, 8)
        sprite_sheet = SpriteSheet(self.sprites+"anim_gauche.png", BG_SPRITES)
        self.animation_g = sprite_sheet.get_all_images(48, 72, 15, 8)


    def afficher(self):
        # fonction d'affichage du personnage

        # si le joueur est de face et qu'il bouge verticallement
        if self.direction == "face" and self.vitesse_y != 0:
            # si on a va dépasser la dernière image de l'animation
            if self.frame >= len(self.animation_b):
                # on retourne à la première
                self.frame = 0
            # on affiche l'image au centre du rect
            screen.blit(self.animation_b[self.frame], [self.pos[0]+11, self.pos[1]-8])
            # on incrémnte le compteur
            self.v_frame += 1
            # si on a afficher 3 fois de suite la même image
            if self.v_frame > 3:
                #on passe à la suivante
                self.frame += 1
                #et on remet le compteur à 0
                self.v_frame = 0
        # si le joueur est de face et ne bouge pas verticallement
        elif self.direction == "face" and self.vitesse_y == 0:
            # on affiche l'image fixe au centre du rect
            screen.blit(self.face, [self.pos[0]+11, self.pos[1]-8])
        # même chose pour les autres directions
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
        # fonction pour faire bouger le personnage

        # si le personnage est dirigé vers la droite et que le compteur n'est pas terminé
        if self.direction == "droite" and self.j < 17:
            # on change la vitesse du personnage pendant uen frame
            self.vitesse_x = 4
            # et on incrémente le comteur
            self.j += 1
        # si on a l'a fait sur 17 frames
        if self.j >= 17:
            # on remet le compteur à 0
            self.j = 0
            # et on arrête le personnage
            self.moving = False
            self.vitesse_x = 0

        # même chose pour les autres directions
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

        # enfin on déplace le joueur selon sa vitesse
        self.pos[0] += self.vitesse_x
        self.pos[1] += self.vitesse_y

    def attack(self):
        # fonction pour faire bouger le rect du slash

        # si le personnage regarde vers la droite
        if self.direction == "droite":
            # on change le Rect du slash pour qu'il soit une case à droite du personnage
            self.slash.rect.topleft = (self.pos[0]+64, self.pos[1])

        # même chose pour les autres directions
        if self.direction == "gauche":
            self.slash.rect.topleft = (self.pos[0]-64, self.pos[1])

        if self.direction == "dos":
            self.slash.rect.topleft = (self.pos[0], self.pos[1]-64)

        if self.direction == "face":
            self.slash.rect.topleft = (self.pos[0], self.pos[1]+64)

    def update(self, pressed_keys=None):
        # fonction qui met a jour les touches enfoncées et agit en conséquence

        # si une touche appuyée est celle 0 (gauche)
        if pressed_keys[self.touches[0]]:
            # si le personnage regarde vers la gauche et qu'il la regardait aussi avant
            if self.direction == "gauche" and self.direction == self.last_direction:
                # on l'autorise a bouger
                self.moving = True
            # sinon on le fait regarder la gauche
            else:
                self.direction = "gauche"
        # même chose pour les autres touches de mouvements
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

        # si la touche 4 (attaque) est enfoncée
        if pressed_keys[self.touches[4]]:
            # on autorise le pseronnage à attaquer
            self.attacking = True

        # si le personnage est orienté vers la gauche mais qu'on a appuie pas sur la touche 0 (gauche)
        if self.direction == "gauche" and not pressed_keys[self.touches[0]]:
            # on change la direction du personnage vers la gauche
            self.last_direction = "gauche"

        # même chose pour les autres directions
        if self.direction == "droite" and not pressed_keys[self.touches[1]]:
            self.last_direction = "droite"
        if self.direction == "dos" and not pressed_keys[self.touches[2]]:
            self.last_direction = "dos"
        if self.direction == "face" and not pressed_keys[self.touches[3]]:
            self.last_direction = "face"

    def afficher_slash(self):
        # fonction pour afficher les slash du personnage

        # si le compteur n'est pas terminé
        if self.i < 9:
            # on affiche le slash pendant une frame
            self.slash.afficher()
            # et on incrémente le compteur
            self.i += 1
        # si il l'est
        else:
            # on remet le compteur à 0
            self.i = 0
            # on met le rect du slash hors de l'écran
            self.slash.rect.topleft = (-128, -128)
            # et on arrête d'attaquer
            self.attacking = False


class Slash(pygame.sprite.Sprite):
    # classe du slash (attaque des personnages)

    def __init__(self):
        # fonction d'initialisation

        # utilisation de pygame.sprite
        super().__init__()
        # on crée une liste vide pour les images de l'animation
        self.animation = []
        # on ajoute dedans chaque images de celle ci
        sprite_sheet = SpriteSheet("slash.png", [64, 128, 0])
        self.animation = sprite_sheet.get_all_images(64, 64, 0, 3)
        # on crée un Rect
        self.rect = pygame.Rect(128, 128, 64, 64)
        # on crée compteurs pour afficher l'animation
        self.frame = 0
        self.v_frame = 0
        # variables de cooldown du slash
        self.in_cd = False
        self.cd = 0

    def afficher(self):
        # fonction pour afficher l'animation du slash

        # si on va dépasser la dernière image
        if self.frame >= len(self.animation):
            # on revient à la première
            self.frame = 0
        # on affiche l'image actuelle pendant une frame
        screen.blit(self.animation[self.frame], self.rect)
        # et on incrémente un compteur
        self.v_frame += 1
        #  on passe a l'image suivante seulement quand on a affiché l'image 2 fois d'affilé
        if self.v_frame > 2:
            self.frame += 1
            self.v_frame = 0


# on crée un slash et on change sa position
slash1 = Slash()
slash1.rect.topleft = (-128, -128)
# on crée un premier joueur auquel on associe le slash
joueur1 = Bomberman(slash=slash1)

# même chose pour le joueur 2
slash2 = Slash()
slash2.rect.topleft = (1088, -128)
joueur2 = Bomberman([pygame.K_a, pygame.K_d, pygame.K_w, pygame.K_s, pygame.K_t], "2", slash2)
# on change aussi sa position
joueur2.pos = [832,56]

# on crée des liste vides pour les blocs
blocs = []
blocs_destru = []

# on crée 30 bloc indestructibles
k = 0
while k < 30:
    blocs.append(Bloc())
    k += 1

# on crée 71 blocs destructibles associés à des attentions
k = 0
while k < 71:
    blocs_destru.append(Blocdestru(Attention()))
    k += 1

# on place les blocs indestructibles
u = 0
for t in range(5):
    while i < 6:
        blocs[u].rect.topleft = [x + (128*i), y + (128 * t)]
        i += 1
        u += 1
    i = 0

# et on place les blocs destructibles
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
    i = 0

u = 0

# on crée deux groupes de sprites pour les différents blocs
list_bloc = pygame.sprite.Group()
list_blocdestru = pygame.sprite.Group()

# et on les rajoute dedans
for bloc in blocs:
    list_bloc.add(bloc)

for bloc in blocs_destru:
    list_blocdestru.add(bloc)

# tant que le jeu n'est pas fini
while not done:
    # --- Main event loop
    # pour chaque évènement pygame
    for event in pygame.event.get():
        # si l'on veut quitter
        if event.type == pygame.QUIT:
            # on change la valeur de la variable qui entraine l'arrêt du jeu
            done = True

    #on met les rect des 2 joueurs a leurs positions
    joueur1.rect.topleft = [joueur1.pos[0], joueur1.pos[1]]
    joueur2.rect.topleft = [joueur2.pos[0], joueur2.pos[1]]

    # on remet la vitesse des deux joueurs à 0
    joueur1.vitesse_x = 0
    joueur1.vitesse_y = 0

    joueur2.vitesse_x = 0
    joueur2.vitesse_y = 0

    # --- Game logic

    # on récupère les touches enfoncées
    touches = pygame.key.get_pressed()

    # si le joueur 1 n'est pas mort
    if not joueur1.dead:
        # si il ne bouge pas et qu'il n'attaque pas
        if not joueur1.moving and not joueur1.attacking:
            # on met a jour le joueur en fonction des touches
            joueur1.update(touches)

        # si le joueur peut bouger
        if joueur1.moving:
            # on le fait bouger
            joueur1.move()

        # si le joueur attaque qu'il ne bouge pas et que sont slash n'est pas en cooldown
        if joueur1.attacking and not joueur1.moving and not joueur1.slash.in_cd:
            # on le fait attaquer
            joueur1.attack()
            # et on met son slash en cooldown
            joueur1.slash.in_cd = True

        # si le slash du joueur est e ncooldown
        if joueur1.slash.in_cd:
            # si il l'est depuis moins de 30 frames
            if joueur1.slash.cd < 30:
                # on le garde en cooldown pour une autre frame
                joueur1.slash.cd += 1
            # sinon
            else:
                # on remet le compteur de frame à 0
                joueur1.slash.cd = 0
                # et le slash n'est plus en cooldown
                joueur1.slash.in_cd = False

        # on récupère la liste de blocs destructible qui est entré en collision avec le slash du joueur pendant cette frame
        collision = pygame.sprite.spritecollide(joueur1.slash, list_blocdestru, False)
        # si il est rentré en collision un
        if len(collision) > 0:
            # on change son état à cassé
            collision[0].etat = "casse"

        # si le joueur est entré en collision avec un bloc indestructible
        if pygame.sprite.spritecollide(joueur1, list_bloc, False):
            # on le  fait ressortir du bloc
            if joueur1.direction == "droite":
                joueur1.pos[0] -= joueur1.vitesse_x

            # même chose pour les autres directions
            elif joueur1.direction == "gauche":
                joueur1.pos[0] -= joueur1.vitesse_x

            elif joueur1.direction == "dos":
                joueur1.pos[1] -= joueur1.vitesse_y

            elif joueur1.direction == "face":
                joueur1.pos[1] -= joueur1.vitesse_y

        # on récupère la liste de blocs destructible qui est entré en collision avec lejoueur pendant cette frame
        collision = pygame.sprite.spritecollide(joueur1, list_blocdestru, False)
        # si il est rentré dans un bloc
        if len(collision) > 0:
            # et si ce bloc est solide
            if collision[0].etat == "solide":
                # on le fait ressortir du bloc (2 * la vitesse car sinon le joueur clip dans le bloc et reste bloqué)
                if joueur1.direction == "droite":
                    joueur1.pos[0] -= 2*joueur1.vitesse_x

                # même chose pour les autres directions
                elif joueur1.direction == "gauche":
                    joueur1.pos[0] -= 2*joueur1.vitesse_x

                elif joueur1.direction == "dos":
                    joueur1.pos[1] -= 2*joueur1.vitesse_y

                elif joueur1.direction == "face":
                    joueur1.pos[1] -= 2*joueur1.vitesse_y

        # si le joueur est renté dans le mur de gauche
        if joueur1.pos[0] < 64:
            # on le fait ressortir
            joueur1.pos[0] -= joueur1.vitesse_x

        if joueur1.pos[0] > 832:
            joueur1.pos[0] -= joueur1.vitesse_x

        if joueur1.pos[1] < 56:
            joueur1.pos[1] -= joueur1.vitesse_y

        if joueur1.pos[1] > 696:
            joueur1.pos[1] -= joueur1.vitesse_y

        # si le joueur s'est fait pousser
        if joueur1.knockback:
            # si le joueur 2 regardais vers la droite lorsqu'il a touché le joueur 1
            if joueur2.direction == "droite":
                # on le fait reculer vers la droite
                joueur1.pos[0] += 64
            if joueur2.direction == "gauche":
                joueur1.pos[0] -= 64
            if joueur2.direction == "dos":
                joueur1.pos[1] -= 64
            if joueur2.direction == "face":
                joueur1.pos[1] += 64
            # puis on arrête de le pousser
            joueur1.knockback = False

        # sil le joueur 1 tape le joueur 2 et que c'est lors de la première frame qu'il l'a touché
        if pygame.sprite.collide_rect(joueur1.slash, joueur2) and not joueur1.knockback_f_montant:
            # on pousse le joueur 2
            joueur2.knockback = True
            # et on empêche que le slash repousse le joueur 2 sur toute la longueur de son animaton
            joueur1.knockback_f_montant = True

    # même chose pour le joueur 2
    if not joueur2.dead:

        if not joueur2.moving and not joueur2.attacking:
            joueur2.update(touches)

        if joueur2.moving:
            joueur2.move()

        if joueur2.attacking and not joueur2.moving:
            joueur2.attack()

        if joueur2.slash.in_cd:
            if joueur2.slash.cd < 30:
                joueur2.slash.cd += 1
            else:
                joueur2.slash.cd = 0
                joueur2.slash.in_cd = False

        if pygame.sprite.spritecollide(joueur2, list_bloc, False):
            if joueur2.direction == "droite":
                joueur2.pos[0] -= joueur2.vitesse_x
            elif joueur2.direction == "gauche":
                joueur2.pos[0] -= joueur2.vitesse_x
            elif joueur2.direction == "dos":
                joueur2.pos[1] -= joueur2.vitesse_y
            elif joueur2.direction == "face":
                joueur2.pos[1] -= joueur2.vitesse_y

        collision = pygame.sprite.spritecollide(joueur2.slash, list_blocdestru, False)
        if len(collision) > 0:
            collision[0].etat = "casse"

        collision = pygame.sprite.spritecollide(joueur2, list_blocdestru, False)
        if len(collision) > 0:
                if collision[0].etat == "solide":
                    if joueur2.direction == "droite":
                        joueur2.pos[0] -= 2*joueur2.vitesse_x
                    elif joueur2.direction == "gauche":
                        joueur2.pos[0] -= 2*joueur2.vitesse_x
                    elif joueur2.direction == "dos":
                        joueur2.pos[1] -= 2*joueur2.vitesse_y
                    elif joueur2.direction == "face":
                        joueur2.pos[1] -= 2*joueur2.vitesse_y

        if joueur2.pos[0] < 64:
            joueur2.pos[0] -= joueur2.vitesse_x

        if joueur2.pos[0] > 832:
            joueur2.pos[0] -= joueur2.vitesse_x

        if joueur2.pos[1] < 56:
            joueur2.pos[1] -= joueur2.vitesse_y

        if joueur2.pos[1] > 696:
            joueur2.pos[1] -= joueur2.vitesse_y

        if joueur2.knockback == True:
            if joueur1.direction == "droite":
                joueur2.pos[0] += 64
            if joueur1.direction == "gauche":
                joueur2.pos[0] -= 64
            if joueur1.direction == "dos":
                joueur2.pos[1] -= 64
            if joueur1.direction == "face":
                joueur2.pos[1] += 64
            joueur2.knockback = False

        if pygame.sprite.collide_rect(joueur2.slash, joueur1) and not joueur2.knockback_f_montant:
            joueur1.knockback = True
            joueur2.knockback_f_montant = True

    # si les deux joueur se rentrent dedans
    if pygame.sprite.collide_rect(joueur1, joueur2):
        # si le joueur 1 regarde à droite
        if joueur1.direction == "droite":
            # on le fait ressortir du joueur 2
            joueur1.pos[0] -= joueur1.vitesse_x
        # même chose pour les autres directions
        elif joueur1.direction == "gauche":
            joueur1.pos[0] -= joueur1.vitesse_x
        elif joueur1.direction == "dos":
            joueur1.pos[1] -= joueur1.vitesse_y
        elif joueur1.direction == "face":
            joueur1.pos[1] -= joueur1.vitesse_y

        # même chose pour le joueur 2
        if joueur2.direction == "droite":
            joueur2.pos[0] -= joueur2.vitesse_x
        elif joueur2.direction == "gauche":
            joueur2.pos[0] -= joueur2.vitesse_x
        elif joueur2.direction == "dos":
            joueur2.pos[1] -= joueur2.vitesse_y
        elif joueur2.direction == "face":
            joueur2.pos[1] -= joueur2.vitesse_y

    # pour chaque bloc destructible
    for bloc in blocs_destru:
        # si le bloc est cassé
        if bloc.etat == "casse":
            # on incrémente le timer
            bloc.timer += 1

        # si le bloc est cassé depuis 240 frames
        if bloc.timer > 240:
            # on remet le time à 0
            bloc.timer = 0
            # et on remet le bloc à l'état solide
            bloc.etat = "solide"

        # si le bloc est solide et que le joueur 1 est dans le bloc
        if bloc.etat == "solide" and pygame.sprite.collide_rect(joueur1, bloc) and not joueur1.moving:
            # le joueur 1 meurt
            joueur1.dead = True

        # mêm chose pour le joueur 2
        if bloc.etat == "solide" and pygame.sprite.collide_rect(joueur2, bloc) and not joueur2.moving:
            joueur2.dead = True

    # si on a touché le joueur 2
    if joueur1.knockback_f_montant == True:
        # on empêche de le faire reculer pendant toute l'animation en gardant le variable à True pendant 9 frames
        if i < 9:
            i += 1
        # si on l'a fait on peut repousser le joueur 2
        else:
            i = 0
            joueur1.knockback_f_montant = False

    # même chose pour le joueur 2
    if joueur2.knockback_f_montant == True:
        if u < 9:
            u += 1
        else:
            u = 0
            joueur2.knockback_f_montant = False

    # --- Drawing code
    # on remplit l'écran de noir
    screen.fill(BLACK)

    # on affiche le fond
    screen.blit(background, (0, 0))

    # on affiche chaque bloc indestructible
    for bloc in blocs:
        bloc.afficher()

    # on affiche chaque bloc destructible
    for bloc in blocs_destru:
        bloc.afficher()

    # selon leurs positionset si ils sont mort ou non, on affiche un joueur devant l'autre
    if joueur1.pos[1] < joueur2.pos[1]:
        if not joueur1.dead:
            joueur1.afficher()
        if not joueur2.dead:
            joueur2.afficher()
    elif joueur2.pos[1] < joueur1.pos[1]:
        if not joueur2.dead:
            joueur2.afficher()
        if not joueur1.dead:
            joueur1.afficher()
    else:
        if not joueur2.dead:
            joueur2.afficher()
        if not joueur1.dead:
            joueur1.afficher()

    # si ils sont mort ou non on affiche les slashs des joueurs
    if not joueur1.dead:
        joueur1.afficher_slash()
    if not joueur1.dead:
        joueur2.afficher_slash()

    # on affiche chaque panneau attention (en dernier pour que ce soit par dessus tout les reste)
    for bloc in blocs_destru:
        if bloc.timer > 210:
            bloc.afficher_attention()

    # on affiche tous nos sprites
    pygame.display.flip()

    # on fait en sorte qu'on est 30 frames par seconde
    clock.tick(30)
    print(joueur1.dead)
# si l'on sort de la boucle, on ferme le jeu
pygame.quit()
